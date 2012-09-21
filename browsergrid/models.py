from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=255), default='')
    notes = db.Column(db.Text, default='')
    checks = db.relationship('Check', backref='job', lazy='dynamic')

    @classmethod
    def new(cls, title, notes=''):
        job = cls(title=title, notes=notes)
        db.session.add(job)
        db.session.commit()
        return job

    def add_check(self, url, browser_name, version, platform, javascript_enabled=True):
        check = Check(
            url = url,
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
    platform = db.Column(db.String(length=25), default='ANY')
    browser_name = db.Column(db.String(length=25), default='firefox')
    version = db.Column(db.String(length=25), default='')
    javascript_enabled = db.Column(db.Boolean, default=True)
    filename = db.Column(db.String(50), nullable=True, default=lambda: str(uuid4()) + '.png')
    running = db.Column(db.Boolean, default=False)
    try_count = db.Column(db.Integer, default=0)
    last_run = db.Column(db.DateTime, nullable=True, default=None)

    @classmethod
    def get_runnable_checks(cls, mark_running=False):
        checks = []
        query = cls.query.filter_by(running=False, try_count=0)
        for field in [cls.platform, cls.browser_name, cls.version]:
            query = query.order_by(field)
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
