from .models import Check, db
from selenium import webdriver

def runner_main(checks, url):
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
                command_executor=url,
                desired_capabilities=desired_capabilities,
            )
            driver.get(check.url)
            check.screenshot = driver.get_screenshot_as_base64()
        except Exception, e:
            print e
        finally:
            check.running = False
            driver.quit()
            db.session.add(check)
            db.session.commit()
