from browsergrid.default_settings import Settings
from browsergrid.app import create_app
from browsergrid.models import db
import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

class TestSettings(Settings):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
    DEBUG = True
    CSRF_ENABLED = False

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestSettings)
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()
        self.app.app_context().push()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def assertRedirects(self, response, location, code=302):
        """
        Checks if response is an HTTP redirect to the 
        given location.
        """
        self.assertStatus(response, code)
        self.assertEqual(
            location,
            response.location,
        )

    def assertStatus(self, response, status_code):
        """
        Helper method to check matching response status.
        """
        self.assertEqual(
            status_code,
            response.status_code, 
            'Expected status code %d, got %s' % (status_code, response.status_code)
        )

    def assert200(self, response):
        self.assertStatus(response, 200)

    def assert400(self, response):
        self.assertStatus(response, 400)

    def assert403(self, response):
        self.assertStatus(response, 403)

    def assert404(self, response):
        self.assertStatus(response, 404)
