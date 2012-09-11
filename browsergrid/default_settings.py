from os.path import dirname, join, abspath

PROJECT_ROOT = abspath(join(dirname(__file__), '..'))

class Settings(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////%s/bg.db' % PROJECT_ROOT
    DEBUG = True
    SECRET_KEY = "\xf3'Q\x10\x01\x81\xcb\xberZ/\x19\x93\xa7\x94\xfe\x9aa\x81\xb6\xb55Z\xe6"
    SITE_TITLE = 'Browser Grid'
