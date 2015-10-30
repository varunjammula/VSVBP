from flask.ext.wtf import Form
from flask import render_template, flash, redirect
from wtforms import StringField, BooleanField, RadioField, widgets, SelectMultipleField
from wtforms.validators import DataRequired




class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class Scanner(Form):
    seed_url = StringField('seed_url', validators=[DataRequired()])
    string_of_files = ['SQL\r\nXSS\r\n']
    list_of_files = string_of_files[0].split()
    files = [(x, x) for x in list_of_files]
    example1 = MultiCheckboxField('Vulnerability Options', choices=files)

