# Bibliotecas
from concurrent.futures import thread
from msvcrt import kbhit
import threading
import time
import keyboard as kb

# Arquivos
import client
import app

threadColetarDadosMaquina = threading.Thread(target=client.menuInicial)
threadEscutarPorta = threading.Thread(target=app.rodarServer)
threadEnviarDadosRota = threading.Thread(target=app.enviarDados)

threadColetarDadosMaquina.daemon = True
threadEscutarPorta.daemon = True
threadEnviarDadosRota.daemon = True

print("SERÁ INICIADO A EXECUÇÃO DAS COLETAS DOS DADOS:")
print("\n   CASO DESEJE PARA A EXECUÇÃO DO ARQUIVO: PRESSIONE C \n\n")

threadColetarDadosMaquina.start()
time.sleep(2)
threadEscutarPorta.start()
threadEnviarDadosRota.start()

while True:
    if kb.is_pressed('m'):
        print("\n\nTECLA E FOI PRESSIONADA \n SAINDO...")
        time.sleep(0.05)
        exit()