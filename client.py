from gc import collect
from tarfile import NUL
import mysql.connector
from mysql.connector import Error
import psutil
import time
import subprocess
import socket, platform, cpuinfo
from datetime import datetime
import csv
import boto3
import threading

def menuInicial():
    saiu = False
    while (saiu == False):
        opcao = int(
            input("Bem vindo ao client InnovaAir, digite uma opção para prosseguir:\n1. Rodar sistema\n2. Sair\n"))
        match (opcao):
            case 1:
                home()
                email = input("\nInforme seu e-mail:\n")
                senha = input("Informe sua senha:\n")
                if (login(email, senha)):
                    home()
                    saiu = True
                else:
                    print("Login ou senha inválidos, tente novamente!")
                    return
            case 2:
                print("Até mais :)")
                saiu = True
                exit()

def login(email, senha):
    consulta = """
      SELECT idUsuario FROM Usuario WHERE email = %s AND senha = %s;
      """
    try:
        # Executa a consulta no banco de dados
        cursor.execute(consulta, (email, senha))


        resultado = cursor.fetchone()

        if resultado:
            print("Usuário encontrado! Login válido.")
            return True
        else:
            return False
    except Exception as e:
        print(f"Erro ao validar login: {e}")
        return False

def obterSerialPlacaMae():
    system = platform.system()
    try:
        if system == "Windows":
            result = subprocess.check_output(
                "wmic baseboard get serialnumber",
                shell=True,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            serial = result.strip().split("\n")[-1].strip()
        elif system == "Linux":
            result = subprocess.check_output(
                "sudo dmidecode -t baseboard | grep 'Serial Number'",
                shell=True,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            serial = result.split(":")[-1].strip()
        elif system == "Darwin":  
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
def resgatarIdComputador():
                numeroSeriePlacaMae = obterSerialPlacaMae()
                # Consulta o banco de dados para encontrar o Computador com o MAC Address
                consulta = "SELECT idMaquina FROM maquina WHERE numeroSerial = '%s'" % numeroSeriePlacaMae
                cursor.execute(consulta)
                #print("Executando a consulta: %s" % consulta)

                # Recupera o resultado da consulta
                myresult = cursor.fetchall()

                if len(myresult) > 0:
                    # Se o Computador for encontrado, retorna o ID
                    id_Computador = myresult[0][0]
                    print(f"Máquina encontrada no sistema.ID: {id_Computador}")
                    return id_Computador
                else:
                    print(f"Máquina não encontrada!")

                return None



def home():
    saiu = False
    while (saiu == False):
        opcao = int(input(
            "\nBem vindo ao client InnovaAir, digite uma opção para prosseguir: \n1. Iniciar captura de dados computacionais.\n2. Verificar informações do Computador\n3. Sair\n"))
        match (opcao):
            case 1:
                print("Verificando se a máquina já está cadastrada no banco de dados...")
                cadastrada = verificarMaquinaCadastrada()
                if (cadastrada):
                    id_Computador = resgatarIdComputador()
                    capturarDados(id_Computador)
            case 2:
                exibirDadosComputacionais()
            case 3:
                print("\nAté mais :)")
                saiu = True
                exit()
                
limiteMinCPU = 80
limiteMaxCPU = 90
limiteMinRAM = 80
limiteMaxRAM = 90
limiteMinDISCO = 80
limiteMaxDISCO = 90

def cadastrarCPU(fkComputador):
    print("\nCadastrando CPU...")
    # capturando informações da CPU
    # resgatando o modelo da CPU (atributo brand_raw do objeto de resposta)
    modelo =  cpuinfo.get_cpu_info()['brand_raw']

    consulta = "INSERT INTO componente (componente, especificacao, fkMaquina) VALUES ('%s', '%s', %s)" % ('Processador', modelo, fkComputador)
    #print("Executando a consulta SQL: '%s'", consulta)
    cursor.execute(consulta)
    mydb.commit()
    id_cpu_cadastrada = cursor._last_insert_id
    #Registrando métricas
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('porcentagemUso', %s, %s, %s)" % (limiteMinCPU, limiteMaxCPU, id_cpu_cadastrada)
    cursor.execute(consulta)
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('frequencia', null, null, %s)" % (id_cpu_cadastrada)
    cursor.execute(consulta)
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('processos', null, null, %s)" % (id_cpu_cadastrada)
    cursor.execute(consulta)
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('tempoAtividade', null, null, %s)" % (id_cpu_cadastrada)
    cursor.execute(consulta)
    mydb.commit()
    #fkMetrica = cursor._last_insert_id
    #frequencia = psutil.cpu_freq().max
    #consulta = "INSERT INTO captura_alerta (valorCapturado, fkMetrica, gravidade) VALUES (%s, %s, 'baixo')" % (frequencia, fkMetrica)
    #cursor.execute(consulta)
    mydb.commit()
    print("\nCPU de id %d cadastrado\n" % id_cpu_cadastrada)

    mydb.commit()
def cadastrarMemoria(fkComputador):
    print("\nCadastrando memória...")
    system = platform.system()
    if system == "Windows":
        especificacao = subprocess.check_output('wmic memorychip get Manufacturer', shell=True, text=True)
        especificacao = especificacao.replace("\n","").replace(" ","")[12:]
    elif system == "Linux":
        especificacao = subprocess.check_output('sudo dmidecode --type memory | grep -i Manufacturer', shell=True, text=True)
        especificacao = especificacao.replace("\n","").replace(" ","").replace("Manufacturer:", "")[10:]
    consulta = "INSERT INTO componente (componente, especificacao, fkMaquina) VALUES ('%s', '%s', %s)" % ('RAM', especificacao, fkComputador)
    #print("Executando a consulta SQL: '%s'", consulta)
    cursor.execute(consulta)
    mydb.commit()

    id_memoria_cadastrada = cursor._last_insert_id
    #Registrando métricas
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('porcentagemUso', %s, %s, %s)" % (limiteMinRAM, limiteMaxRAM, id_memoria_cadastrada)
    cursor.execute(consulta)
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('processos', null, null, %s)" % (id_memoria_cadastrada)
    cursor.execute(consulta)
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('total', null, null, %s)" % (id_memoria_cadastrada)
    cursor.execute(consulta)
    mydb.commit()
    #total = psutil.virtual_memory().total
    #fkMetrica = cursor._last_insert_id
    #consulta = "INSERT INTO captura_alerta (valorCapturado, fkMetrica, gravidade) VALUES (%s, %s, 'baixo')" % (total, fkMetrica)
    #cursor.execute(consulta)
    mydb.commit()
    print("memória de id %d cadastrado\n" % id_memoria_cadastrada)


def cadastrarDiscos(fkComputador):
    print("\nCadastrando discos...")

    system = platform.system()
    windows_version = platform.version()  # Obtém a versão do Windows, por exemplo, '10.0.19042' para Windows 10 ou '10.0.22000' para Windows 11
    
    if system == "Darwin":  # Se for macOS
        try:
            # Usando 'diskutil list' para obter as partições e discos no macOS
            result = subprocess.check_output(
                "diskutil list",
                shell=True,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Filtrando a saída do 'diskutil list' para extrair discos e partições
            # A saída do 'diskutil list' precisa ser processada para pegar discos válidos.
            print("Informações dos discos no macOS:")
            discos_info = result.splitlines()
            for line in discos_info:
                # Exemplo de validação simples para encontrar discos, pode ser adaptado conforme necessário
                if "/dev/" in line:  # Validar que é um disco
                    disco_nome = line.split()[0]  # Pega o nome do dispositivo (ex: /dev/disk1)
                    capacidade = 0  # No macOS, podemos capturar mais dados, mas aqui simplificamos.
                    sistema_arquivos = "HFS+"  # A maioria dos sistemas de arquivos no macOS é HFS+ ou APFS

                    # Consulta SQL para inserir as informações no banco de dados
                    consulta = """
                    INSERT INTO componente (componente, especificacao, fkMaquina)
                    VALUES (%s, %s, %s)
                    """
                    parametros = ("Armazenamento", especificacao, fkComputador)

                    #print(f"Executando a consulta para cadastrar o disco: {disco_nome}...")

                    cursor.execute(consulta, parametros)
                    mydb.commit()

                    id_disco_cadastrado = cursor.lastrowid

                    print(f"Disco de id {id_disco_cadastrado} cadastrado com sucesso no macOS!\n")
                    
        except Exception as e:
            print(f"Erro ao buscar ou cadastrar discos no macOS: {e}")
    
    elif system == "Windows":  # Se for Windows (verificando versão)
        try:
            # Agora, coletando os discos no Windows usando psutil
            try:
                especificacao = str(subprocess.check_output('wmic diskdrive get Model', shell=True, text=True).split()[1:3]).replace("[",  "").replace("]", "").replace("'", "").replace(",", "")
                # Consulta SQL para inserir as informações no banco de dados
                consulta = """
                INSERT INTO componente (componente, especificacao, fkMaquina)
                VALUES (%s, %s, %s)
                """
                parametros = ("Armazenamento", especificacao, fkComputador)
                # Executa a consulta no banco de dados
                cursor.execute(consulta, parametros)
                mydb.commit()
                id_disco_cadastrado = cursor.lastrowid
                consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('porcentagemUso', %s, %s, %s)" % (limiteMinDISCO, limiteMaxDISCO, id_disco_cadastrado)
                cursor.execute(consulta)
                consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('total', null, null, %s)" % (id_disco_cadastrado)
                cursor.execute(consulta)
                mydb.commit()
                #fkMetrica = cursor._last_insert_id
                #valorCaptura = psutil.disk_usage('C:/').total
                #consulta = "INSERT INTO captura_alerta (valorCapturado, fkMetrica, gravidade) VALUES (%s, %s, 'baixo')" % (valorCaptura, fkMetrica)
                #cursor.execute(consulta)
                mydb.commit()
                print(f"Disco de id {id_disco_cadastrado} cadastrado com sucesso!\n")
            except Exception as e:
                print(f"Erro ao cadastrar o disco: {e}")
        
        except Exception as e:
            print(f"Erro ao obter o número de série da placa-mãe ou ao buscar discos no Windows: {e}")

def cadastrarRede(fkComputador):
    system = platform.system()
    if system == "Windows":
        especificacao = subprocess.check_output('wmic nic get Manufacturer, Name, Description', shell=True, text=True)
        especificacao = especificacao.strip().replace(" ", "").split("\n")[2]
    elif system == "Linux":
        especificacao = subprocess.check_output('lspci | grep -i ethernet', shell=True, text=True)
        especificacao = especificacao.split("Ethernet controller:")[-1].strip()
    consulta = "INSERT INTO componente (componente, especificacao, fkMaquina) VALUES ('%s', '%s', %s)" % ('Rede', especificacao, fkComputador)
    #print("Executando a consulta SQL: '%s'", consulta)
    cursor.execute(consulta)
    mydb.commit()
    redeCadastrado = cursor._last_insert_id
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('velocidadeDownload', 15, 5, %s)" % (redeCadastrado)
    cursor.execute(consulta)

    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('velocidadeUpload', 15, 5, %s)" % (redeCadastrado)
    cursor.execute(consulta)
    mydb.commit()
    print(f"Chip de rede de id {redeCadastrado} cadastrado com sucesso!\n")
    

def cadastrarMaquina():
    print
    modelo = input("Digite o modelo desta máquina (Em letra minuscula): ")
    hostname = socket.gethostname()
    endereco_mac = psutil.net_if_addrs()["Ethernet"][0].address
    numero_serie = obterSerialPlacaMae()
    print('\nCadastrando a máquina no banco de dados:\nNumero Serial: %s\nHostname: %s\nEndereço MAC %s' % (numero_serie, endereco_mac, hostname))
    fkFilial = int(input("Insira o id da filial a qual essa máquina pertence: "))
    consulta = "INSERT INTO maquina(numeroSerial, enderecoMac, hostname, fkFilial, modelo) VALUES ('%s', '%s', '%s', %s, '%s')" % (numero_serie, endereco_mac, hostname, fkFilial, modelo)
    cursor.execute(consulta)
    mydb.commit()
    id_Computador_cadastrado = cursor._last_insert_id
    print("Computador de id %d cadastrado" % id_Computador_cadastrado)
    print("\nCadastrando componentes do Computador...")
    cadastrarCPU(id_Computador_cadastrado)
    cadastrarMemoria(id_Computador_cadastrado)
    cadastrarDiscos(id_Computador_cadastrado)
    cadastrarRede(id_Computador_cadastrado)

def verificarMaquinaCadastrada():
                consulta = "SELECT * FROM maquina WHERE numeroSerial = '%s'" % obterSerialPlacaMae()
                cursor.execute(consulta)
                #print("Executando a consulta: %s" % consulta)
                myresult = cursor.fetchall()
                if (len(myresult) > 0):
                    print("Máquina encontrada no sistema")
                    return True
                else:
                    print("Máquina ainda não cadastrada!")
                    cadastrarMaquina()
                return False



def capturarDados(idComputador):
    # Capturando ID das cpus e memorias associados
    consulta_ids = """
SELECT idComponente, componente, metrica, idMetrica, case when limiteMinimo is null then 2147000000 else limiteMinimo end as limiteMinimo, case when limiteMaximo is null then 2147000000 else limiteMaximo end as limiteMaximo, terminal, setor, idMaquina, especificacao from componente join maquina on idMaquina = fkMaquina join metrica on idComponente = fkComponente join filial on idFilial = fkFilial where idMaquina = %s;
        """
    cursor.execute(consulta_ids, (idComputador,))
    resultados = cursor.fetchall()
    dados = [['terminal', 'setor', 'idMaquina', 'componente', 'especificacao', 'metrica', 'valorCapturado', 'momento']]
    # Executa a consulta para obter os IDs da CPU e da Memória
    minuto = 0
    while True:
        for consulta in resultados:
            limiteMinimo = int(consulta[4])
            limiteMaximo = int(consulta[5])
            limiteMedio = (limiteMaximo+limiteMinimo)/2
            if(consulta[1] == "Processador"):
                if(consulta[2] == "porcentagemUso"):
                    cpuPorcentagemUso = psutil.cpu_percent(interval=None)
                    if(cpuPorcentagemUso >= limiteMinimo and cpuPorcentagemUso < limiteMedio):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'baixo')" % (cpuPorcentagemUso, consulta[3])
                        cursor.execute(insert)
                    if(cpuPorcentagemUso >= limiteMedio and cpuPorcentagemUso < limiteMaximo):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'alto')" % (cpuPorcentagemUso, consulta[3])
                        cursor.execute(insert)
                    if(cpuPorcentagemUso >= limiteMaximo):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'critico')" % (cpuPorcentagemUso, consulta[3])
                        cursor.execute(insert)
                    agora = datetime.now()
                    agora = agora.strftime("%Y/%m/%d %H:%M:%S")
                    dado = [consulta[6], consulta[7], consulta[8], consulta[1], consulta[9], consulta[2], cpuPorcentagemUso, agora]
                    dados.append(dado)
                elif(consulta[2] == "processos"):
                    total = 0
                    for processo in psutil.process_iter(['name']):
                         total+=1
                    agora = datetime.now()
                    agora = agora.strftime("%Y/%m/%d %H:%M:%S")
                    dado = [consulta[6], consulta[7], consulta[8], consulta[1], consulta[9], consulta[2], total, agora]
                    dados.append(dado)
                elif(consulta[2] == "tempoAtividade"):
                    boot_time = round(psutil.boot_time())
                    agora = time.time()
                    tempoLigado = int(agora - boot_time)
                    agora = datetime.now()
                    agora = agora.strftime("%Y/%m/%d %H:%M:%S")
                    dado = [consulta[6], consulta[7], consulta[8], consulta[1], consulta[9], consulta[2], tempoLigado, agora]
                    dados.append(dado)
            elif(consulta[1] == "RAM"):
                if(consulta[2] == "porcentagemUso"):
                    ramPorcentagemUso = psutil.virtual_memory().percent
                    if(ramPorcentagemUso >= limiteMinimo and ramPorcentagemUso < limiteMedio):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'baixo')" % (ramPorcentagemUso, consulta[3])
                        cursor.execute(insert)
                    if(ramPorcentagemUso >= limiteMedio and ramPorcentagemUso < limiteMaximo):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'alto')" % (ramPorcentagemUso, consulta[3])
                        cursor.execute(insert)
                    if(ramPorcentagemUso >= limiteMaximo):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'critico')" % (ramPorcentagemUso, consulta[3])
                        cursor.execute(insert)
                    agora = datetime.now()
                    agora = agora.strftime("%Y/%m/%d %H:%M:%S")
                    dado = [consulta[6], consulta[7], consulta[8], consulta[1], consulta[9], consulta[2], ramPorcentagemUso, agora]
                    dados.append(dado)
            elif(consulta[1] == "Armazenamento"):
                if(consulta[2] == "porcentagemUso"):
                    isLinux = psutil.LINUX
                    if isLinux:
                        discoPorcentagemUso = psutil.disk_usage('/').percent
                    else:
                        discoPorcentagemUso = psutil.disk_usage('C:/').percent
                    if(discoPorcentagemUso >= limiteMinimo and discoPorcentagemUso < limiteMedio):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'baixo')" % (discoPorcentagemUso, consulta[3])
                        cursor.execute(insert)
                    if(discoPorcentagemUso >= limiteMedio and discoPorcentagemUso < limiteMaximo):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'alto')" % (discoPorcentagemUso, consulta[3])
                        cursor.execute(insert)
                    if(discoPorcentagemUso >= limiteMaximo):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'critico')" % (discoPorcentagemUso, consulta[3])
                        cursor.execute(insert)
                    agora = datetime.now()
                    agora = agora.strftime("%Y/%m/%d %H:%M:%S")
                    dado = [consulta[6], consulta[7], consulta[8], consulta[1], consulta[9], consulta[2], discoPorcentagemUso, agora]
                    dados.append(dado)
            elif(consulta[1] == "Rede"):
                if(consulta[2] == "velocidadeDownload"):
                    redeDownload1 = psutil.net_io_counters().bytes_sent
                    time.sleep(2)
                    redeDownload2 = psutil.net_io_counters().bytes_sent
                    redeDownload = redeDownload2 - redeDownload1
                    if(redeDownload >= limiteMinimo and redeDownload < limiteMedio):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'baixo')" % (redeDownload, consulta[3])
                        cursor.execute(insert)
                    if(redeDownload >= limiteMedio and redeDownload < limiteMaximo):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'alto')" % (redeDownload, consulta[3])
                        cursor.execute(insert)
                    if(redeDownload >= limiteMaximo):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'critico')" % (redeDownload, consulta[3])
                        cursor.execute(insert)
                    agora = datetime.now()
                    agora = agora.strftime("%Y/%m/%d %H:%M:%S")
                    dado = [consulta[6], consulta[7], consulta[8], consulta[1], consulta[9], consulta[2], redeDownload, agora]
                    dados.append(dado)
                elif(consulta[2] == "velocidadeUpload"):
                    redeUpload1 = psutil.net_io_counters().bytes_recv
                    time.sleep(2)
                    redeUpload2 = psutil.net_io_counters().bytes_recv
                    redeUpload = redeUpload2 - redeUpload1
                    if(redeUpload >= limiteMinimo and redeUpload < limiteMedio):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'baixo')" % (redeUpload, consulta[3])
                        cursor.execute(insert)
                    if(redeUpload >= limiteMedio and redeUpload < limiteMaximo):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'alto')" % (redeUpload, consulta[3])
                        cursor.execute(insert)
                    if(redeUpload >= limiteMaximo):
                        insert = "INSERT INTO captura_alerta (idCapturaAlerta, valorCapturado, fkMetrica, gravidade) VALUES (default, %s, %s, 'critico')" % (redeUpload, consulta[3])
                        cursor.execute(insert)
                    agora = datetime.now()
                    agora = agora.strftime("%Y/%m/%d %H:%M:%S")
                    dado = [consulta[6], consulta[7], consulta[8], consulta[1], consulta[9], consulta[2], redeUpload, agora]
                    dados.append(dado)
                    minuto+=1
                    if(minuto == 4):
                        minuto = 1
                        agora = datetime.now()
                        agora = agora.strftime("%Y%m%d%H%M%S")
                        filename = 'data' + str(agora) + str(idComputador) + '.csv'
                        with open(filename, 'w', newline='') as csvfile:
                            csvwriter = csv.writer(csvfile)
                            csvwriter.writerows(dados)
                        s3 = boto3.client(
                            's3',
                            aws_access_key_id='aws_access_key_id',
                            aws_secret_access_key='aws_secret_access_key',
                            region_name='region_name',
                            aws_session_token='aws_session_token'
                        )                       
                        s3.upload_file(filename, 'lucasrawteste', filename)
            mydb.commit()
        time.sleep(20)




