from flask.ext.sqlalchemy import SQLAlchemy

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
            browser_name = browser_name,
            version = version,
            platform = platform,
            javascript_enabled = javascript_enabled,
        )
        self.checks.append(check)
        db.session.add(check)
        db.session.commit()


class Check(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    browser_name = db.Column(db.String(length=25), default='firefox')
    version = db.Column(db.String(length=25), default='')
    platform = db.Column(db.String(length=25), default='ANY')
    javascript_enabled = db.Column(db.Boolean, default=True)

    @classmethod
    def new(cls, url):
        job = cls(url=url)
        db.session.add(job)
        db.session.commit()
        return job
