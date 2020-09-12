import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from py2neo import Graph
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import matplotlib
matplotlib.use('Agg')
graph = Graph(password="Dpt@7102")


#
# depth = "1"
# factor = "EQUITY_HELD_BY"
# rel_weight = "0.01"

def related_entities(quant_factors):
    parent_list = []
    related_ent_list = []
    rel_ent_dict = {}
    parent_query = "MATCH (ent:Entity)  WHERE NOT(ent)-[]->() and ()-[]->(ent)  RETURN ent.name as entity"
    parent_query_result = graph.run(parent_query)
    for pq_result in parent_query_result:
        parent_list.append(pq_result['entity'])

    for parent in parent_list:
        for key in quant_factors:
            factor = key
            rel_weight = quant_factors[key][0]
            depth = quant_factors[key][1]
            query = 'match (e),(e1),p=(e)-[r*1..' + depth + ']->(e1) WHERE all (a in relationships(p) where type(a) ="' + factor + '") AND  e1.name ="' + parent + '" AND ALL(r IN relationships(p) WHERE r.weight>=' + rel_weight + ') unwind relationships(p) as rel return e1.name as parent,collect(distinct e.name) AS related_entity'
            result = graph.run(query)
            for item in result.data():
                for value in item['related_entity']:
                    if value not in related_ent_list:
                        related_ent_list.append(value)

        rel_ent_dict[parent] = related_ent_list
        related_ent_list = []
    return rel_ent_dict


def exposure_aggregation(rel_ent_dict):
    import_path = "D:/neo4j/Neo4j app data/neo4jDatabases/database-f655dcf5-9431-494e-b674-f2624aefd98e/installation-4.1.0/import/exposure.csv"
    exposure_data = pd.read_csv(import_path)
    prev_consolidation = ""
    columns = ["Entity", "Exposure"]
    list_nc = []
    list_c = []

    for parent_value in rel_ent_dict:
        exp_amt = 0
        consolidation = ""
        parent_exposure = exposure_data.loc[exposure_data['Entity_Name'] == parent_value, 'Lending_Exposure'].values[0]
        exp_amt = exp_amt + parent_exposure
        consolidation = consolidation + "Parent: " + parent_value
        list_nc.append({'Entity': parent_value, 'Exposure': int(parent_exposure)})
        for child_value in rel_ent_dict[parent_value]:
            individual_exposure = \
                exposure_data.loc[exposure_data['Entity_Name'] == child_value, 'Lending_Exposure'].values[0]
            exp_amt = exp_amt + individual_exposure
            list_nc.append({'Entity': child_value, 'Exposure': int(individual_exposure)})
        list_c.append({'Entity': consolidation, 'Exposure': int(exp_amt)})

    df_nc = pd.DataFrame(list_nc, columns=columns)
    df_c = pd.DataFrame(list_c, columns=columns)
    df_c = df_c[df_c.Exposure != 0]
    return df_c, df_nc


def plot_graph(df_plot, title, filename):
    ax = df_plot.plot.barh(x='Entity', y='Exposure', title=title, rot=0,
                           legend=False)
    for p in ax.patches:
        ax.annotate(str(p.get_width()), (p.get_x() + p.get_width(), p.get_y()), xytext=(5, 10),
                    textcoords='offset points')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.savefig('D:/flask/relation_extraction/graph/project/static/images/' + filename)
    plt.clf()

#
# ax1 = df_c.plot.barh(x='Entity', y='Exposure', title="Counterparty Exposure with aggregation($)", legend=False, rot=0)
# for p in ax1.patches:
#     ax1.annotate(str(p.get_width()), (p.get_x() + p.get_width(), p.get_y()), xytext=(5, 10), textcoords='offset points')
#
# ax1.spines['top'].set_visible(False)
# ax1.spines['right'].set_visible(False)
# ax1.spines['bottom'].set_visible(False)
# ax1.spines['left'].set_visible(False)
#
# plt.show()
#
