from .shared import FlaskTestCase
from browsergrid.models import Job, db
from shutil import rmtree
import tempfile
from uuid import uuid4
from os import path

class TestNewJob(FlaskTestCase):

    def test_new_job_creates_job(self):
        resp = self.client.post(
            '/new',
            data = {
                'title': 'My Test',
                'urls': 'http://foo.com\nhttp://bar.com',
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
                'urls': 'http://foo.com\nhttp://bar.com',
            },
        )
        self.assertRedirects(resp, 'http://localhost/job/1')


class TestFetchScreenshot(FlaskTestCase):

    def setUp(self):
        FlaskTestCase.setUp(self) 
        self.tempdir = tempfile.mkdtemp()
        self.app.config['SS_ROOT'] = self.tempdir

    def tearDown(self):
        FlaskTestCase.tearDown(self) 
        rmtree(self.tempdir)
    
    def test_screenshot_served_correctly(self):
        fname = str(uuid4()) + '.png'
        with open(path.join(self.tempdir, fname), 'w') as f:
            f.write('HELLO!')
        resp = self.client.get('/screenshot/%s' % fname)
        self.assert200(resp)
        self.assertEqual('HELLO!', resp.data)
        self.assertEqual('image/png', resp.headers.get('Content-Type'))
    
    def test_screenshot_404s_with_bad_filename(self):
        resp = self.client.get('/screenshot/fdsfdsafdsfad')
        self.assert404(resp)
