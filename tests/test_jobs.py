from browsergrid.models import db, Check, Job
from .shared import FlaskTestCase
from datetime import datetime

class TestJobStatus(FlaskTestCase):

    def setUp(self):
        FlaskTestCase.setUp(self)
        self.job = Job.new('http://goo.com')
        self.check = self.job.add_check(
            url = 'http://foo.com',
            browser_name = 'firefox',
            version = '15',
            platform = 'ANY',
        )
        db.session.add(self.job)
        db.session.add(self.check)
        db.session.commit()

    def test_no_running_jobs(self):
        self.assertEqual('Pending', self.job.status)

    def test_running_jobs(self):
        self.check.running = True
        self.assertEqual('Running', self.job.status)

    def test_finished_jobs(self):
        self.check.try_count = 1
        self.assertEqual('Complete', self.job.status)
