from os.path import dirname, join, abspath

PROJECT_ROOT = abspath(join(dirname(__file__), '..'))

class Settings(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////%s/bg.db' % PROJECT_ROOT
    DEBUG = True
    SECRET_KEY = "\xf3'Q\x10\x01\x81\xcb\xberZ/\x19\x93\xa7\x94\xfe\x9aa\x81\xb6\xb55Z\xe6"
    SITE_TITLE = 'Browser Grid'
    SELENIUM_REMOTE_URL = None
    BROWSER_OPTIONS= {
        'Windows XP': {
            'Internet Explorer': {
                'versions': range(6, 9),
                'browser_name': 'internet explorer',
                'platform_name': 'WINDOWS',
            },
            'Firefox': {
                'versions': range(2, 16),
                'browser_name': 'firefox',
                'platform_name': 'WINDOWS',
            },
            'Opera': {
                'versions': range(9, 13),
                'browser_name': 'opera', 
                'platform_name': 'WINDOWS',
            },
            'Safari': {
                'versions': range(3, 6),
                'browser_name': 'safari',
                'platform_name': 'WINDOWS',
            },
            'Google Chrome': {
                'versions': [],
                'browser_name': 'chrome',
                'platform_name': 'WINDOWS',
            }
        },
        'Windows Vista/7': {
            'Internet Explorer': {
                'versions': [9,],
                'browser_name': 'internet explorer',
                'platform_name': 'VISTA',
            },
        },
        'OSX': {
            'iPhone': {
                'versions': [4.3, 5],
                'browser_name': 'iPhone',
                'platform_name': 'MAC',
            },
            'iPad': {
                'versions': [4.3, 5],
                'browser_name': 'iPad',
                'platform_name': 'MAC',
            },
            'Firefox': {
                'versions': range(2, 16),
                'browser_name': 'firefox',
                'platform_name': 'MAC',
            },
            'Safari': {
                'versions': [5,],
                'browser_name': 'safari',
                'platform_name': 'MAC',
            },
            'Google Chrome': {
                'versions': [],
                'browser_name': 'chrome',
                'platform_name': 'MAC',
            }
        },
        'Linux': {
            'Android': {
                'versions': [4],
                'browser_name': 'android',
                'platform_name': 'LINUX',
            },
            'Firefox': {
                'versions': range(2, 16),
                'browser_name': 'firefox',
                'platform_name': 'LINUX',
            },
            'Google Chrome': {
                'versions': [],
                'browser_name': 'chrome',
                'platform_name': 'LINUX',
            }
            
        },
    }
