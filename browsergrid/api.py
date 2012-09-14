from flask import Blueprint, jsonify, current_app
from .models import db, Job, Check

api = Blueprint('api', __name__)

def check_to_json(check):
    return {
        'id': check.id,
        'browser_name': check.browser_name,
        'browser_label': current_app.config['BROWSER_LABELS'][check.browser_name],
        'version': check.version,
        'platform': check.platform,
        'platform_label': current_app.config['PLATFORM_LABELS'][check.platform],
        'status': 'pending',
    }

@api.route('/browser_labels')
def get_browser_labels():
    return jsonify(current_app.config['BROWSER_LABELS'])

@api.route('/platform_labels')
def get_platform_labels():
    return jsonify(current_app.config['PLATFORM_LABELS'])

@api.route('/check/<int:check_id>')
def get_check(check_id):
    check = Check.query.get_or_404(check_id)
    return jsonify(check_to_json(check))
