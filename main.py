import cx_Oracle

username = "Lab_2"                                      
password = "query"                                                                                      
database = "localhost/xe"

connection = cx_Oracle.connect(username, password, database)

query1 = """
    SELECT GEN_NUM, MAX_POKEMON_NUM - MIN_POKEMON_NUM + 1 AS QUANTITY FROM GENERATIONS
"""

query2 = """
    SELECT P_TYPES.P_TYPE, ROUND(count(*) / (SELECT count(*) FROM POKEMONS ), 4 ) AS PERCENTAGE
    FROM P_TYPES
    JOIN POKEMONS
    ON POKEMONS.TYPE_1 = P_TYPES.P_TYPE
    GROUP BY P_TYPE
"""

query3 = """
    SELECT GENERATIONS.GEN_NUM, ROUND(AVG(POKEMONS.ATTACK), 3) AVG_ATTACK
    FROM GENERATIONS
    JOIN POKEMONS
    ON POKEMONS.GEN_NUM = GENERATIONS.GEN_NUM
    GROUP BY GENERATIONS.GEN_NUM
    ORDER BY GENERATIONS.GEN_NUM ASC
"""

cursor = connection.cursor()

cursor.execute(query1)

for row in cursor:
    print(row)


cursor.execute(query2)

for row in cursor:
    print(row)

cursor.execute(query3)

for row in cursor:
    print(row)

    
cursor.close()
connection.close()