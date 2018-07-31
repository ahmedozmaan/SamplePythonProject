import datetime
from collections import OrderedDict
from lib.util_sqlalchemy import ResourceMixin
from ami.extensions import db
from sqlalchemy import or_


class Meter(ResourceMixin, db.Model):
    ROLE = OrderedDict([
        ('dev', 'Development'),
        ('pro', 'Production')
    ])
    __tablename__ = 'meters'
    id = db.Column(db.Integer, primary_key=True)
    sequence_number = db.Column(db.String(20), unique=True, index=True)
    serial_number = db.Column(db.String(20), unique=True, index=True, nullable=False,
                              server_default='')
    phone_number = db.Column(db.String(20), unique=True, index=True, nullable=False,
                             server_default='')
    customer_name = db.Column(db.String(255), nullable=False,
                              server_default='')
    ak_ek = db.Column(db.String(255), nullable=False,
                      server_default='30303030303030303030303030303030')
    branch = db.Column(db.String(10), nullable=False,
                       server_default='')
    zone = db.Column(db.String(10), nullable=False,
                     server_default='')
    initial_reading = db.Column(db.String(10), nullable=False,
                                server_default='')
    lat_long = db.Column(db.String(30), nullable=False,
                         server_default='')
    online = db.Column('is_online', db.Boolean(), nullable=False,
                       server_default='1')
    power = db.Column('power_on', db.Boolean(), nullable=False,
                      server_default='1')
    ct = db.Column('is_ct', db.Boolean(), nullable=False,
                   server_default='1')
    active = db.Column('is_active', db.Boolean(), nullable=False,
                       server_default='1')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Meter, self).__init__(**kwargs)

    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a meter by its sequence_number or serial_number or phone_number.

        :param identity: sequence_number or serial_number or phone_number
        :type identity: str
        :return: Meter instance
        """
        return Meter.query.filter(
            (Meter.sequence_number == identity) | (Meter.phone_number == identity) | (
                Meter.serial_number == identity)).first()

    def is_active(self):
        """
        Return whether or not the user account is active, this satisfies
        Flask-Login by overwriting the default value.

        :return: bool
        """
        return self.active

    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        search_chain = (Meter.sequence_number.ilike(search_query),
                        Meter.serial_number.ilike(search_query),
                        Meter.phone_number.ilike(search_query))

        return or_(*search_chain)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'serial_number': self.serial_number,
            'sequence_number': self.sequence_number,
            'phone_number': self.phone_number,
            'customer_name': self.customer_name,
            'ak_ek': self.ak_ek,
            'active': self.active,
            'branch': self.branch,
            'zone': self.zone,
            'lat_long': self.lat_long,
            'initial_reading': self.initial_reading,
            'ct': self.ct,
            'power': self.power,
            'online': self.online,
            'created_on': self.created_on,
            'updated_on': self.updated_on,
        }
