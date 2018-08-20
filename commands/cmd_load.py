import click

from faker import Faker

from ami.app import create_app
from ami.extensions import db
from ami.blueprints.meter.models import Meter
from ami.blueprints.data.models import DailyData, HourlyData, MonthlyData, DemandData, AlertData
from ami.blueprints.load.models import LoadMeter, LoadDaily, LoadHourly, LoadMonthly, LoadDemand

# Create an app context for the database connection.
app = create_app()
db.app = app
fake = Faker()


def _log_status(count, model_label):
    """
    Log the output of how many records were created.

    :param count: Amount created
    :type count: int
    :param model_label: Name of the model
    :type model_label: str
    :return: None
    """
    click.echo('Created {0} {1}'.format(count, model_label))

    return None


def _bulk_insert(model, data, label):
    """
    Bulk insert data to a specific model and log it. This is much more
    efficient than adding 1 row at a time in a loop.

    :param model: Model being affected
    :type model: SQLAlchemy
    :param data: Data to be saved
    :type data: list
    :param label: Label for the output
    :type label: str
    :return: None
    """
    with app.app_context():
        model.query.delete()
        db.session.commit()
        db.engine.execute(model.__table__.insert(), data)

        _log_status(model.query.count(), label)

    return None


@click.group()
def cli():
    """ Add items to the database. """
    pass


@click.command()
def meters():
    """
    Generate fake users.
    """
    meter_list = LoadMeter.query.all()
    data = []
    for meter in meter_list:
        params = {
            'id': meter.id,
            'serial_number': meter.serial_no,
            'phone_number': meter.phone_number,
            'sequence_number': meter.customer_seq_no,
            'customer_name': meter.customer_name,
            'ak_ek': meter.ak_ek,
            'branch': meter.branch,
            'zone': meter.zone,
            'lat_long': meter.latlong,
            'initial_reading': meter.initial,
            'ct': meter.ct,
            'current_data': meter.current_data,
            'power': meter.power,
            'online': meter.online,
        }
        data.append(params)
    return _bulk_insert(Meter, data, 'meter')

@click.command()
def loadalert():
    """
    Generate fake users.
    """
    sql = str("""select meter_id ,created_at,alert_name,alert_code	from	ami.alert,	ami.alert_type,	ami.meter
          where	alert.alert_id	=	ami.alert_type.id  and	alert.meter_id	=	ami.meter.id""")
    result = db.engine.execute(sql)
    data = []
    names = []
    for row in result:
        params = {
                'meter_id': row[0],
                'capture_time': row[1],
                'name': row[2],
                'code': row[3],
                }
        data.append(params)

    return _bulk_insert(AlertData, data, 'alerts')



@click.command()
def load_daily():
    """
    Generate fake users.
    """
    data = []
    for meter in Meter.query.all():
        dic = dict()
        for meter_cr in LoadDaily.query.filter(LoadDaily.meter_id == meter.id):
            try:
                dic[meter_cr.created_at].set_value(meter_cr.obis, meter_cr.data)
            except KeyError:
                daily_data = DailyData()
                daily_data.meter_id = meter.id
                daily_data.capture_time = meter_cr.created_at
                daily_data.set_value(meter_cr.obis, meter_cr.data)
                dic[meter_cr.created_at] = daily_data
        for x in dic:
            print(x, dic[x])
            params = {
                'meter_id': dic[x].meter_id,
                'capture_time': x,
                'active_increase': dic[x].active_increase,
                'total_active': str(dic[x].total_active).replace("null", ""),
                'import_active': dic[x].import_active,
                'export_active': dic[x].export_active,
                'import_apparent': dic[x].import_apparent,
                'export_apparent': dic[x].export_apparent,
                'import_reactive': dic[x].import_reactive,
                'export_reactive': dic[x].export_reactive,
            }
            data.append(params)
    return _bulk_insert(DailyData, data, 'daily_data_')


