from lib.util_sqlalchemy import ResourceMixin
from ami.extensions import db
from sqlalchemy import or_
from sqlalchemy import and_
from ami.blueprints.meter.models import Meter
from lib.util_datetime import tzware_datetime


class DailyData(ResourceMixin, db.Model):
    __tablename__ = 'daily_data_'
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'), unique=True,
                         index=True, nullable=False)
    meter = db.relationship(Meter, uselist=False, backref='daily_data_',
                            passive_deletes=True)
    capture_time = db.Column(db.TIMESTAMP, default=tzware_datetime, unique=True)
    active_increase = db.Column(db.String(25), nullable=False, server_default='')
    total_active = db.Column(db.String(25), nullable=False, server_default='')
    import_active = db.Column(db.String(25), nullable=False, server_default='')
    export_active = db.Column(db.String(25), nullable=False, server_default='')
    import_apparent = db.Column(db.String(25), nullable=False, server_default='')
    export_apparent = db.Column(db.String(25), nullable=False, server_default='')
    import_reactive = db.Column(db.String(25), nullable=False, server_default='')
    export_reactive = db.Column(db.String(25), nullable=False, server_default='')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(DailyData, self).__init__(**kwargs)

    def set_value(self, obis, value):
        if obis == "1.0.15.8.0.255":
            # cumulative_total_active_energy
            self.total_active = value
        elif obis == "1.0.1.8.0.255":
            # cumulative_import_active_energy
            self.import_active = value
        elif obis == "1.0.2.8.0.255":
            # cumulative_export_active_energy
            self.export_active = value
        elif obis == "1.0.3.8.0.255":
            # cumulative_import_reactive_energy
            self.import_reactive = value
        elif obis == "1.0.4.8.0.255":
            # cumulative_import_reactive_energy
            self.export_reactive = value
        elif obis == "1.0.9.8.0.255":
            # cumulative_import_apparent_energy
            self.import_apparent = value
        elif obis == "1.0.10.8.0.255":
            # cumulative_export_apparent_energy
            self.export_apparent = value
        elif obis == "1.0.15.19.0.255":
            # current_day_active_energy_increase
            self.active_increase = value

    @classmethod
    def query_search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if query:
            search_query = '%{0}%'.format(query)
            query_chain = (DailyData.meter.property.mapper.class_.sequence_number.ilike(search_query),
                           DailyData.meter.property.mapper.class_.serial_number.ilike(search_query))
            return or_(*query_chain)
        return ''

    @classmethod
    def date_search(cls, start_date, end_date):
        """
        Search a resource by 1 or more fields.

        :param end_date:
        :param start_date:
        :return: SQLAlchemy filter
        """
        if start_date and end_date:
            date_chain = (DailyData.capture_time >= start_date,
                          DailyData.capture_time <= end_date)
            return and_(*date_chain)
        return ''

    @property
    def serialize(self):
        return {
            'id': self.id,
            'meter_id': self.meter_id,
            'active_increase': self.active_increase,
            'total_active': self.total_active,
            'import_active':self.import_active,
            'export_active':self.export_active,
            'sequence_number': self.meter.sequence_number,
            'capture_time': self.capture_time,
        }


