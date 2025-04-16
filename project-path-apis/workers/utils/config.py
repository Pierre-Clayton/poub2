from __future__ import absolute_import

import os
from dotenv import load_dotenv

load_dotenv("utils/.env")


class BaseConfig:

    DEBUG = True
    # GCP
    BUCKET_NAME = 'projectpath-projects-bucket'
    RAW_FOLDER_NAME = 'RAW-DOCUMENTS'
    EXTRACTED_FOLDER_NAME = 'EMBEDDINGS'

    # Base URL
    APP_BASE_URL = os.environ.get("APPBASEURL")
    DHOST = os.environ.get("DHOST")
    DPORT = os.environ.get("DPORT")
    DBASE = os.environ.get("DBASE")
    DUSER = os.environ.get("DUSER")
    DPASS = os.environ.get("DPASS")

    # Redis configs
    REDIS_PASSWORD = os.environ.get("REDISPASSWORD")
    REDIS_HOST = os.environ.get("REDISHOST")
    REDIS_PORT = os.environ.get("REDISPORT")
    REDIS_DATABASE = os.environ.get("REDISDATABASE")

    # Celery configs
    CELERY_BROKER_URL = "redis://:{0}@{1}:{2}/{3}".format(
        REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, REDIS_DATABASE)
    CELERY_RESULT_BACKEND = "redis://:{0}@{1}:{2}/{3}".format(
        REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, REDIS_DATABASE)
    CELERY_TASK_RESULT_EXPIRES = 3600  # 1 hour
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Africa/Nairobi'
    REQUEST_HEADERS = {"Accept": "application/json"}
    TEMP_DOC_FOLDER = 'tempfold'

    #AWS
    AWS_ACCESS_KEY = os.environ.get("AWSSERVERPUBLICKEY")
    AWS_SECRET_KEY = os.environ.get("AWSSERVERSECRETKEY")

    
 
