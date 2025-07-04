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
threadEnviarDadosRota = threading.Thread(target=app.enviarDados)

threadColetarDadosMaquina.daemon = True
threadEnviarDadosRota.daemon = True

print("SERÁ INICIADO A EXECUÇÃO DAS COLETAS DOS DADOS:")
print("\n   CASO DESEJE PARA A EXECUÇÃO DO ARQUIVO: PRESSIONE C + V'\n\n")

threadColetarDadosMaquina.start()
threadEnviarDadosRota.start()

while True:
    if kb.is_pressed('c') and kb.is_pressed('v'):
        print("\n\nTECLA E FOI PRESSIONADA \n SAINDO...")
        time.sleep(0.025)
        exit()