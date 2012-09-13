from .models import Check, db

def run_check(driver, check):
    driver.get(check.url)
    check.screenshot = driver.get_screenshot_as_base64()
    driver.quit()
    check.running = False
    return check

def runner_main(app, url=None):
    from selenium import webdriver
    with app.app_context():
        checks = Check.to_run(lock=True)
        for check in checks:
            driver = webdriver.Remote(
                command_executor=url or app.config.SELENIUM_REMOTE_URL,
                desired_capabilities={
                    'browserName': check.browser_name,
                    'version': check.version,
                    'javascriptEnabled': check.javascript_enabled,
                    'platform': check.platform,
                },
            )
            run_check(driver, check)
            db.session.add(check)
        db.session.commit()
