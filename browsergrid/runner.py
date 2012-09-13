from .models import Check, db
from selenium import webdriver
from itertools import groupby

def grouper(check): 
    return check.platform, check.browser_name, check.version

def runner_main(check_list, url):
    for ((platform, browser_name, version), checks) in groupby(check_list, grouper):
        desired_capabilities={
            'browserName': browser_name.lower(),
            'version': version,
            'javascriptEnabled': True,
            'platform': platform.upper(),
            'max-duration': 90,
        }
        driver = webdriver.Remote(
            command_executor=url,
            desired_capabilities=desired_capabilities,
        )
        for check in checks:
            try:
                driver.get(check.url)
                check.screenshot = driver.get_screenshot_as_base64()
            except Exception, e:
                print e
            finally:
                check.running = False
                db.session.add(check)
        db.session.commit()
        driver.quit()
