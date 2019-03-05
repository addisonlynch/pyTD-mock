import os


class BaseConfig(object):

    PROJECT = 'pyTD-mock'

    # Get app root path, can also use flask.root_path
    # ../../config.py
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    ADMINS = ['ahlshop@gmail.com']
    LOG_FOLDER = os.path.abspath("/var/log")


class DefaultConfig(BaseConfig):
    DEBUG = True

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    DB_URI = 'sqlite:////tmp/account.db'
    BASE_URL = '/v1'
