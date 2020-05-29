import cx_Oracle
import chart_studio
import re
import plotly.graph_objects as go
import chart_studio.plotly as py
import chart_studio.dashboard_objs as dash

username = "Lab_2"                                      
password = "query"                                                                                      
database = "localhost/xe"

connection = cx_Oracle.connect(username, password, database)
cursor = connection.cursor()

generation1 = []
quantity = []
query1 = """
    SELECT GEN_NUM, MAX_POKEMON_NUM - MIN_POKEMON_NUM + 1 AS QUANTITY FROM GENERATIONS
"""
cursor.execute(query1)

for row in cursor.fetchall():
    generation1.append (row[0])
    quantity.append(row[1])
bar = go.Bar (x = generation1 , y = quantity)
bar = py.plot([bar], auto_open = True, file_name = "Plot1")


p_type = []
percentage = []
query2 = """
    SELECT P_TYPES.P_TYPE, ROUND(count(*) / (SELECT count(*) FROM POKEMONS ), 4 ) AS PERCENTAGE
    FROM P_TYPES
    JOIN POKEMONS
    ON POKEMONS.TYPE_1 = P_TYPES.P_TYPE
    GROUP BY P_TYPE
"""
cursor.execute(query2)

for row in cursor.fetchall():
    p_type.append (row[0])
    percentage.append(row[1])
pie = go.Pie (labels = p_type, values = percentage)
pie = py.plot([pie],auto_open = True, file_name = "Plot2",)


generation2 = []
attack = []
query3 = """
    SELECT GENERATIONS.GEN_NUM, ROUND(AVG(POKEMONS.ATTACK), 3) AVG_ATTACK
    FROM GENERATIONS
    JOIN POKEMONS
    ON POKEMONS.GEN_NUM = GENERATIONS.GEN_NUM
    GROUP BY GENERATIONS.GEN_NUM
    ORDER BY GENERATIONS.GEN_NUM ASC
"""
cursor.execute(query3)

for row in cursor.fetchall():
    generation2.append (row[0])
    attack.append(row[1])
scatter = go.Scatter (x = generation2, y = attack)
scatter = py.plot([scatter],auto_open = True, file_name = "Plot3")

my_dboard = dash.Dashboard()
bar_id = GetId(bar)
pie_id = GetId(pie)
scatter_id = GetId(scatter)
box_1= {
    'type': 'box',
    'boxType': 'plot',
    'fileId': bar_id,
    'title': 'Покоління покемонів та загальну кількість покемонів цього покоління'
}

box_2 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': pie_id,
    'title': 'Тип покемонів та % покемонів, що мають цей тип як перший від загальної кількості покемонів'

}

box_3 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': scatter_id,
    'title': 'Середнє значення атаки покемонів в динаміці зміни поколінь'
}


my_dboard.insert(box_1)
my_dboard.insert(box_2, 'below', 1)
my_dboard.insert(box_3, 'right', 2)

py.dashboard_ops.upload(my_dboard, 'Lab_2')
    
cursor.close()
connection.close()