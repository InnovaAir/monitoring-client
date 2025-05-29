import random
from datetime import datetime, timedelta
import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="innova_client",
        password="Innovaair@123",
        database="innovaair"
    )
cursor = mydb.cursor()

# Lista de métricas com id, limiteMin, limiteMax
metricas = [
    (1, 20, 90), (2, 25, 85), (3, 30, 80), (4, 20, 95), (5, 15, 75),
    (6, 25, 85), (7, 30, 80), (8, 20, 95), (9, 15, 75), (10, 25, 85),
    (11, 30, 95), (12, 35, 90), (13, 25, 85), (14, 20, 80), (15, 30, 95),
    (16, 25, 85), (17, 35, 90), (18, 20, 80), (19, 30, 95), (20, 35, 90),
    (21, 40, 95), (22, 30, 85), (23, 35, 90), (24, 25, 75), (25, 30, 85),
    (26, 35, 90), (27, 25, 75), (28, 30, 85), (29, 35, 90), (30, 25, 75)
]

# Tempo: de 30 dias atrás até agora
now = datetime.now()
start_time = now - timedelta(days=365)

all_inserts = []

for metrica_id, limite_min, limite_max in metricas:
    num_inserts = 35040
    meio = (limite_min + limite_max) / 2

    for _ in range(num_inserts):
        valor = round(random.uniform(0, 100), 2)
        gravidade = None

        if limite_min <= valor < meio:
            gravidade = 'baixo'
        elif meio <= valor < limite_max:
            gravidade = 'alto'
        elif valor >= limite_max:
            gravidade = 'critico'
        else:
            gravidade = 'nulo'

        momento = start_time + timedelta(seconds=random.randint(0, int((now - start_time).total_seconds())))
        insert = (
          f"INSERT INTO dados_previsao (valorPrevisto, momento, gravidade, fkMetrica, isPrevisao) "
          f"VALUES ({valor}, '{momento.strftime('%Y-%m-%d %H:%M:%S')}', '{gravidade}', {metrica_id}, 0);"
        )
        cursor.execute(insert)
        if(gravidade != 'nulo'):
            insert = (
            f"INSERT INTO captura_alerta (valorCapturado, momento, gravidade, fkMetrica) "
            f"VALUES ({valor}, '{momento.strftime('%Y-%m-%d %H:%M:%S')}', '{gravidade}', {metrica_id});"
            )
            cursor.execute(insert)
        mydb.commit()