class HourlyData(ResourceMixin, db.Model):
    __tablename__ = 'hourly_data_'
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'), unique=True,
                         index=True, nullable=False)
    meter = db.relationship(Meter, uselist=False, backref='hourly_data',
                            passive_deletes=True)
    capture_time = db.Column(db.TIMESTAMP, default=tzware_datetime, unique=True, index=True)
    block_import_active = db.Column(db.String(25), nullable=False, server_default='')
    block_export_active = db.Column(db.String(25), nullable=False, server_default='')
    block_import_apparent = db.Column(db.String(25), nullable=False, server_default='')
    block_export_apparent = db.Column(db.String(25), nullable=False, server_default='')
    block_import_reactive = db.Column(db.String(25), nullable=False, server_default='')
    block_export_reactive = db.Column(db.String(25), nullable=False, server_default='')
    profile_status = db.Column(db.String(25), nullable=False, server_default='')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(HourlyData, self).__init__(**kwargs)

    def set_value(self, obis, value):
        if obis == "1.0.1.29.0.255":
            # BLOCK_IMPORT_ACTIVE = "1.0.1.29.0.255"
            self.block_import_active = value
        elif obis == "1.0.2.29.0.255":
            # BLOCK_EXPORT_ACTIVE = "1.0.2.29.0.255"
            self.block_export_active = value
        elif obis == "1.0.3.29.0.255":
            # BLOCK_IMPORT_REACTIVE = "1.0.3.29.0.255"
            self.block_export_reactive = value
        elif obis == "1.0.4.29.0.255":
            # BLOCK_EXPORT_REACTIVE = "1.0.4.29.0.255"
            self.block_export_reactive = value
        elif obis == "1.0.9.29.0.255":
            # BLOCK_IMPORT_APPARENT = "1.0.9.29.0.255"
            self.block_import_apparent = value
        elif obis == "1.0.10.29.0.255":
            # BLOCK_EXPORT_APPARENT = "1.0.10.29.0.255"
            self.block_export_apparent = value
        elif obis == "0.0.96.10.1.255":
            # PROFILE_STATUS = "0.0.96.10.1.255"
            self.profile_status = value

    @classmethod
    def query_search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if query:
            search_query = '%{0}%'.format(query)
            query_chain = (HourlyData.meter.property.mapper.class_.sequence_number.ilike(search_query),
                           HourlyData.meter.property.mapper.class_.serial_number.ilike(search_query))
            return or_(*query_chain)
        return ''

    @classmethod
    def date_search(cls, start_date, end_date):
        """
        Search a resource by 1 or more fields.

        :param end_date:
        :param start_date:
        :return: SQLAlchemy filter
        """
        if start_date and end_date:
            date_chain = (HourlyData.capture_time >= start_date,
                          HourlyData.capture_time <= end_date)
            return and_(*date_chain)
        return ''
    @property
    def serialize(self):
        return {
            'id': self.id,
            'meter_id': self.meter_id,
            'import_active': self.block_import_active,
            'export_active': self.block_export_active,
            'import_reactive':self.block_import_reactive,
            'export_reactive':self.block_export_reactive,
            'import_apparent':self.block_import_apparent,
            'bexport_apparent':self.block_export_apparent,
            'sequence_number': self.meter.sequence_number,
            'capture_time': self.capture_time,
        }

