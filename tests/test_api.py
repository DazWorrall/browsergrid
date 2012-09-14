from .shared import FlaskTestCase
from browsergrid.models import Job, Check, db
import json

class TestGet(FlaskTestCase):

    def setUp(self):
        FlaskTestCase.setUp(self)
        self.job = Job.new(
            title = 'Test Job',
        )
        self.check = self.job.add_check(
            url = 'http://www.foo.com',
            browser_name = 'firefox',
            platform = 'windows',
            version = '1',
        )
        db.session.commit()

    def test_get_labels(self):
        browser = self.client.get('/api/browser_labels')
        platform = self.client.get('/api/platform_labels')
        self.assertEqual(
            self.app.config['BROWSER_LABELS'],
            json.loads(browser.data),
        )
        self.assertEqual(
            self.app.config['PLATFORM_LABELS'],
            json.loads(platform.data),
        )

    def test_get_check(self):
        resp = self.client.get('/api/check/%d' % self.check.id)
        self.assert200(resp)
        self.assertEqual(
            {
                'id': self.check.id,
                'browser_name': 'firefox',
                'browser_label': self.app.config['BROWSER_LABELS']['firefox'],
                'version': '1',
                'platform': 'windows',
                'platform_label': self.app.config['PLATFORM_LABELS']['windows'],
                'status': 'pending',
            },
            json.loads(resp.data),
        )
