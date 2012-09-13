from browsergrid.models import db, Check, Job
from browsergrid.runner import run_check
from .shared import FlaskTestCase
from mock import Mock

class TestRunCheck(FlaskTestCase):

    def setUp(self):
        FlaskTestCase.setUp(self)
        self.job = Job.new('http://goo.com')
        self.check = Check(
            job_id = self.job.id,
            url = self.job.url,
            browser_name = 'firefox',
            version = '15',
            platform = 'ANY',
            try_count = 1,
            running = True,
        )
        db.session.add(self.check)
        db.session.commit()
        self.driver = Mock()
        self.driver.get_screenshot_as_base64.return_value = 'pic'.encode('base64')

    def test_run_check_saves_screenshot(self):
        run_check(self.driver, self.check)
        self.assertEqual('pic'.encode('base64'), self.check.screenshot)

    def test_run_check_sets_correct_flags(self):
        run_check(self.driver, self.check)
        self.assertFalse(self.check.running)
        self.assertTrue(self.driver.quit.called)
