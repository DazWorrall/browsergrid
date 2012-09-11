#!/usr/bin/env python
from __future__ import with_statement
from .models import db, Job
from flask import (Flask, request, session, g, redirect, url_for, abort,
     render_template, flash, Blueprint)
from .default_settings import Settings
from .forms import NewJobForm

bg = Blueprint('bg', __name__)

def create_app(conf_obj=Settings, envvar='BG_SETTINGS'):
    app = Flask(__name__)
    app.config.from_object(conf_obj)
    app.config.from_envvar(envvar, silent=True)
    db.init_app(app)
    app.register_blueprint(bg)
    return app

def init_db(app):
    """Creates the database tables."""
    with app.app_context():
        db.create_all()

@bg.route('/')
def index():
    return render_template('index.html')

@bg.route('/new', methods=['GET', 'POST'])
def new():
    form = NewJobForm()
    if form.validate_on_submit():
        job = Job.new(url=form.url.data)
        return redirect(url_for('.job_detail', _id = job.id))
    print form.errors
    return render_template('new.html', form=form)

@bg.route('/job/<_id>')
def job_detail(_id):
    pass

app = create_app()

if __name__=="__main__":
    app.run()
