from ami.extensions import db


class LoadMeter(db.Model):
    __bind_key__ = 'ami'
    __tablename__ = 'meter'
    id = db.Column(db.Integer, primary_key=True)
    hes_id = db.Column(db.Integer, index=True, nullable=False)
    serial_no = db.Column(db.String(255))
    customer_seq_no = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    customer_name = db.Column(db.String(255))
    branch = db.Column(db.String(10), nullable=False,
                       server_default='')
    zone = db.Column(db.String(10), nullable=False,
                     server_default='')
    online = db.Column('online', db.Boolean(), nullable=False,
                       server_default='1')
    power = db.Column('power', db.Boolean(), nullable=False,
                      server_default='1')
    ct = db.Column('ct', db.Boolean(), nullable=False,
                   server_default='1')
    ak_ek = db.Column(db.String(255), nullable=False,
                      server_default='30303030303030303030303030303030')
    initial = db.Column(db.String(10), nullable=False,
                        server_default='')
    latlong = db.Column(db.String(30), nullable=False,
                        server_default='')
    current_data = db.Column(db.String(30), nullable=False,
                             server_default='')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(LoadMeter, self).__init__(**kwargs)


class LoadDaily(db.Model):
    __bind_key__ = 'ami'
    __tablename__ = 'daily_data'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.DECIMAL)
    created_at = db.Column(db.TIMESTAMP)
    meter_id = db.Column(db.Integer)
    obis = db.Column(db.String(255))
    name = db.Column(db.String(255))
    scalar = db.Column(db.Integer)
    unit = db.Column(db.String(5))
    unit_value = db.Column(db.Integer)
    value = db.Column(db.DECIMAL)
    data = db.Column(db.String(45))

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(LoadDaily, self).__init__(**kwargs)


class LoadMonthly(db.Model):
    __bind_key__ = 'ami'
    __tablename__ = 'monthly_data'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.DECIMAL)
    created_at = db.Column(db.TIMESTAMP)
    meter_id = db.Column(db.Integer)
    obis = db.Column(db.String(255))
    name = db.Column(db.String(255))
    scalar = db.Column(db.Integer)
    unit = db.Column(db.String(5))
    unit_value = db.Column(db.Integer)
    value = db.Column(db.DECIMAL)
    data = db.Column(db.String(45))

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(LoadDaily, self).__init__(**kwargs)


class LoadHourly(db.Model):
    __bind_key__ = 'ami'
    __tablename__ = 'hourly_data'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.DECIMAL)
    created_at = db.Column(db.TIMESTAMP)
    meter_id = db.Column(db.Integer)
    obis = db.Column(db.String(255))
    name = db.Column(db.String(255))
    scalar = db.Column(db.Integer)
    unit = db.Column(db.String(5))
    unit_value = db.Column(db.Integer)
    value = db.Column(db.DECIMAL)
    data = db.Column(db.String(45))

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(LoadDaily, self).__init__(**kwargs)


class LoadDemand(db.Model):
    __bind_key__ = 'ami'
    __tablename__ = 'demand_data'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.DECIMAL)
    created_at = db.Column(db.TIMESTAMP)
    meter_id = db.Column(db.Integer)
    obis = db.Column(db.String(255))
    name = db.Column(db.String(255))
    scalar = db.Column(db.Integer)
    unit = db.Column(db.String(5))
    unit_value = db.Column(db.Integer)
    value = db.Column(db.DECIMAL)
    data = db.Column(db.String(45))

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(LoadDemand, self).__init__(**kwargs)