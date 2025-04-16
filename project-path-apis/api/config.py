import datetime
import os
from dotenv import load_dotenv
import sqlalchemy

load_dotenv()
_basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    APP_BASE_URL = os.environ.get("APPBASEURL")
    # Database Configs
    DHOST = os.environ.get("DHOST")
    DPORT = os.environ.get("DPORT")
    DBASE = os.environ.get("DBASE")
    DUSER = os.environ.get("DUSER")
    DPASS = os.environ.get("DPASS")
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DUSER}:{DPASS}@{DHOST}:{DPORT}/{DBASE}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    # REDIS
    REDIS_PASSWORD = os.environ.get("REDISPASSWORD")
    REDIS_HOST = os.environ.get("REDISHOST")
    REDIS_PORT = os.environ.get("REDISPORT")
    REDIS_DATABASE = os.environ.get("REDISDATABASE")

    # CORS_SEND_WILDCARD = True

    # Celery configs
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Africa/Nairobi'
    CELERY_BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DATABASE}"
    CELERY_RESULT_BACKEND = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DATABASE}"
    CELERY_TASK_RESULT_EXPIRES = 600

    # JWT
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    JWT_SECRET_KEY = (
        "5baa87c5f3f08787yyt6df6654er6cf838jtyt56583yu8fdf3f06822pppf8331b7e"
    )
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)



    REQUEST_HEADERS = {
        "Content-Type": "application/json",
    }
    GOOGLE_CLIENT_ID = '905099102796-vh9v1cm74cf1j56e71v8o9f3gb6sb24c.apps.googleusercontent.com'
    LOGFILE = "{}/logs/log.log".format(_basedir)
    UPLOAD_FOLDER = "{}/dataupload/".format(_basedir)
    OPENAI_API_KEY = os.environ.get("OPENAIAPIKEY")

    #Sendgrid Data
    SENDGRID_APIKEY = os.environ.get("SENDGRID")
    SENDGRID_APPROVE_EMAIL_TEMP = os.environ.get("SENDGRIDTEMPLATEAPPROVAL")
    SENDGRID_SENDER = os.environ.get("SENDGRIDSENDER")

    #AWS data
    RAW_DOCUMENTS = 'RAW-DOCUMENTS'
    DOCUMENT_EMBEDINGS = 'EMBEDDINGS'

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "06hj822yfdf22y6654er6cf8331b7ee68fd8willb"


class ProductionConfig(Config):
    DEBUG = False
    # JWT
    JWT_PRIVATE_KEY_PATH = "{}/certs/prjpath.pem".format(_basedir)
    JWT_PUBLIC_KEY_PATH = "{}/certs/prjpath.pub".format(_basedir)
    JWT_ALGORITHM = "RS256"
    JWT_PRIVATE_KEY = open(JWT_PRIVATE_KEY_PATH).read()
    JWT_PUBLIC_KEY = open(JWT_PUBLIC_KEY_PATH).read()



configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
