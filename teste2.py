import mysql.connector
from mysql.connector import Error
import psutil
import time
import subprocess
import socket, platform, cpuinfo

mydb = mysql.connector.connect(
        host="localhost",
        user="innova_client",
        password="Innovaair@123",
        database="innovaair"
    )

cursor = mydb.cursor()

result = subprocess.check_output(
    "wmic baseboard get serialnumber",
    shell=True,
    stderr=subprocess.STDOUT,
    universal_newlines=True
)

numeroSeriePlacaMae = result.strip().split("\n")[-1].strip()
print(numeroSeriePlacaMae)
# Consulta o banco de dados para encontrar o Computador com o MAC Address
consulta = "SELECT idMaquina FROM maquina WHERE numeroSerial = '%s'" % numeroSeriePlacaMae
cursor.execute(consulta)
# Recupera o resultado da consulta
myresult = cursor.fetchall()
idComputador = myresult[0][0]
cursor = mydb.cursor()
consulta_ids = """
    SELECT idComponente, componente from componente join maquina on idMaquina = fkMaquina where idMaquina = %s
    """
# Executa a consulta para obter os IDs da CPU e da Memória
cursor.execute(consulta_ids, (idComputador,))
resultado_ids = cursor.fetchall()
print(resultado_ids)
if resultado_ids:
    id_cpu, id_memoria = resultado_ids
    print(f"ID da CPU associada: {id_cpu}")
    print(f"ID da Memória associada: {id_memoria}")
    while True:
        ramPorcentagemUso = psutil.virtual_memory().percent
        print("-------------------------------------------------------------")
        print(f"Porcentagem de cpu sendo usada: {ramPorcentagemUso}%")
        print("-------------------------------------------------------------")
        # Preparando consultas
        # consulta_cpu = "INSERT INTO MetrmicaCPU (percentualUso, fkCpu) VALUES (%.2f, %d)" % (cpuPercent, id_cpu)
        # consulta_memoria = "INSERT INTO MetricaMemoria (percentualUso, quantidadeLivre, quantidadeUsada, fkMemoria) VALUES (%.2f, %.2f, %.2f, %d)" % (memVirtualPerc, memVirtualFree, memVirtualUsed, id_memoria)
        # print("Executando consulta: %s\nExecutando consulta: %s" % (consulta_cpu, consulta_memoria))
        # cursor.execute(consulta_cpu)
        # mydb.commit()
        # cursor.execute(consulta_memoria)
        # mydb.commit()
        time.sleep(3)