from .shared import FlaskTestCase
from browsergrid.models import Job, db

class TestNewJob(FlaskTestCase):

    def test_new_job_creates_job(self):
        resp = self.client.post(
            '/new',
            data = {
                'title': 'My Test',
            },
        )
        job = Job.query.get(1)
        self.assertEqual('My Test', job.title)

    def test_new_job_creates_checksb(self):
        resp = self.client.post(
            '/new',
            data = {
                'title': 'My check',
                'checks': [u'linux-firefox-2'],
                'urls': 'http://foo.com\nhttp://bar.com',
            },
        )
        job = Job.query.get(1)
        checks = list(job.checks)
        self.assertEqual(2, len(checks))
        for check in checks:
            self.assertEqual('linux', check.platform)
            self.assertEqual('firefox', check.browser_name)
            self.assertEqual('2', check.version)
        self.assertEqual('http://foo.com', checks[0].url)
        self.assertEqual('http://bar.com', checks[1].url)

    def test_new_job_redirects_to_result_page(self):
        resp = self.client.post(
            '/new',
            data = {
                'title': 'My check',
            },
        )
        self.assertRedirects(resp, 'http://localhost/job/1')


class TestFetchScreenshot(FlaskTestCase):

    def setUp(self):
        FlaskTestCase.setUp(self) 
        self.job = Job.new('http://foobar.com')
        self.check = self.job.add_check(
            url = 'http://foo.bar.com',
            browser_name = 'firefox',
            version = '15',
            platform = 'any',
        )
        self.check.screenshot = 'TEST'.encode('base64')
        db.session.add(self.check)
        db.session.commit()
    
    def test_screenshot_served_correctly(self):
        resp = self.client.get('/screenshot/%d' % self.check.id)
        self.assert200(resp)
        self.assertEqual('TEST', resp.data)
        self.assertEqual('image/png', resp.headers.get('Content-Type'))
