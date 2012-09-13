from browsergrid.models import db, Check, Job
from browsergrid.runner import runner_main
from .shared import FlaskTestCase
from mock import Mock, patch

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
        self.patcher = patch('browsergrid.runner.webdriver')
        self.webdriver = self.patcher.start()
        self.driver = self.webdriver.Remote.return_value = Mock()
        self.driver.get_screenshot_as_base64.return_value = 'pic'.encode('base64')

    def tearDown(self):
        FlaskTestCase.tearDown(self)
        self.patcher.stop()
        
    def test_run_check_saves_screenshot(self):
        runner_main([self.check], 'http://foo.bar.com')
        self.assertEqual('pic'.encode('base64'), self.check.screenshot)

    def test_runner_exception_handled(self):
        self.driver.get.side_effect = ValueError
        runner_main([self.check], 'http://foo.bar.com')
        self.assertFalse(self.check.running)
        self.assertTrue(self.driver.quit.called)

    def test_runner_reuses_sessions_when_it_can(self):
        check = Check(
            job_id = self.job.id,
            url = self.job.url,
            browser_name = 'firefox',
            version = '15',
            platform = 'ANY',
            try_count = 1,
            running = True,
        )
        db.session.add(check)
        db.session.commit()
        runner_main([self.check, check], 'http://foo.bar.com')
        self.assertEqual(1, self.webdriver.Remote.call_count)
        self.assertEqual(2, self.driver.get.call_count)
        self.assertEqual(1, self.driver.quit.call_count)
