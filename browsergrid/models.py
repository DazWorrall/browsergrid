from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(length=255), default='')
    results = db.relationship('Result', backref='job', lazy='dynamic')

    @classmethod
    def new(cls, url):
        job = cls(url=url)
        db.session.add(job)
        db.session.commit()
        return job


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    browser_name = db.Column(db.String(length=25), default='firefox')
    version = db.Column(db.String(length=25), default='')
    platform = db.Column(db.String(length=25), default='ANY')
    javascript_enabled = db.Column(db.Boolean, default=True)
