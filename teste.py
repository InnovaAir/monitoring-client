import psutil
import subprocess
import time

            # Dados relevantes
            # RAM:
            # porcentagemUso
ramPorcentagemUso = psutil.virtual_memory().percent
print(ramPorcentagemUso)
            # total
ramTotal = psutil.virtual_memory().total
print(ramTotal)
            # processos

            # CPU:
            # porcentagemUso
cpuPorcentagemUso = psutil.cpu_percent()
print(cpuPorcentagemUso)
            # frequencia
cpuFreq = psutil.cpu_freq().max
print(cpuFreq)
            # Disco:
            # porcentagemUso
discoPorcentagemUso = psutil.disk_usage('C:/').percent
print(discoPorcentagemUso)
            # total
discoTotal = psutil.disk_usage('C:/').total
print(discoTotal)
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

especificacao = str(subprocess.check_output('wmic diskdrive get Model', shell=True, text=True).split()[1:3]).replace("[",  "").replace("]", "").replace("'", "").replace(",", "")

print(especificacao)

especificacao = subprocess.check_output('lspci | grep -i ethernet', shell=True, text=True)
print(especificacao)


# wmic nic get Name, Manufacturer, ProductName