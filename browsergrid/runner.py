from .models import Check, db

def run_check(driver, check):
    driver.get(check.url)
    check.screenshot = driver.get_screenshot_as_base64()
    return check

def runner_main(app, url=None):
    from selenium import webdriver
    with app.app_context():
        checks = Check.to_run(lock=True)
        for check in checks:
            desired_capabilities={
                'browserName': check.browser_name.lower(),
                'version': check.version,
                'javascriptEnabled': check.javascript_enabled,
                'platform': check.platform.upper(),
                'max-duration': 90,
            }
            try:
                driver = webdriver.Remote(
                    command_executor=url or app.config.SELENIUM_REMOTE_URL,
                    desired_capabilities=desired_capabilities,
                )
                run_check(driver, check)
            except Exception, e:
                print e
            finally:
                check.running = False
                driver.quit()
                db.session.add(check)
                db.session.commit()
