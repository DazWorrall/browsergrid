from flask.ext.wtf import (Form, TextField, TextAreaField, DecimalField, 
                          validators, HiddenField, FileField, SelectField, 
                          BooleanField, ValidationError, PasswordField, RadioField,
                          IntegerField, SelectMultipleField)
from wtforms.fields import Field
from wtforms.widgets import ListWidget, CheckboxInput, TextArea
from flask.ext.wtf.html5 import EmailField, DateField, URLField
from flask import current_app

def create_browser_choices(options):
    choices = []
    for platform, browsers in options.iteritems():
        platform_label = current_app.config['PLATFORM_LABELS'][platform]
        for browser, versions in browsers.iteritems():
            browser_label = current_app.config['BROWSER_LABELS'][browser]
            if versions:
                for v in versions:
                    choices.append((
                        '-'.join([platform, browser, str(v)]),
                        '%s %s on %s' % (browser_label, v, platform_label)
                    ))
            else:
                choices.append((
                    '%s-%s-' % (platform, browser),
                    '%s on %s' % (browser_label, platform_label)
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

class LineBreakListField(Field):
    widget = TextArea()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            text = valuelist[0].replace('\r\n', '\n')
            self.data = [x.strip() for x in text.split('\n')]
        else:
            self.data = []


class NewJobForm(Form):
    title = TextField('Title', [validators.required()])
    notes = TextAreaField('Notes', [validators.optional()])
    checks = MultiCheckboxField('Checks') 
    urls = LineBreakListField('URLs to Check') 