def exibirDadosComputacionais():
    print("Buscando dados computacionais...")
    numero_cpus_logicas = psutil.cpu_count(True)
    numeros_cpus_nao_logicas = psutil.cpu_count(False)
    print("\nVocê possui %d núcleos de CPUs (lógicas inclusas) e %d CPUs (lógicas não inclusas)" % (
    numero_cpus_logicas, numeros_cpus_nao_logicas))
    frequencia_cpu = psutil.cpu_freq()
    frequencia_maxima_cpu = frequencia_cpu.max
    frequencia_atual_cpu = frequencia_cpu.current
    print("A frequência máxima da sua CPU é %.2f GHz\nA frequência atual da sua CPU é %.2f GHz" % (
    (frequencia_maxima_cpu / 1000), (frequencia_atual_cpu / 1000)))

    memoria_virtual = psutil.virtual_memory()
    memoria_total = memoria_virtual.total
    print("A memória RAM total do sistema é %.2f GB" % (memoria_total / (1024 ** 3)))


    discos = psutil.disk_partitions()
    # Exibindo informações de todos os discos
    for disco in discos:
        try:
            print("Disco encontrado com montagem em %s com o Filesystem %s possui %.2f GB de tamanho\n" % (
            disco.device, disco.fstype, (psutil.disk_usage(disco.device).total / (1024 ** 3))))
        except Exception as e:
            print("Erro ao buscar disco: %s" % e)


try:
    mydb = mysql.connector.MySQLConnection(
        host="127.0.0.1",
        user="root",
        password="urubu100",
        database="innovaair",
        auth_plugin="mysql_native_password",
        port=3307)
    
    cursor = mydb.cursor()

except Error as e:
    print("Houve um problema com a comunicação com o banco de dados\n")
    print(e)
    exit(0)