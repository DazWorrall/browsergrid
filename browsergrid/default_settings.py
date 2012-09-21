from os.path import dirname, join, abspath
from werkzeug.datastructures import OrderedMultiDict

PROJECT_ROOT = abspath(join(dirname(__file__), '..'))

class Settings(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////%s/bg.db' % PROJECT_ROOT
    DEBUG = True
    SECRET_KEY = "\xf3'Q\x10\x01\x81\xcb\xberZ/\x19\x93\xa7\x94\xfe\x9aa\x81\xb6\xb55Z\xe6"
    SITE_TITLE = 'Browser Grid'
    SELENIUM_REMOTE_URL = None
    RECENT_JOBS_COUNT = 5
    SS_ROOT = '/tmp' # Where screenshots are saved
    PLATFORM_LABELS = {
        'windows': 'Windows XP/2003',
        'vista': 'Windows Vista/7/2008',
        'linux': 'Linux',
        'mac': 'OSX',
        'any': 'Anything',
    }
    BROWSER_LABELS = {
        'internet explorer': 'Internet Explorer',
        'chrome': 'Google Chrome',
        'opera' : 'Opera',
        'firefox': 'Firefox',
        'safari': 'Safari',
        'iphone': 'iPhone',
        'ipad': 'iPad',
        'android': 'Android',
    }
    BROWSER_OPTIONS= OrderedMultiDict({
        'windows': {
            'internet explorer': range(6, 9),
            'firefox': range(2, 16),
            'opera': range(9, 13),
            'safari': range(3, 6),
            'chrome': [],
        },
        'vista': {
            'internet explorer': [9,],
        },
        'mac': {
            'iphone': [4.3, 5],
            'ipad': [4.3, 5],
            'firefox': range(2, 15),
            'safari': [5,],
            'chrome': [],
        },
        'linux': {
            'android': [4],
            'firefox': range(2, 16),
            'chrome': [],
        },
    })