class DemandData(ResourceMixin, db.Model):
    __tablename__ = 'demand_data_'
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'), unique=True,
                         index=True, nullable=False)
    meter = db.relationship(Meter, uselist=False, backref='demand_data',
                            passive_deletes=True)

    capture_time = db.Column(db.TIMESTAMP, default=tzware_datetime, unique=True, index=True)
    total_active = db.Column(db.String(25), nullable=False, server_default='')

    import_active = db.Column(db.String(25), nullable=False, server_default='')
    export_active = db.Column(db.String(25), nullable=False, server_default='')

    total_import_apparent = db.Column(db.String(25), nullable=False, server_default='')
    total_export_apparent = db.Column(db.String(25), nullable=False, server_default='')

    power_on_duration = db.Column(db.String(25), nullable=False, server_default='')

    current_x = db.Column(db.String(255), nullable=False, server_default='')
    current_y = db.Column(db.String(255), nullable=False, server_default='')
    current_z = db.Column(db.String(255), nullable=False, server_default='')

    current_neutral = db.Column(db.String(255), nullable=False, server_default='')
    voltage_x = db.Column(db.String(255), nullable=False, server_default='')
    voltage_y = db.Column(db.String(255), nullable=False, server_default='')
    voltage_z = db.Column(db.String(255), nullable=False, server_default='')

    reactive_power = db.Column(db.String(25), nullable=False, server_default='')
    apparent_power = db.Column(db.String(25), nullable=False, server_default='')
    active_power = db.Column(db.String(25), nullable=False, server_default='')

    billing_count = db.Column(db.String(25), nullable=False, server_default='')
    output_state = db.Column(db.String(25), nullable=False, server_default='')
    power_down_count = db.Column(db.String(25), nullable=False, server_default='')
    program_count = db.Column(db.String(25), nullable=False, server_default='')
    tamper_count = db.Column(db.String(25), nullable=False, server_default='')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(DemandData, self).__init__(**kwargs)

    @classmethod
    def query_search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if query:
            search_query = '%{0}%'.format(query)
            query_chain = (DemandData.meter.property.mapper.class_.sequence_number.ilike(search_query),
                           DemandData.meter.property.mapper.class_.serial_number.ilike(search_query))
            return or_(*query_chain)
        return ''

    @classmethod
    def date_search(cls, start_date, end_date):
        """
        Search a resource by 1 or more fields.

        :param end_date:
        :param start_date:
        :return: SQLAlchemy filter
        """
        if start_date and end_date:
            date_chain = (DemandData.capture_time >= start_date,
                          DemandData.capture_time <= end_date)
            return and_(*date_chain)
        return ''

    def set_value(self, obis, value):
        if obis == "0.0.96.3.10.255":
            # OUTPUT_STATE:
            self.output_state = value
        elif obis == "1.0.0.1.0.255":
            # BILLING_COUNT
            self.billing_count = value
        elif obis == "0.0.96.7.0.255":
            # POWER_DOWN_COUNT
            self.power_down_count = value
        elif obis == "0.0.96.2.0.255":
            # PROGRAM_COUNT
            self.program_count = value
        elif obis == "0.0.96.91.0.255":
            # TAMPER_COUNT
            self.tamper_count = value
        elif obis == "1.0.32.7.0.255":
            # VOLTAGE_PHASE_ONE
            self.voltage_x = value
        elif obis == "1.0.31.7.0.255":
            # CURRENT_PHASE_ONE
            self.current_x = value
        elif obis == "1.0.91.7.0.255":
            # NEUTRAL
            self.current_neutral = value
        elif obis == "1.0.1.7.0.255":
            # ACTIVE_POWER
            self.active_power = value
        elif obis == "1.0.3.7.0.255":
            # REACTIVE_POWER
            self.reactive_power = value
        elif obis == "1.0.9.7.0.255":
            # APPARENT_POWER
            self.apparent_power = value
        elif obis == "0.0.96.91.14.255":
            # POWER_ON_DURATION
            self.power_on_duration = value
        elif obis == "1.0.13.7.0.255":
            # POWER_FACTOR
            self.power_factor = value
        elif obis == "1.0.14.7.0.255":
            # FREQUENCY
            self.frequency = value
        elif obis == "1.0.51.7.0.255":
            # CURRENT_PHASE_TWO
            self.current_y = value
        elif obis == "1.0.52.7.0.255":
            # VOLTAGE_PHASE_TWO
            self.voltage_y = value
        elif obis == "1.0.71.7.0.255":
            # CURRENT_PHASE_THREE
            self.current_z = value
        elif obis == "1.0.72.7.0.255":
            # VOLTAGE_PHASE_THREE
            self.voltage_z = value
        elif obis == "1.0.9.8.0.255":
            # TOTAL_IMPORT_APPARENT
            self.total_import_apparent = value
        elif obis == "1.0.1.8.0.255":
            # TOTAL_IMPORT_ACTIVE
            self.total_import_active = value
        elif obis == "1.0.10.8.0.255":
            # TOTAL_EXPORT_APPARENT
            self.total_export_apparent = value
        elif obis == "1.0.2.8.0.255":
            # EXPORT_ACTIVE
            self.total_export_active = value


