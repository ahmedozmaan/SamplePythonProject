from lib.util_sqlalchemy import ResourceMixin
from ami.extensions import db
from sqlalchemy import or_
from sqlalchemy import and_
from ami.blueprints.meter.models import Meter
from lib.util_datetime import tzware_datetime


class DailyData(ResourceMixin, db.Model):
    __tablename__ = 'daily_data'
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'),
                         index=True, nullable=False)
    meter = db.relationship(Meter, uselist=False, backref='daily_data',
                            passive_deletes=True)
    capture_time = db.Column(db.TIMESTAMP, default=tzware_datetime, unique=True, index=True)
    active_increase = db.Column(db.String(25), nullable=False, server_default='')
    total_active = db.Column(db.String(25), nullable=False, server_default='')
    import_active = db.Column(db.String(25), nullable=False, server_default='')
    export_active = db.Column(db.String(25), nullable=False, server_default='')
    import_apparent = db.Column(db.String(25), nullable=False, server_default='')
    export_apparent = db.Column(db.String(25), nullable=False, server_default='')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(DailyData, self).__init__(**kwargs)

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


class HourlyData(ResourceMixin, db.Model):
    __tablename__ = 'hourly_data'
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'),
                         index=True, nullable=False)
    meter = db.relationship(Meter, uselist=False, backref='hourly_data',
                            passive_deletes=True)
    capture_time = db.Column(db.TIMESTAMP, default=tzware_datetime, unique=True, index=True)
    import_active = db.Column(db.String(25), nullable=False, server_default='')
    export_active = db.Column(db.String(25), nullable=False, server_default='')
    import_apparent = db.Column(db.String(25), nullable=False, server_default='')
    export_apparent = db.Column(db.String(25), nullable=False, server_default='')
    import_reactive = db.Column(db.String(25), nullable=False, server_default='')
    export_reactive = db.Column(db.String(25), nullable=False, server_default='')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(HourlyData, self).__init__(**kwargs)

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


class DemandData(ResourceMixin, db.Model):
    __tablename__ = 'demand_data'
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'),
                         index=True, nullable=False)
    meter = db.relationship(Meter, uselist=False, backref='demand_data',
                            passive_deletes=True)

    capture_time = db.Column(db.TIMESTAMP, default=tzware_datetime, unique=True, index=True)
    total_active = db.Column(db.String(25), nullable=False, server_default='')

    import_active = db.Column(db.String(25), nullable=False, server_default='')
    export_active = db.Column(db.String(25), nullable=False, server_default='')

    import_apparent = db.Column(db.String(25), nullable=False, server_default='')
    export_apparent = db.Column(db.String(25), nullable=False, server_default='')

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


class MonthlyData(ResourceMixin, db.Model):
    __tablename__ = 'monthly_data'
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'),
                         index=True, nullable=False)
    meter = db.relationship(Meter, uselist=False, backref='monthly_data',
                            passive_deletes=True)
    capture_time = db.Column(db.TIMESTAMP, default=tzware_datetime, unique=True, index=True)
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
            return and_(*date_chain)
        return ''


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
            'capture_time': self.capture_time,
        }
