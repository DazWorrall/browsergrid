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

    def test_new_job_redirects_to_result_page(self):
        resp = self.client.post(
            '/new',
            data = {
                'url': 'http://foo.bar.com',
            },
        )
        self.assertRedirects(resp, 'http://localhost/job/1')
