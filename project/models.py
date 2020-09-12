from project import db
from flask_table import Table, Col, LinkCol

class ruleEngine(db.Model):
    __tablename__ = 'rule_table'
    id = db.Column(db.Integer, primary_key=True)

    rule_name = db.Column(db.String(80))
    factor_name = db.Column(db.String(80))
    tolerance = db.Column(db.Float(10))
    inc = db.Column(db.String(10))
    depth = db.Column(db.Integer())

    def __init__(self,rule_name,factor_name,tolerance,inc,depth):
        self.rule_name = rule_name
        self.factor_name = factor_name
        self.tolerance = tolerance
        self.inc = inc
        self.depth = depth


class Results(Table):
        table_id = 'list_table'
        classes = ['table-bordered']
        id = Col('id',show=False)
        rule_name = Col('Rule Name')
        factor_name = Col('Factor Name')
        tolerance = Col('Tolerance')
        inc = Col('Include')
        depth = Col('Depth')
        edit = LinkCol('Edit', 'rules_engine.edit', url_kwargs=dict(id='id'))




