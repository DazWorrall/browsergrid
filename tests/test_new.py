from .shared import FlaskTestCase
from browsergrid.models import Job

class TestNewJob(FlaskTestCase):

    def test_new_job_creates_job(self):
        resp = self.client.post(
            '/new',
            data = {
                'url': 'http://foo.bar.com',
            },
        )
        job = Job.query.get(1)
        self.assertEqual('http://foo.bar.com', job.url)

    def test_new_job_creates_checksb(self):
        resp = self.client.post(
            '/new',
            data = {
                'url': 'http://foo.bar.com',
                'checks': ['windows-internet explorer-8', u'linux-firefox-2'],
            },
        )
        job = Job.query.get(1)
        checks = list(job.checks)
        self.assertEqual(2, len(checks))
        check1, check2 = checks
        self.assertEqual('windows', check1.platform)
        self.assertEqual('internet explorer', check1.browser_name)
        self.assertEqual('8', check1.version)
        self.assertEqual('linux', check2.platform)
        self.assertEqual('firefox', check2.browser_name)
        self.assertEqual('2', check2.version)

    def test_new_job_redirects_to_result_page(self):
        resp = self.client.post(
            '/new',
            data = {
                'url': 'http://foo.bar.com',
            },
        )
        self.assertRedirects(resp, 'http://localhost/job/1')
