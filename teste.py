import psutil
import subprocess

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
redeDownload = psutil.net_io_counters().bytes_sent
print(redeDownload)
            # uploadBytes
redeUpload = psutil.net_io_counters().bytes_recv
print(redeUpload)

especificacao = str(subprocess.check_output('wmic diskdrive get Model', shell=True, text=True).split()[1:3]).replace("[",  "").replace("]", "").replace("'", "").replace(",", "")

print(especificacao)