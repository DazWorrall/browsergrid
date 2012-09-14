from .shared import FlaskTestCase
from browsergrid.models import Job, Check, db
import json

class TestGet(FlaskTestCase):

    def setUp(self):
        FlaskTestCase.setUp(self)
        self.job = Job.new(
            url = 'http://www.foo.com',
        )
        self.check = self.job.add_check(
            browser_name = 'firefox',
            platform = 'windows',
            version = '1',
        )
        db.session.commit()

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
