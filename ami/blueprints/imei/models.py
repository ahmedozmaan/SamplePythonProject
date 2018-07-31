from lib.util_sqlalchemy import ResourceMixin
from ami.extensions import db
from sqlalchemy import or_


class Imei(ResourceMixin, db.Model):
    __tablename__ = 'imei'
    id = db.Column(db.Integer, primary_key=True)
    meter_identifier = db.Column(db.String(30), unique=True, index=True)
    modem_imei = db.Column(db.String(30), unique=True, index=True, default='')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Imei, self).__init__(**kwargs)

    def __str__(self):
        return str(self.meter_identifier) + " : " + str(self.modem_imei)


    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a meter by its sequence_number or serial_number or phone_number.

        :param identity: sequence_number or serial_number or phone_number
        :type identity: str
        :return: Meter instance
        """
        return Imei.query.filter(
            (Imei.meter_identifier == identity) | (Imei.modem_imei == identity)).first()

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
        search_chain = (Imei.meter_identifier.ilike(search_query),
                        Imei.modem_imei.ilike(search_query))

        return or_(*search_chain)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'meter_identifier': self.meter_identifier,
            'modem_imei': self.modem_imei,
            'created_on': self.created_on,
            'updated_on': self.updated_on,
        }


class Sim(ResourceMixin, db.Model):
    __tablename__ = 'sim'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(25), unique=True, index=True)
    sim_serial = db.Column(db.String(25), unique=True, index=True, default='')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Imei, self).__init__(**kwargs)

    def __str__(self):
        return str(self.phone_number) + " : " + str(self.sim_serial)

    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a meter by its sequence_number or serial_number or phone_number.

        :param identity: sequence_number or serial_number or phone_number
        :type identity: str
        :return: Meter instance
        """
        return Imei.query.filter(
            (Imei.phone_number == identity) | (Imei.sim_serial == identity)).first()

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
        search_chain = (Imei.phone_number.ilike(search_query),
                        Imei.sim_serial.ilike(search_query))

        return or_(*search_chain)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'phone_number': self.meter_identifier,
            'sim_serial': self.modem_imei,
            'created_on': self.created_on,
            'updated_on': self.updated_on,
        }