class MonthlyData(ResourceMixin, db.Model):
    __tablename__ = 'monthly_data_'
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'), unique=True,
                         index=True, nullable=False)
    meter = db.relationship(Meter, uselist=False, backref='monthly_data_',
                            passive_deletes=True)
    capture_time = db.Column(db.TIMESTAMP, default=tzware_datetime, unique=True, index=True)
    active_increase = db.Column(db.String(25), nullable=False, server_default='')
    monthly_active_increase = db.Column(db.String(25), nullable=False, server_default='')
    total_active = db.Column(db.String(25), nullable=False, server_default='')
    import_active = db.Column(db.String(25), nullable=False, server_default='')
    total_import_active = db.Column(db.String(25), nullable=False, server_default='')
    power_factor = db.Column(db.String(25), nullable=False, server_default='')
    export_active = db.Column(db.String(25), nullable=False, server_default='')
    total_import_apparent = db.Column(db.String(25), nullable=False, server_default='')
    total_export_apparent = db.Column(db.String(25), nullable=False, server_default='')
    import_reactive = db.Column(db.String(25), nullable=False, server_default='')
    export_reactive = db.Column(db.String(25), nullable=False, server_default='')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(MonthlyData, self).__init__(**kwargs)

    @classmethod
    def query_search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if query:
            search_query = '%{0}%'.format(query)
            query_chain = (MonthlyData.meter.property.mapper.class_.sequence_number.ilike(search_query),
                           MonthlyData.meter.property.mapper.class_.serial_number.ilike(search_query))
            print(search_query)
            print(or_(*query_chain))
            return or_(*query_chain)
        return ''

    @classmethod
    def date_search(cls, start_date, end_date):
        """
        Search a resource by 1 or more fields.

        :param end_date:
        :param start_date:
        :return: SQLAlchemy filter
        """
        if start_date and end_date:
            date_chain = (MonthlyData.capture_time >= start_date,
                          MonthlyData.capture_time <= end_date)
            print(or_(*date_chain))
            return and_(*date_chain)
        return ''

    @property
    def serialize(self):
        return {
            'id': self.id,
            'meter_id': self.meter_id,
            'active_increase': self.monthly_active_increase,
            'total_active': self.total_active,
            'import_active': self.import_active,
            'export_active': self.export_active,
            'import_reactive':self.import_reactive,
            'export_reactive':self.export_reactive,
            'import_apparent':self.total_import_apparent,
            'export_apparent':self.total_export_apparent,
            'sequence_number': self.meter.sequence_number,
            'capture_time': self.capture_time,
        }

def set_value(self, obis, value):
        if obis == "1.0.1.8.0.255":
            # TOTAL_IMPORT_ACTIVE
            self.total_import_active = value
        elif obis == "1.0.2.8.0.255":
            # EXPORT_ACTIVE
            self.export_active = value
        elif obis == "1.0.3.8.0.255":
            # IMPORT_REACTIVE
            self.import_reactive = value
        elif obis == "1.0.4.8.0.255":
            # EXPORT_REACTIVE
            self.export_reactive = value
        elif obis == "1.0.9.8.0.255":
            # TOTAL_IMPORT_APPARENT
            self.total_import_apparent = value
        elif obis == "1.0.10.8.0.255":
            # TOTAL_EXPORT_APPARENT
            self.total_export_apparent = value
        elif obis == "1.0.15.19.0.255":
            # ACTIVE_INCREASE
            self.active_increase = value
        elif obis == "1.0.13.0.0.255":
            # BILLING_PERIOD_AVERAGE_POWER_FACTOR
            self.power_factor = value
        elif obis == "1.0.15.8.0.255":
            # TOTAL_ACTIVE
            self.total_active = value
        elif obis == "1.0.15.9.0.255":
            # MONTH_ACTIVE_INCREASE
            self.monthly_active_increase = value


class AlertData(ResourceMixin, db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    # Relationships.
    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'),
                         index=True, nullable=False)
    meter = db.relationship(Meter, uselist=False, backref='alerts',
                            passive_deletes=True)

    capture_time = db.Column(db.TIMESTAMP, default=tzware_datetime, unique=True, index=True)
    code = db.Column(db.Integer)
    name = db.Column(db.String(25), nullable=False, server_default='')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(AlertData, self).__init__(**kwargs)

    @classmethod
    def query_search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if query:
            search_query = '%{0}%'.format(query)
            query_chain = (AlertData.meter.property.mapper.class_.sequence_number.ilike(search_query),
                           AlertData.meter.property.mapper.class_.serial_number.ilike(search_query))
            return or_(*query_chain)
        return ''

    @classmethod
    def date_search(cls, start_date, end_date):
        """
        Search a resource by 1 or more fields.

        :param end_date:
        :param start_date:
        :return: SQLAlchemy filter
        """
        if start_date and end_date:
            date_chain = (AlertData.capture_time >= start_date,
                          AlertData.capture_time <= end_date)
            return and_(*date_chain)
        return ''

    @property
    def serialize(self):
        return {
            'id': self.id,
            'meter_id': self.meter_id,
            'code': self.code,
            'name': self.name,
            'sequence_number': self.meter.sequence_number,
            'capture_time': self.capture_time,
        }
