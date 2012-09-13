from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(length=255), default='')
    checks = db.relationship('Check', backref='job', lazy='dynamic')

    @classmethod
    def new(cls, url):
        job = cls(url=url)
        db.session.add(job)
        db.session.commit()
        return job

    def add_check(self, browser_name, version, platform, javascript_enabled=True):
        check = Check(
            url = self.url,
            browser_name = browser_name,
            version = version,
            platform = platform,
            javascript_enabled = javascript_enabled,
        )
        self.checks.append(check)
        db.session.add(check)
        return check

    @property
    def status(self):
        '''
        Returns a string detailing the status of this job:
            
            Pending: Job not started
            Running: Job in flight
            Complete: All checks ran
        '''
        checks = list(self.checks)
        if any([c.running for c in checks]):
            return 'Running'
        if all([c.running == False and c.try_count > 0 for c in checks]):
            return 'Complete'
        return 'Pending'


class Check(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    url = db.Column(db.String(length=255), default='')
    browser_name = db.Column(db.String(length=25), default='firefox')
    version = db.Column(db.String(length=25), default='')
    platform = db.Column(db.String(length=25), default='ANY')
    javascript_enabled = db.Column(db.Boolean, default=True)
    screenshot = db.Column(db.Text, nullable=True, default=None)
    running = db.Column(db.Boolean, default=False)
    try_count = db.Column(db.Integer, default=0)
    last_run = db.Column(db.DateTime, nullable=True, default=None)

    @classmethod
    def get_runnable_checks(cls, mark_running=False):
        checks = []
        query = cls.query.filter_by(running=False, try_count=0)
        if mark_running:
            query = query.with_lockmode('update')
            now = datetime.utcnow()
            for c in query:
                c.running = True
                c.last_run = now
                c.try_count += 1
                db.session.add(c)
                checks.append(c)
            db.session.commit()
        else:
            checks = list(query)
        return checks
