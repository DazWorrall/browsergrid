from .models import Check, db
from selenium import webdriver
from itertools import groupby
from os import path

def grouper(check): 
    return check.platform, check.browser_name, check.version

def runner_main(check_list, url, ss_path):
    for ((platform, browser_name, version), checks) in groupby(check_list, grouper):
        checks = list(checks)
        driver = None
        desired_capabilities={
            'browserName': browser_name.lower(),
            'version': version,
            'javascriptEnabled': True,
            'platform': platform.upper(),
            'max-duration': 90,
        }
        try:
            driver = webdriver.Remote(
                command_executor=url,
                desired_capabilities=desired_capabilities,
            )
            for check in checks:
                try:
                    driver.get(check.url)
                    with open(path.join(ss_path, check.filename), 'w') as f:
                        f.write(driver.get_screenshot_as_base64().decode('base64'))
                except Exception, e:
                    print e
                    continue
        except Exception, e:    
            print e
            continue
        finally:
            for check in checks:
                check.running = False
                db.session.add(check)
            db.session.commit()
            if driver:
                driver.quit()
