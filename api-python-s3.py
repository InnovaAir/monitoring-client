import mysql.connector
import csv
import boto3

bucket_name = 'innovaair-raw'
arquivo_csv_local = 'data.csv'
chave_no_s3 = 'sshinnovaairserver.pem' 

mydb = mysql.connector.connect(
    host="localhost",
    user="innova_s3",
    password="Innovaair@123",
    database="innovaair"
)
cursor = mydb.cursor()

consulta = "SELECT razaoSocial, idFilial, idMaquina, componente, especificacao, metrica, valorCapturado, momento from maquina join componente on idMaquina = fkMaquina join metrica on idComponente = fkComponente join captura_historico on idMetrica = fkMetrica join filial on idFilial = fkFilial join cliente on idCliente = fkCliente" % ()
cursor.execute(consulta)
valores = cursor.fetchall()
valores = [list(valor) for valor in valores]

print(valores)
    
data = [
    ['razaoSocial', 'idFilial', 'idMaquina', 'componente', 'especificacao', 'metrica', 'valorCapturado', 'momento'],
]
data.extend(valores)
    
filename = 'data.csv'
    
with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(data)

s3 = boto3.client('s3')

s3.upload_file(arquivo_csv_local, bucket_name, chave_no_s3)