from collections import OrderedDict

from flask_wtf import Form
from wtforms import SelectField, StringField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from wtforms_components import Unique
from wtforms_sqlalchemy.fields import QuerySelectField

from lib.util_wtforms import ModelForm, choices_from_dict
from ami.extensions import db
from ami.blueprints.user.models import User
from ami.blueprints.meter.models import Meter
from ami.blueprints.imei.models import Sim, Imei


class SearchForm(Form):
    q = StringField('Search terms', [Optional(), Length(1, 256)])


class DataSearchForm(Form):
    q = StringField('Search terms', [Optional(), Length(1, 256)])
    start = DateTimeField('Start', [Optional()],
                          format='%Y-%m-%d %H:%M:%S')
    end = DateTimeField('End', [Optional()],
                        format='%Y-%m-%d %H:%M:%S')


class BulkDeleteForm(Form):
    SCOPE = OrderedDict([
        ('all_selected_items', 'All selected items'),
        ('all_search_results', 'All search results')
    ])

    scope = SelectField('Privileges', [DataRequired()],
                        choices=choices_from_dict(SCOPE, prepend_blank=False))


class UserForm(ModelForm):
    username_message = 'Letters, numbers and underscores only please.'

    username = StringField(validators=[
        Unique(
            User.username,
            get_session=lambda: db.session
        ),
        Optional(),
        Length(1, 16),
        Regexp('^\w+$', message=username_message)
    ])

    role = SelectField('Privileges', [DataRequired()],
                       choices=choices_from_dict(User.ROLE,
                                                 prepend_blank=False))
    active = BooleanField('Yes, allow this user to sign in')


def serial_query():
    subquery = db.session.query(Meter.serial_number)
    return Imei.query.filter(Imei.meter_identifier.notin_(subquery))


def phone_query():
    subquery = db.session.query(Meter.phone_number)
    return Sim.query.filter(Sim.phone_number.notin_(subquery))


class MeterForm(ModelForm):
    sequence_number_message = 'Sequence number is required and must be unique.'
    serial_number_message = 'Serial number is required and must be unique.'
    phone_number_message = 'Phone number is required and must be unique.'

    sequence_number = StringField(validators=[
        Unique(
            Meter.sequence_number,
            get_session=lambda: db.session
        ),
        DataRequired(),
        Length(1, 16),
        Regexp('^\w+$', message=sequence_number_message)
    ])
    serial_number = QuerySelectField(query_factory=serial_query)
    phone_number = QuerySelectField(query_factory=phone_query)

    customer_name = StringField('Customer Name', [Optional(), Length(1, 256)])
    branch = StringField('Branch', [Optional(), Length(1, 256)])
    zone = StringField('Zone', [Optional(), Length(1, 256)])
    initial_reading = StringField('Initial Reading', [Optional(), Length(1, 256)])
    lat_long = StringField('Lat Long', [Optional(), Length(1, 256)])
    hes = SelectField('HES APP', [DataRequired()],
                      choices=choices_from_dict(Meter.ROLE,
                                                prepend_blank=False))
    active = BooleanField('Yes, allow to collect data from this meter')
