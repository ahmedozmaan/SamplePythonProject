from datetime import timedelta

DEBUG = True
LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG

SERVER_NAME = 'localhost:8000'
SECRET_KEY = 'insecurekeyfordev'

# Flask-Mail.
#MAIL_DEFAULT_SENDER = 'contact@local.host'
#MAIL_SERVER = 'smtp.gmail.com'
#MAIL_PORT = 587
#MAIL_USE_TLS = True
#MAIL_USE_SSL = False
#MAIL_USERNAME = 'you@gmail.com'
#MAIL_PASSWORD = 'awesomepassword'

# Celery.
#CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
#CELERY_RESULT_BACKEND = 'redis://:devpassword@redis:6379/0'
#CELERY_ACCEPT_CONTENT = ['json']
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'
#CELERY_REDIS_MAX_CONNECTIONS = 5

# SQLAlchemy.
#db_uri = 'postgresql://snakeeyes:devpassword@postgres:5432/snakeeyes'
db_uri = 'mysql://development:development@localhost/myami'

SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_BINDS = {
    'myami':        db_uri,
    'ami':      'mysql://development:development@localhost/ami'
}

# User.
SEED_ADMIN_EMAIL = 'ahmed@local.host'
SEED_ADMIN_PASSWORD = 'aothecode'
REMEMBER_COOKIE_DURATION = timedelta(days=90)
