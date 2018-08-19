from flask import (
    Blueprint,
    redirect,
    request,
    flash,
    url_for,
    jsonify,
    render_template)
from flask_login import login_required, current_user
from sqlalchemy import text

from ami.blueprints.admin.models import Dashboard
from ami.blueprints.user.decorators import role_required
from ami.blueprints.user.models import User
from ami.blueprints.meter.models import Meter
from ami.blueprints.imei.models import Imei, Sim

from ami.blueprints.data.models import (
    HourlyData,
    MonthlyData,
    DailyData,
    DemandData,
    AlertData
)
from ami.blueprints.admin.forms import (
    SearchForm,
    BulkDeleteForm,
    UserForm,
    MeterForm,
    DataSearchForm
)

admin = Blueprint('admin', __name__,
                  template_folder='templates', url_prefix='/admin')


@admin.before_request
@login_required
@role_required('admin')
def before_request():
    """ Protect all of the admin endpoints. """
    pass


# Dashboard -------------------------------------------------------------------
@admin.route('')
def dashboard():
    group_and_count_users = Dashboard.group_and_count_users()

    return render_template('admin/page/dashboard.html',
                           group_and_count_users=group_and_count_users)


# Imei -----------------------------------------------------------------------
@admin.route('/imei', defaults={'page': 1})
@admin.route('/imei/page/<int:page>')
def imei(page):
    search_form = SearchForm()

    sort_by = Imei.sort_by(request.args.get('sort', 'created_on'),
                           request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    imeies = Imei.query \
        .filter(Imei.search(request.args.get('q', ''))) \
        .order_by(text(order_values)) \
        .paginate(page, 50, True)

    return render_template('admin/imei/index.html',
                           form=search_form,
                           data=imeies)


# Sim -----------------------------------------------------------------------
@admin.route('/sim', defaults={'page': 1})
@admin.route('/sim/page/<int:page>')
def sim(page):
    search_form = SearchForm()

    sort_by = Sim.sort_by(request.args.get('sort', 'created_on'),
                          request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    sim_cards = Sim.query \
        .filter(Sim.search(request.args.get('q', ''))) \
        .order_by(text(order_values)) \
        .paginate(page, 50, True)

    return render_template('admin/sim/index.html',
                           form=search_form,
                           data=sim_cards)


# Users -----------------------------------------------------------------------
@admin.route('/users', defaults={'page': 1})
@admin.route('/users/page/<int:page>')
def users(page):
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = User.sort_by(request.args.get('sort', 'created_on'),
                           request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_users = User.query \
        .filter(User.search(request.args.get('q', ''))) \
        .order_by(User.role.asc(), text(order_values)) \
        .paginate(page, 50, True)

    return render_template('admin/user/index.html',
                           form=search_form, bulk_form=bulk_form,
                           users=paginated_users)


@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def users_edit(id):
    user = User.query.get(id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        if User.is_last_admin(user,
                              request.form.get('role'),
                              request.form.get('active')):
            flash('You are the last admin, you cannot do that.', 'error')
            return redirect(url_for('admin.users'))

        form.populate_obj(user)

        if not user.username:
            user.username = None

        user.save()

        flash('User has been saved successfully.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user/edit.html', form=form, user=user)


@admin.route('/users/bulk_delete', methods=['POST'])
def users_bulk_delete():
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = User.get_bulk_action_ids(request.form.get('scope'),
                                       request.form.getlist('bulk_ids'),
                                       omit_ids=[current_user.id],
                                       query=request.args.get('q', ''))

        delete_count = User.bulk_delete(ids)

        flash('{0} user(s) were scheduled to be deleted.'.format(delete_count),
              'success')
    else:
        flash('No users were deleted, something went wrong.', 'error')

    return redirect(url_for('admin.users'))


# Meters -----------------------------------------------------------------------
@admin.route('/meters', defaults={'page': 1})
@admin.route('/meters/page/<int:page>')
def meters(page):
    search_form = SearchForm()
    sort_by = Meter.sort_by(request.args.get('sort', 'created_on'),
                            request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_meters = Meter.query \
        .filter(Meter.search(request.args.get('q', ''))) \
        .order_by(Meter.serial_number.asc(), text(order_values)) \
        .paginate(page, 50, True)

    return render_template('admin/meter/index.html',
                           form=search_form,  # bulk_form=bulk_form,
                           meters=paginated_meters)


@admin.route('/meters/edit/<int:id>', methods=['GET', 'POST'])
def meters_edit(id):
    meter = Meter.query.get(id)
    form = MeterForm(obj=meter)

    if form.validate_on_submit():
        form.populate_obj(meter)
        meter.save()
        flash('Meter has been Updated successfully.', 'success')
        return redirect(url_for('admin.meters'))

    return render_template('admin/meter/edit.html', form=form, meter=meter)


@admin.route('/meters/detail/<int:id>', methods=['GET', 'POST'])
def meters_detail(id):
    meter = Meter.query.get(id)
    if request.method == 'POST':
        if request.form['dataType']:
            meter = Meter.query.get(request.form['dataType'])
            return jsonify(MeterData=meter.serialize)
    return render_template('admin/meter/detail.html', meter=meter)


@admin.route('/meters/data/<int:meter_id>', methods=['GET', 'POST'])
def meters_data(meter_id):
    if request.method == 'POST':
        data_type = int(request.form['dataType'])
        meter = Meter.query.get(meter_id)
        data = None
        if meter:
            if data_type == 0:
                data = DemandData.query \
                    .filter(DemandData.query_search(meter.sequence_number)) \
                    .order_by(DemandData.created_on.asc()) \
                    .paginate(1, 10, True)
            elif data_type == 1:
                data = AlertData.query \
                    .filter(AlertData.query_search(meter.sequence_number)) \
                    .order_by(AlertData.created_on.asc()) \
                    .paginate(1, 10, True)
            elif data_type == 2:
                data = HourlyData.query \
                    .filter(HourlyData.query_search(meter.sequence_number)) \
                    .order_by(HourlyData.created_on.asc()) \
                    .paginate(1, 10, True)
            elif data_type == 3:
                data = DailyData.query \
                    .filter(DailyData.query_search(meter.sequence_number)) \
                    .order_by(DailyData.created_on.asc()) \
                    .paginate(1, 10, True)
            elif data_type == 4:
                data = MonthlyData.query \
                    .filter(MonthlyData.query_search(meter.sequence_number)) \
                    .order_by(MonthlyData.created_on.asc()) \
                    .paginate(1, 10, True)
        if data:
            return jsonify([i.serialize for i in data.items])
    return ''


@admin.route('/meters/add', methods=['GET', 'POST'])
def meters_add():
    form = MeterForm()
    if form.validate_on_submit():
        meter = Meter()
        form.populate_obj(meter)

        meter.serial_number = str(meter.serial_number).split(":")[0].strip()
        meter.phone_number = str(meter.phone_number).split(":")[0].strip()
        meter.save()
        flash('Meter has been Registered successfully.', 'success')
        return redirect(url_for('admin.meters'))
    return render_template('admin/meter/add.html', form=form)


# Meter Data -----------------------------------------------------------------------
@admin.route('/data/demand', defaults={'page': 1})
@admin.route('/data/demand/page/<int:page>')
def data_demand(page):
    sort_by = DemandData.sort_by(request.args.get('sort', 'created_on'),
                                 request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_data = DemandData.query \
        .filter(DemandData.query_search(request.args.get('q', ''))) \
        .filter(DemandData.date_search(request.args.get('start', ''), request.args.get('end', ''))) \
        .join(Meter, Meter.id == DemandData.meter_id)\
        .order_by(text(order_values)) \
        .paginate(page, 50, True)

    return render_template('admin/data/demand.html',
                           form=DataSearchForm(),
                           data=paginated_data)


@admin.route('/data/alert', defaults={'page': 1})
@admin.route('/data/alert/page/<int:page>')
def data_alert(page):
    sort_by = AlertData.sort_by(request.args.get('sort', 'created_on'),
                                request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_data = AlertData.query \
        .filter(AlertData.query_search(request.args.get('q', ''))) \
        .filter(AlertData.date_search(request.args.get('start', ''), request.args.get('end', ''))) \
        .order_by(text(order_values)) \
        .paginate(page, 50, True)

    return render_template('admin/data/alert.html',
                           form=DataSearchForm(),
                           data=paginated_data)


@admin.route('/data/hourly', defaults={'page': 1})
@admin.route('/data/hourly/page/<int:page>')
def data_hourly(page):
    sort_by = HourlyData.sort_by(request.args.get('sort', 'created_on'),
                                 request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_data = HourlyData.query \
        .filter(HourlyData.query_search(request.args.get('q', ''))) \
        .filter(HourlyData.date_search(request.args.get('start', ''), request.args.get('end', ''))) \
        .join(Meter, Meter.id == HourlyData.meter_id)\
        .order_by(text(order_values)) \
        .paginate(page, 50, True)

    return render_template('admin/data/hourly.html',
                           form=DataSearchForm(),
                           data=paginated_data)


@admin.route('/data/daily', defaults={'page': 1})
@admin.route('/data/daily/page/<int:page>')
def data_daily(page):
    sort_by = DailyData.sort_by(request.args.get('sort', 'created_on'),
                                request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_data = DailyData.query \
        .filter(DailyData.query_search(request.args.get('q', ''))) \
        .filter(DailyData.date_search(request.args.get('start', ''), request.args.get('end', ''))) \
        .join(Meter, Meter.id == DailyData.meter_id)\
        .order_by(text(order_values)) \
        .paginate(page, 50, True)

    return render_template('admin/data/daily.html',
                           form=DataSearchForm(),
                           data=paginated_data)


@admin.route('/data/monthly', defaults={'page': 1})
@admin.route('/data/monthly/page/<int:page>')
def data_monthly(page):
    sort_by = MonthlyData.sort_by(request.args.get('sort', 'created_on'),
                                  request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_data = MonthlyData.query \
        .filter(MonthlyData.query_search(request.args.get('q', ''))) \
        .filter(MonthlyData.date_search(request.args.get('start', ''), request.args.get('end', ''))) \
        .join(Meter, Meter.id == MonthlyData.meter_id)\
        .order_by(text(order_values)) \
        .paginate(page, 50, True)

    return render_template('admin/data/monthly.html',
                           form=DataSearchForm(),
                           data=paginated_data)


def prettyprintable(statement, dialect=None, reindent=True):
    """Generate an SQL expression string with bound parameters rendered inline
    for the given SQLAlchemy statement. The function can also receive a
    `sqlalchemy.orm.Query` object instead of statement.
    can

    WARNING: Should only be used for debugging. Inlining parameters is not
             safe when handling user created data.
    """
    import sqlparse
    import sqlalchemy.orm
    if isinstance(statement, sqlalchemy.orm.Query):
        if dialect is None:
            dialect = statement.session.get_bind().dialect
        statement = statement.statement
    compiled = statement.compile(dialect=dialect,
                                 compile_kwargs={'literal_binds': True})
    return sqlparse.format(str(compiled), reindent=reindent)
