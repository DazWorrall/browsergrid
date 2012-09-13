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

    def tearDown(self):
        FlaskTestCase.tearDown(self)
        self.patcher.stop()
        
    def test_run_check_saves_screenshot(self):
        self.driver.get_screenshot_as_base64.return_value = 'pic'.encode('base64')
        runner_main([self.check], 'http://foo.bar.com')
        self.assertEqual('pic'.encode('base64'), self.check.screenshot)
