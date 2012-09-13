from .models import Check, db

def run_check(driver, check):
    driver.get(check.url)
    check.screenshot = driver.get_screenshot_as_base64()
    driver.quit()
    check.running = False
    return check

def runner_main(app):
    with app.app_context():
        checks = Check.to_run(lock=True)
        for c in checks:
            run_check(c)
            db.session.add(c)
        db.session.commit()
