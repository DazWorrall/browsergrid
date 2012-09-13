from browsergrid.models import db, Check, Job
from .shared import FlaskTestCase
from datetime import datetime

class TestToRun(FlaskTestCase):

    def setUp(self):
        FlaskTestCase.setUp(self)
        self.job = Job.new('http://goo.com')
        self.ran_once = Check(
            job_id = self.job.id,
            url = self.job.url,
            browser_name = 'firefox',
            version = '15',
            platform = 'ANY',
            screenshot = 'ANIMAGE'.encode('base64'),
            try_count = 1,
        )
        self.not_ran = Check(
            job_id = self.job.id,
            url = self.job.url,
            browser_name = 'firefox',
            version = '15',
            platform = 'ANY',
            try_count = 0,
        )
        self.in_flight = Check(
            job_id = self.job.id,
            url = self.job.url,
            browser_name = 'firefox',
            version = '15',
            platform = 'ANY',
            try_count = 1,
            running = True,
            last_run = datetime.now(),
        )
        for c in [self.ran_once, self.not_ran, self.in_flight]:
            db.session.add(c)
        db.session.commit()

    def test_basic_to_run(self):
        self.assertEqual([self.not_ran], list(Check.to_run()))

    def test_to_run_lock(self):
        self.assertEqual([self.not_ran], list(Check.to_run(lock=True)))
        self.assertEqual([], list(Check.to_run(lock=True)))
        self.assertTrue(self.not_ran.running)
        self.assertEqual(1, self.not_ran.try_count)
        self.assertIsInstance(self.not_ran.last_run, datetime)