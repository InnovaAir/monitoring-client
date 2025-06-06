import random
from datetime import datetime, timedelta
import mysql.connector
#CONEXÃO COM O BANCO
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
    (11, 30, 95), (12, 500, 4000), (13, 2147800000, 2147800000), (14, 35, 90), (15, 400, 3000),
    (16, 2147800000, 2147800000), (17, 25, 85), (18, 200, 2000), (19, 2147800000, 2147800000), (20, 20, 80),
    (21, 600, 3500), (22, 2147800000, 2147800000), (23, 30, 95), (24, 500, 4000), (25, 2147800000, 2147800000),
    (26, 25, 85), (27, 300, 2500), (28, 2147800000, 2147800000), (29, 35, 90), (30, 450, 3500),
    (31, 2147800000, 2147800000), (32, 20, 80), (33, 500, 4000), (34, 2147800000, 2147800000), (35, 30, 95),
    (36, 350, 3000), (37, 2147800000, 2147800000), (38, 35, 90), (39, 600, 4000), (40, 2147800000, 2147800000),
    (41, 40, 95), (42, 30, 85), (43, 35, 90), (44, 25, 75), (45, 30, 85),
    (46, 35, 90), (47, 25, 75), (48, 30, 85), (49, 35, 90), (50, 25, 75),
    (51, 10, 100), (52, 20, 200), (53, 15, 150), (54, 25, 250), (55, 20, 120),
    (56, 30, 220), (57, 10, 110), (58, 20, 210), (59, 15, 140), (60, 25, 240),
    (61, 20, 130), (62, 30, 230), (63, 10, 105), (64, 20, 205), (65, 15, 145),
    (66, 25, 245), (67, 20, 135), (68, 30, 235), (69, 10, 115), (70, 20, 215)
]


# NESSAS 2 LINHAS DEFIMINIMOS E MOMENTO ATUAL DE DE QUANTO TEMPO QUEREMOS SIMULAR OS DADOS 
# SE NO timedelta() ESTIVER 30 VAI SIMULAR DADOS DOS ULTIMOS 30 DIAS SE TIVER 365 VAI SIMULAR
# DADOS DOS ULTIMOS 365 DIAS
now = datetime.now()
start_time = now - timedelta(days=180)

# USAMOS UM FOR APRIMORADO E DECLARAMOS QUE PARA CADA CONJUNTO QUER PERCORRERMOS A PRIMEIRA VARIÁVEL
#  É O ID DA MÉTRICA A SEGUNDA É O LIMITE MINIMO E A TERCEIRA O LIMITE MAXIMO

for metrica_id, limite_min, limite_max in metricas:
    # AQUI DECLARAMOS QUANTOS INSERTS QUEREMOS PARA CADA METRICA SE QUISER FAZER APENAS UMA SIMULAÇÃO RÁPIDA DEIXE ALGO PEQUENO
    #  COMO 500
    num_inserts = 350
    # DEFINIMOS O LIMITEMEDIO
    meio = (limite_min + limite_max) / 2

    # FAZEMOS UM FOR PARA O NUMERO DE INSERTS
    # CRIAMOS UM VALOR ALEATÓRIO ENTRE 0 E 100 E DEPOIS VERIFICAMOS
    # A QUE NIVEL DE GRAVIDADE ISSO EQUIVALE
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
        
        # PEGAMOS O DATETIME ATUAL
        momento = start_time + timedelta(seconds=random.randint(0, int((now - start_time).total_seconds())))
        
        # TAMBÉM CASO GRAVIDADE NÃO SEJA NULO INSERIMOS EM CAPTURA_ALERTA
        if(gravidade != 'nulo'):
            insert = (
            f"INSERT INTO captura_alerta (valorCapturado, momento, gravidade, fkMetrica) "
            f"VALUES ({valor}, '{momento.strftime('%Y-%m-%d %H:%M:%S')}', '{gravidade}', {metrica_id});"
            )
            cursor.execute(insert)
            
        mydb.commit()