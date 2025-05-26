import array
from email import header
from multiprocessing import process
from traceback import print_tb
from flask import Flask, request
import subprocess
import requests
import datetime
import time
import threading
import psutil
import platform

def obterSerialPlacaMae():
    try:
        if psutil.WINDOWS:
            result = subprocess.check_output(
                "wmic baseboard get serialnumber",
                shell=True,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            serial = result.strip().split("\n")[-1].strip()
        elif psutil.LINUX:
            result = subprocess.check_output(
                "sudo dmidecode -t baseboard | grep 'Serial Number'",
                shell=True,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            serial = result.split(":")[-1].strip()
        elif psutil.MACOS:  
            result = subprocess.check_output(
                "system_profiler SPHardwareDataType | grep 'Serial Number (system)'",
                shell=True,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            serial = result.split(":")[-1].strip()
        else:
            raise Exception("Sistema operacional não suportado.")

        return serial
    except Exception as e:
        print(f"Erro ao obter número de série da placa-mãe: {e}")
        return None

# Criação do API Flask
app = Flask(__name__)

@app.get('/cache')
def usage_cache():
    
    if (request.remote_addr != '10.18.33.61'):
        return "Acesso negado" 

    print("Capturando total de Espaço usado em Cache")

    querry = subprocess.run(["du", "-hs", "/etc"], shell=True, capture_output=True, text=True).stdout.strip()
    espacoUsado = querry.split()[0]

    mensagem = f"O espaço que está sendo utilizado é: {espacoUsado}"
    return mensagem

@app.delete('/kill')
def kill_process():
    #ID do Processo
    pid = request.args.get('pid')

    if (pid == None): return "Argumento Nulo"
    
    print(f"Matando o processo {pid}")

    # Querry
    subprocess.run(f"kill {pid}", shell=True, capture_output=True, text=True)

    mensagem = f"Processo finalizado com sucesso"
    return mensagem

def enviarDados():

    while True:
        arrayDados = {'cpu':[],'ram':[],'disco':[],'rede':[]}

        # Captura de dados de máquina a cada
        # Gera um array com 6 dados = 1 minuto
        i = 0
        while (i < 1):

            cpuPorcentagemUso = psutil.cpu_percent(interval=None)
            ramPorcentagemUso = psutil.virtual_memory().percent
            discoPorcentagemUso = psutil.disk_usage('/').percent       
            redeDownload1 = psutil.net_io_counters().bytes_sent

            arrayDados["cpu"].append(cpuPorcentagemUso)
            arrayDados["ram"].append(ramPorcentagemUso)
            arrayDados["disco"].append(discoPorcentagemUso)
            arrayDados["rede"].append(redeDownload1)
            
            i = i + 1
        
        comando = ''
        processos = ''
        
        # Busca ds 5 Maiores Processos
        if (psutil.WINDOWS):
            comando = """
            Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 `
            @{Name="ProcessName";Expression={$_.ProcessName}}, 
            @{Name="CPU(s)";Expression={[math]::Round($_.CPU,2)}}, 
            @{Name="Memory(MB)";Expression={[math]::Round($_.WorkingSet64 / 1MB, 2)}}, 
            @{Name="Uptime";Expression={(Get-Date) - $_.StartTime}}, 
            Id"""
            processos = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=False).stdout.strip()

        elif (psutil.LINUX):
            comando = "ps -eo pid,comm,%cpu,%mem,time --sort=-%cpu | head -n 6"
            processos = subprocess.run(comando, shell=True, capture_output=True, text=False).stdout.strip().split()
        # Transformando o Byte para String e separando pelos os espaços de '\r\n'
        processos = processos.decode("utf-8").split('\r\n')
    
        # Apagando os espaços vazios do array
        i = 0    
        while i < len(processos):
            if processos[i] == "":
                del processos[i]  # Remove o elemento no índice i
                i -= 1  # Ajusta o índice para evitar erros de iteração
            i += 1

        # Separando as linhas do processo
        i = 0
        
        arrayTratamento = []
        arrayProcessos = []
        while i < len(processos):
            split_proc = processos[i].split(":",1)
            v_type = split_proc[0].strip()
            
            value = split_proc[1].strip()
            
            arrayTratamento.append({v_type:value})
            i = i + 1
        
        # Tratamento dos Dados para Dict com informações de cada processo
        for i in range(5):
            arrayProcessos.append([arrayTratamento[0], arrayTratamento[1], arrayTratamento[2], arrayTratamento[3], arrayTratamento[4]])
            
            del arrayTratamento[:5]

        # Envia os dados de processos tratados
        ip = 'localhost'
        url = f"http://{ip}:3333/dados/tempoReal"
        headers = {"Content-Type":"application/json"}
        
        placa_mae = obterSerialPlacaMae()

        if (placa_mae == None): return 'Serial Placa-Mãe nulo'

        try:
            requests.post(url, json={'placa_mae':placa_mae, 'momento':f'{datetime.datetime.now()}', 'processos':arrayProcessos, 'dados':arrayDados}, headers=headers)
        except:
            print("Erro ao enviar dados ao Web-Data-Viz")
            
        time.sleep(20)

# Rodando o servidor
def rodarServer():
    if __name__ == '__main__':
        app.run(port=5000, host='localhost', debug=False)    