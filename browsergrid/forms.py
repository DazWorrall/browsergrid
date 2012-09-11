from flask.ext.wtf import (Form, TextField, TextAreaField, DecimalField, 
                          validators, HiddenField, FileField, SelectField, 
                          BooleanField, ValidationError, PasswordField, RadioField,
                          IntegerField)
from wtforms.fields import Field
from wtforms.widgets import TextInput
from flask.ext.wtf.html5 import EmailField, DateField, URLField

class NewJobForm(Form):
    url = URLField('Username', [validators.Required('URL is required')])
