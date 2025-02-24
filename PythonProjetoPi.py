import mysql.connector;
import psutil;
import time;
from datetime import datetime;

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="muffin123",
  database="TesteProjetoPi"
)
mycursor = mydb.cursor()

# CREATE TABLE infosComputador (tipoSO varchar(40), cpuPercent float, DiskUsageTotal float, cpuFreq float, cpuCpount int);
# ALTER TABLE  infosComputador MODIFY COLUMN memoriaSwap float (5,2);
# ALTER TABLE infosComputador ADD COLUMN horario datetime;

# Infos que podem ser importante para as máquinas de check-in de aeroportos:
# cpu - % que está sendo usada
# memória virtual - %
# memória virtual - disponível / total GB
# tempo de uso
# rede
# processos ativos

while True:

    cpuPercent = format(psutil.cpu_percent())
    memVirtualPerc = format(psutil.virtual_memory().percent)
    redeBytesSent = psutil.net_io_counters().bytes_sent
    redeBytesRecv = psutil.net_io_counters().bytes_recv
    disco = psutil.disk_usage("/Users/gabriellalodiantunes").used/1e+9

# Isso pode servir para ver se um computador de check-in ta transmitindo os dados de maneira correta
    redePacksSent = psutil.net_io_counters().packets_sent
    redePacksRecv = psutil.net_io_counters().packets_recv

    mediaSent = redeBytesSent / redePacksSent if redePacksSent > 0 else 0
    mediaRecv = redeBytesRecv / redePacksRecv if redePacksRecv > 0 else 0

    uptimeSeconds = time.time() - psutil.boot_time()

    # o time.time() pega o número de segundos que se passaram desde o "start" da época.
    # a época seria 1º de janeiro de 1970, à meia-noite UTC (Coordinated Universal Time). Esse momento é conhecido como Unix Epoch.
    # A escolha do 1º de janeiro de 1970 como a "época" tem a ver com a história do Unix, um sistema operacional criado nos anos 60 e 70. Aqui está um resumo:
    # Ao usar segundos desde a época, o Unix poderia calcular facilmente o tempo com um número inteiro. Isso simplifica o uso e a precisão do tempo em sistemas com capacidade limitada de armazenamento e processamento (o que era uma preocupação no início da computação).

    # o psutil.boot_time() retorna exatamente o momento em que o sistema foi iniciado ou reiniciado. Esse é o ponto de referência para medir quanto tempo o seu computador ficou ligado sem ser reiniciado.

    uptimeHours = int(uptimeSeconds / 3600)
    uptimeMinutes = int((uptimeSeconds % 3600) / 60)
    uptimeSeconds = int(uptimeSeconds % 60)


    totalHoras = format(f"{uptimeHours}h {uptimeMinutes}m {uptimeSeconds}s")
    mediaSentf = format(f"{mediaSent:.2f}")
    mediaRecvf = format(f"{mediaRecv:.2f}")
    # % ajuda a pegar o "resto" (quantos segundos ou minutos restaram).
    # 1 hora = 3600 segundos
    # 1 minuto = 60 segundos

    # o if aqui serve para, caso a quantidade de pacotes for 0, a conta não dar erro !! já que divir algo por 0 não da muito certo skjdksjd


    print("-------------------------------------------------------------")
    print(f"Tamanho médio dos pacotes enviados: {mediaSent:.2f} bytes")
    print(f"Tamanho médio dos pacotes recebidos: {mediaRecv:.2f} bytes")
    print(f"Porcentagem de memória vitual: {memVirtualPerc}%")
    print(f"Porcentagem de cpu sendo usada: {cpuPercent}%")
    print(f"Tempo de Atividade: {totalHoras}")
    print(f"Uso do disco: {disco:.2f}")
    print("-------------------------------------------------------------")

    sql = "INSERT INTO InfosComputer (fkComputador, pacotesRecv, pacotesEnv, memVirtual, cpuUsada, tempoAtvd, discoUso, horarioLog) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    print(f"Porcentagem de cpu sendo usada: {cpuPercent}%")
    val = ("1", mediaSent, mediaRecv, memVirtualPerc, cpuPercent, totalHoras, disco, datetime.now())

    mycursor.execute(sql,val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

    time.sleep(1)
# print(redeBytesSent)
# print(redeBytesRecv)
# print(redePacksSent)
# print(redePacksRecv)

