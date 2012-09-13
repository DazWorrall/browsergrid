from os.path import dirname, join, abspath

PROJECT_ROOT = abspath(join(dirname(__file__), '..'))

class Settings(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////%s/bg.db' % PROJECT_ROOT
    DEBUG = True
    SECRET_KEY = "\xf3'Q\x10\x01\x81\xcb\xberZ/\x19\x93\xa7\x94\xfe\x9aa\x81\xb6\xb55Z\xe6"
    SITE_TITLE = 'Browser Grid'
    SELENIUM_REMOTE_URL = None
    BROWSER_OPTIONS= {
        'windows': {
            'label': 'Windows XP/2003',
            'browsers': {
                'internet explorer': {
                    'versions': range(6, 9),
                    'label': 'Internet Explorer',
                },
                'firefox': {
                    'versions': range(2, 16),
                    'label': 'Firefox',
                },
                'opera': {
                    'versions': range(9, 13),
                    'label': 'Opera', 
                },
                'safari': {
                    'versions': range(3, 6),
                    'label': 'Safari',
                },
                'chrome': {
                    'versions': [],
                    'label': 'Chrome',
                },
            },
        },
        'vista': {
            'label': 'Windows Vista/7',
            'browsers': {
                'internet explorer': {
                    'versions': [9,],
                    'label': 'Internet Explorer',
                },
            },
        },
        'mac': {
            'label': 'OSX',
            'browsers': {
                'iphone': {
                    'versions': [4.3, 5],
                    'label': 'iPhone',
                },
                'ipad': {
                    'versions': [4.3, 5],
                    'label': 'iPad',
                },
                'firefox': {
                    'versions': range(2, 16),
                    'label': 'Firefox',
                },
                'safari': {
                    'versions': [5,],
                    'label': 'Safari',
                },
                'chrome': {
                    'versions': [],
                    'label': 'Chrome',
                }
            },
        },
        'linux': {
            'label': 'Linux',
            'browsers': {
                'android': {
                    'versions': [4],
                    'label': 'Android',
                },
                'firefox': {
                    'versions': range(2, 16),
                    'label': 'Firefox',
                },
                'chrome': {
                    'versions': [],
                    'label': 'Chrome',
                },
            },
        },
    }
