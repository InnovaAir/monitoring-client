import psutil
import subprocess
import time
import datetime

            # Dados relevantes
            # RAM:
            # porcentagemUso
# ramPorcentagemUso = psutil.virtual_memory().percent
# print(ramPorcentagemUso)
#             # total
# ramTotal = psutil.virtual_memory().total
# print(ramTotal)
            # processos
# listaProcessos = []
for processo in psutil.process_iter([]):
    print(processo.info['name'])
            # CPU:
#             # porcentagemUso
# cpuPorcentagemUso = psutil.cpu_percent()
# print(cpuPorcentagemUso)
            # frequencia
            # boottime
# boot_time = round(psutil.boot_time())
# print(boot_time)
# agora = time.time()
# tempoLigado = int(agora - boot_time)
# print(tempoLigado)
# boot_datetime = datetime.datetime.fromtimestamp(boot_time)
# tempoLigado = datetime.datetime.now() - boot_datetime
# tempoLigado = str(tempoLigado).split('.')[0]
# print(tempoLigado)
# cpuFreq = psutil.cpu_freq().max
# print(cpuFreq)
            # Disco:
            # porcentagemUso
# discoPorcentagemUso = psutil.disk_usage('C:/').percent
# print(discoPorcentagemUso)
            # total
# discoTotal = psutil.disk_usage('C:/').total
# print(discoTotal)
            # Rede:
            # downloadBytes
redeDownload1 = psutil.net_io_counters().bytes_sent
time.sleep(2)
redeDownload2 = psutil.net_io_counters().bytes_sent
redeDownload = redeDownload2 - redeDownload1
print(redeDownload)
            # uploadBytes
redeUpload1 = psutil.net_io_counters().bytes_recv
time.sleep(2)
redeUpload2 = psutil.net_io_counters().bytes_recv
redeUpload = redeUpload2 - redeUpload1
print(redeUpload)