@click.command()
def load_hourly():
    """
    Generate fake users.
    """
    data = []
    for meter in Meter.query.all():
        dic = dict()
        for query_data in LoadHourly.query.filter(LoadHourly.meter_id == meter.id):
            try:
                dic[query_data.created_at].set_value(query_data.obis, query_data.data)
            except KeyError:
                hourly_data = HourlyData()
                hourly_data.meter_id = meter.id
                hourly_data.capture_time = query_data.created_at
                hourly_data.set_value(query_data.obis, query_data.data)
                dic[query_data.created_at] = hourly_data
        for x in dic:
            print(x, dic[x])
            params = {
                'meter_id': dic[x].meter_id,
                'capture_time': x,
                'block_import_active': dic[x].block_import_active,
                'block_export_active': dic[x].block_export_active,
                'block_import_apparent': dic[x].block_import_apparent,
                'block_export_apparent': dic[x].block_export_apparent,
                'block_import_reactive': str(dic[x].block_import_reactive).replace("null", ""),
                'block_export_reactive': dic[x].block_export_reactive,
                'profile_status': dic[x].profile_status,
            }
            data.append(params)
    return _bulk_insert(HourlyData, data, 'hourly_data_')


@click.command()
def load_demand():
    """
    Generate fake users.
    """
    data = []
    for meter in Meter.query.all():
        dic = dict()
        for query_data in LoadDemand.query.filter(LoadDemand.meter_id == meter.id):
            try:
                dic[query_data.created_at].set_value(query_data.obis, query_data.data)
            except KeyError:
                demand_data = DemandData()
                demand_data.meter_id = meter.id
                demand_data.capture_time = query_data.created_at
                demand_data.set_value(query_data.obis, query_data.data)
                dic[query_data.created_at] = demand_data
        for x in dic:
            print(x, dic[x])
            params = {
                'meter_id': dic[x].meter_id,
                'capture_time': x,
                'total_active': str(dic[x].total_active).replace("null", ""),
                'import_active': str(dic[x].import_active).replace("null", ""),
                'export_active': str(dic[x].export_active).replace("null", ""),
                'total_import_apparent': dic[x].total_import_apparent,
                'total_export_apparent': dic[x].total_export_apparent,
                'power_on_duration': str(dic[x].power_on_duration).replace("null", ""),
                'current_x': dic[x].current_x,
                'current_y': str(dic[x].current_y).replace("null", ""),
                'current_z': str(dic[x].current_z).replace("null", ""),
                'current_neutral': dic[x].current_neutral,
                'voltage_x': dic[x].voltage_x,
                'voltage_y': str(dic[x].voltage_y).replace("null", ""),
                'voltage_z': str(dic[x].voltage_z).replace("null", ""),
                'reactive_power': dic[x].reactive_power,
                'apparent_power': dic[x].apparent_power,
                'active_power': dic[x].active_power,
                'billing_count': dic[x].billing_count,
                'output_state': str(dic[x].output_state).replace("null", ""),
                'power_down_count': dic[x].power_down_count,
                'program_count': dic[x].program_count,
                'tamper_count': dic[x].tamper_count,
            }
            data.append(params)
    return _bulk_insert(DemandData, data, 'demand_data_')


@click.command()
def load_monthly():
    """
    Generate fake users.
    """
    data = []
    # Select all data of specific meter
    for meter in Meter.query.all():
        dic = dict()
        for query_data in LoadMonthly.query.filter(LoadMonthly.meter_id == meter.id):
            try:
                dic[query_data.created_at].set_value(query_data.obis, query_data.data)
            except KeyError:
                monthly_data = MonthlyData()
                monthly_data.meter_id = meter.id
                monthly_data.capture_time = query_data.created_at
                monthly_data.set_value(query_data.obis, query_data.data)
                dic[query_data.created_at] = monthly_data
        for x in dic:
            print(x, dic[x])
            params = {
                'meter_id': dic[x].meter_id,
                'capture_time': x,
                'active_increase': str(dic[x].active_increase).replace("null", ""),
                'monthly_active_increase': str(dic[x].monthly_active_increase).replace("null", ""),
                'total_active': str(dic[x].total_active).replace("null", ""),
                'import_active': str(dic[x].import_active).replace("null", ""),
                'total_import_active': dic[x].total_import_active,
                'power_factor': dic[x].power_factor,
                'export_active': dic[x].export_active,
                'total_import_apparent': dic[x].total_import_apparent,
                'total_export_apparent': dic[x].total_export_apparent,
                'import_reactive': dic[x].import_reactive,
                'export_reactive': dic[x].export_reactive,
            }
            data.append(params)
    return _bulk_insert(MonthlyData, data, 'monthly_data_')


@click.command()
@click.pass_context
def all(ctx):
    """
    Generate all data.

    :param ctx:
    :return: None
    """
    # ctx.invoke(meters)
    ctx.invoke(load_daily)
    ctx.invoke(load_hourly)
    ctx.invoke(load_monthly)
    ctx.invoke(load_demand)

    return None


cli.add_command(all)
cli.add_command(loadalert)
