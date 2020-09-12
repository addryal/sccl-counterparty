from flask import Blueprint,render_template,redirect,url_for,request,flash
from project.rules_engine.forms import rule_upload,rule_display
from project.models import ruleEngine,Results
from project import db
from project.graph_extract import related_entities,exposure_aggregation,plot_graph



# Registering Blueprints
rules_blueprint = Blueprint('rules_engine',__name__,template_folder='templates/rules_engine')

@rules_blueprint.route('/add_rule',methods=['GET', 'POST'])
def add_rule():
    form = rule_upload()
    if request.method == 'POST':
        name = form.rule_class.data
        v_depth = form.vote_depth.data
        rule_vote = ruleEngine(name,"VOTING_HELD_BY",form.vote_tolerance.data,form.vote_include.data,form.vote_depth.data)
        rule_equity = ruleEngine(name, "EQUITY_HELD_BY", form.equity_tolerance.data, form.equity_include.data, form.equity_depth.data)
        rule_revenue = ruleEngine(name, "REVENUE_DEPENDENCE", form.revenue_tolerance.data, form.revenue_include.data, form.revenue_depth.data)
        rule_exp = ruleEngine(name, "CREDIT_GUARANTEE_BY", form.exp_tolerance.data, form.exp_include.data, form.exp_depth.data)
        rule_prod = ruleEngine(name, "PRODUCTION_DEPENDENCE", form.prod_tolerance.data, form.prod_include.data, form.prod_depth.data)
        rule_distress = ruleEngine(name, "DISTRESS_CONTAGION",1 , form.distress_include.data,1 )
        rule_credit = ruleEngine(name, "CREDIT_GUARANTEE_BY", 1, form.credit_include.data, 1)
        rule_influence = ruleEngine(name, "SIGNIFICANT_INFLUENCE", 1, form.influence_include.data, 1)

        rule = ruleEngine(name, "credit", form.vote_tolerance.data, form.vote_include.data, form.vote_depth.data)
        # rule = ruleEngine(name, "influence", form.vote_tolerance.data, form.vote_include.data, form.vote_depth.data)
        db.session.add(rule_vote)
        db.session.add(rule_equity)
        db.session.add(rule_revenue)
        db.session.add(rule_exp)
        db.session.add(rule_prod)
        db.session.add(rule_distress)
        db.session.add(rule_credit)
        db.session.add(rule_influence)

        db.session.commit()
        return render_template('add_confirmation.html')




    return render_template('add_rule.html',form=form)



@rules_blueprint.route('/view_rule')
def view_rule():
    rules = ruleEngine.query.all()
    #rules = ruleEngine.query.filter_by(inc='true')
    if not rules:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = Results(rules)
        table.border = True
        return render_template('view_rule.html', table=table)



@rules_blueprint.route('/run_aggregation',methods=['GET', 'POST'])
def run_agg():
    rule_engine_list = []
    for value in db.session.query(ruleEngine.rule_name).distinct():
        rule_engine_list.append(value[0])

    if request.method == 'POST':
        selected_rule = request.form['rule_value']

        factor_dict = {}
        rules_cp = db.session.query(ruleEngine.factor_name,ruleEngine.tolerance,ruleEngine.depth).filter_by(rule_name=selected_rule,inc='true').all()
        for item_val in rules_cp:
            factor_dict[item_val[0]] = [str(item_val[1]), str(item_val[2])]

        related_ent_list = related_entities(factor_dict)
        consol_df,sa_df = exposure_aggregation(related_ent_list)
        rel_ent_display = list(related_ent_list.items())
        # Generating consolidated graph
        title ="Consolidated exposure($)"
        filename = "Cpty_consol.png"
        plot_graph(consol_df, title, filename)

        # Generating standalone exposure
        title = "Standalone exposure($)"
        filename = "Cpty_sa.png"
        plot_graph(sa_df, title, filename)

        if not rules_cp:
            flash('No results found!')
            return redirect('/')
        else:
            # display results
            return render_template('agg_view.html', consol_url='/static/images/Cpty_consol.png' ,sa_url='/static/images/Cpty_sa.png',rel_entity=rel_ent_display)
    return render_template('rule_select.html', rule_engine_list=rule_engine_list)


@rules_blueprint.route('/modify/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db.session.query(ruleEngine.rule_name,ruleEngine.factor_name, ruleEngine.tolerance, ruleEngine.depth,ruleEngine.inc ).filter_by(id=id).first()
    rule_mod = ruleEngine.query.filter_by(id=id).first()
    if request.method == 'POST':
        new_tolerance = request.form['tolerance']
        new_depth = request.form['depth']
        new_include = request.form['include']
        rule_mod.depth = new_depth
        rule_mod.tolerance = new_tolerance
        rule_mod.inc = new_include
        db.session.commit()
        return render_template('add_confirmation.html')




    return render_template('edit_rule.html',result=qry,rule_engine=qry[0],factor=qry[1],tolerance=qry[2],depth=qry[3],include=1)



# @rules_blueprint.route('/modify/<str:rule_name>', methods=['GET', 'POST'])
# def edit(rule_name):
#     qry = db.session.query(ruleEngine).filter(ruleEngine.rule_name==rule_name).first()
#     result_set = qry.first()
#
#     if result_set:
#         form = rule_upload(formdata=request.form, obj=result_set)
#         if request.method == 'POST' and form.validate():
#             rule_vote = ruleEngine(rule_name, "VOTING_HELD_BY", form.vote_tolerance.data, form.vote_include.data,form.vote_depth.data)
#
#             # save edits
#             return redirect('/')
#         return render_template('edit_album.html', form=form)
#     else:
#         return 'Error loading #{id}'.format(id=id)
