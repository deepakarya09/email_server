import os
import logging
from logging.handlers import TimedRotatingFileHandler
from re import TEMPLATE

if not os.path.exists("log/"):
    os.makedirs("log")

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s  %(name)s %(threadName)s :- %(message)s")

handler = TimedRotatingFileHandler(
    'log/app.log', when="midnight", interval=1, encoding='utf8')

handler.suffix = "%Y-%m-%d_%H-%M-%S"
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False

PAGE = 1
LIMIT = 10
DEFAULT_COUNTRY = "US"
MIN_SUB_ARTICLE_COUNT = 5
MIN_DEC_LENGTH = 20
MIN_TAG_LENGTH = 2
MIN_TITLE_LENGTH = 5
bucket_base_url = "https://storage.googleapis.com/cur-prod-email/"
img_base_width = 680
img_base_height = 680
BUCKET_NAME = "cur-prod-email"
remote_image_page_directory = "Images/"  # with /
LOGO = "Logo/"
THUMBNAIL = "Thumbnail/"
CLIENT_ID_PRODUCTION = "436819105815-pns2vtis52sbnilbt1fsgj7psl5ujtk3.apps.googleusercontent.com"
CLIENT_ID_DEVELOPMENT = "240891439748-8sqgqfurlmg3v9d97hk5smtjeqh54v2i.apps.googleusercontent.com"
DOMAIN_NAME = ".nmedia2.com"
EMAIL_INVITATION = "https://nmedia2.com/new/user/"
EMAIL_VERIFICATION_DOMAIN = "https://nmedia2.com/confirm-email/"
HTML_GCP_REMOTE_FOLDER = "page"
TEMPLATE = 'templates'

class DevelopmentConfig(Config):
    """
    Development Configuration
    """
    TESTING = True
    DEBUG = True
    ENV = 'development'
    DATABASE_USER = 'postgres'
    DATABASE_NAME = 'email_subs'
    DATABASE_PASSWORD = '3366'
    DATABASE_URI = '127.0.0.1'
    DATABASE_PORT = 5432
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_URI}:{DATABASE_PORT}/{DATABASE_NAME}"


class TestingConfig(Config):
    """
    Development Configuration
    """
    TESTING = True
    DEBUG = True
    ENV = 'development'
    DATABASE_USER = 'postgres'
    DATABASE_NAME = 'email_subs'
    DATABASE_PASSWORD = '3366'
    DATABASE_URI = '127.0.0.1'
    DATABASE_PORT = 5432
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = "app.log"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_URI}:{DATABASE_PORT}/{DATABASE_NAME}"


class ProductionConfig(Config):
    """
    Production Environment Config FIle Configuration
    Environment Required Variable:
        variable         :     operation                 :      example
    ==================================================================================================================
        DATABASE_USER    : export user name              :       "root"
        DATABASE_NAME    : export name                   :       "mydb"
        DATABASE_PASSWORD: export DATABASE_USER password :       "xyz"
        DATABASE_URI     : export databse URI            :       IP Address
        DATABASE_PORT    : export port                   :       "5432"
    ==================================================================================================================
    """
    TESTING = False
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_USER = os.environ.get("DATABASE_USER")
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    DATABASE_URI = os.environ.get("DATABASE_URI")
    DATABASE_PORT = os.environ.get("DATABASE_PORT")
    LOG_FILE = "app.log"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_URI}:{DATABASE_PORT}/{DATABASE_NAME}"


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
