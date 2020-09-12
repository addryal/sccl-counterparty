from flask_wtf import Form
from wtforms import StringField,SubmitField,BooleanField,IntegerField,DecimalField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email


class rule_upload(Form):
    rule_class = StringField('Rule Engine Name', validators=[DataRequired()])
    submit = SubmitField('Save Ruleset ')
    vote_include = BooleanField()
    vote_depth = IntegerField()
    vote_tolerance = DecimalField()
    equity_include = BooleanField()
    equity_depth = IntegerField()
    equity_tolerance = DecimalField()
    revenue_include = BooleanField()
    revenue_depth = IntegerField()
    revenue_tolerance = DecimalField()
    exp_include = BooleanField()
    exp_depth = IntegerField()
    exp_tolerance = DecimalField()
    prod_include = BooleanField()
    prod_depth = IntegerField()
    prod_tolerance = DecimalField()

    distress_include =  BooleanField()
    credit_include = BooleanField()
    influence_include = BooleanField()

class rule_display(Form):
    rule_engine = StringField('Rule Engine Name')


