from flask.ext.wtf import (Form, TextField, TextAreaField, DecimalField, 
                          validators, HiddenField, FileField, SelectField, 
                          BooleanField, ValidationError, PasswordField, RadioField,
                          IntegerField, SelectMultipleField)
from wtforms.fields import Field
from wtforms.widgets import ListWidget, CheckboxInput
from flask.ext.wtf.html5 import EmailField, DateField, URLField

def create_browser_choices(options):
    choices = []
    for platform, browsers in options.iteritems():
        for browser, data in browsers.iteritems():
            if data.get('versions'):
                for v in data['versions']:
                    choices.append((
                        '-'.join([data['platform_name'].lower(), data['browser_name'].lower(), str(v)]),
                        '%s %s on %s' % (browser, v, platform)
                    ))
            else:
                choices.append((
                    '%s-%s-' % (data['platform_name'].lower(), data['browser_name'].lower()),
                    '%s on %s' % (browser, platform)
                ))
    return choices

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class NewJobForm(Form):
    url = URLField('Username', [validators.Required('URL is required')])
    checks = MultiCheckboxField('Checks') 
