import mysql.connector
from mysql.connector import Error
import psutil
import time
import subprocess
import socket, platform, cpuinfo

def menuInicial():
    saiu = False
    while (saiu == False):
        opcao = int(
            input("Bem vindo ao client InnovaAir, digite uma opção para prosseguir:\n1. Rodar sistema\n2. Sair\n"))
        match (opcao):
            case 1:
                home()
                # email = input("\nInforme seu e-mail:\n")
                # senha = input("Informe sua senha:\n")
                # if (login(email, senha)):
                #     home()
                #     saiu = True
                # else:
                #     print("Login ou senha inválidos, tente novamente!")
                #     return
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
                print("Executando a consulta: %s" % consulta)

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

def cadastrarCPU(fkComputador):
    print("\nCadastrando CPU...")
    # capturando informações da CPU
    # resgatando o modelo da CPU (atributo brand_raw do objeto de resposta)
    modelo =  cpuinfo.get_cpu_info()['brand_raw']

    consulta = "INSERT INTO componente (componente, especificacao, fkMaquina) VALUES ('%s', '%s', %s)" % ('Processador', modelo, fkComputador)
    print("Executando a consulta SQL: '%s'", consulta)
    cursor.execute(consulta)
    mydb.commit()
    id_cpu_cadastrada = cursor._last_insert_id
    #Registrando métricas
    limiteMin = input("Insira o limite mínimo para a captura de dados da porcentagem de uso dessa CPU: ")
    limiteMax = input("Insira o limite máximo para a captura de dados da porcentagem de uso dessa CPU: ")
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('porcentagemUso', %s, %s, %s)" % (limiteMin, limiteMax, id_cpu_cadastrada)
    cursor.execute(consulta)
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('frequencia', null, null, %s)" % (id_cpu_cadastrada)
    cursor.execute(consulta)
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('processos', null, null, %s)" % (id_cpu_cadastrada)
    cursor.execute(consulta)
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('tempoAtividade', null, null, %s)" % (id_cpu_cadastrada)
    cursor.execute(consulta)
    mydb.commit()
    fkMetrica = cursor._last_insert_id
    frequencia = psutil.cpu_freq().max
    consulta = "INSERT INTO captura_historico (valorCapturado, fkMetrica) VALUES (%s, %s)" % (frequencia, fkMetrica)
    cursor.execute(consulta)
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
        especificacao = especificacao.replace("\n","").replace(" ","").replace("Manufacturer:", "")[12:]
    consulta = "INSERT INTO componente (componente, especificacao, fkMaquina) VALUES ('%s', '%s', %s)" % ('RAM', especificacao, fkComputador)
    print("Executando a consulta SQL: '%s'", consulta)
    cursor.execute(consulta)
    mydb.commit()

    id_memoria_cadastrada = cursor._last_insert_id
    #Registrando métricas
    limiteMin = input("Insira o limite mínimo para a captura de dados da porcentagem de uso dessa RAM: ")
    limiteMax = input("Insira o limite máximo para a captura de dados da porcentagem de uso dessa RAM: ")
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('porcentagemUso', %s, %s, %s)" % (limiteMin, limiteMax, id_memoria_cadastrada)
    cursor.execute(consulta)
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('total', null, null, %s)" % (id_memoria_cadastrada)
    cursor.execute(consulta)
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('processos', null, null, %s)" % (id_memoria_cadastrada)
    cursor.execute(consulta)
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

                    print(f"Executando a consulta para cadastrar o disco: {disco_nome}...")

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
                limiteMin = input("Insira o limite mínimo para a captura de dados da porcentagem de uso desse armazenamento: ")
                limiteMax = input("Insira o limite máximo para a captura de dados da porcentagem de uso desse armazenamento: ")
                consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('porcentagemUso', %s, %s, %s)" % (limiteMin, limiteMax, id_disco_cadastrado)
                cursor.execute(consulta)
                consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('total', %s, %s, %s)" % (limiteMin, limiteMax, id_disco_cadastrado)
                cursor.execute(consulta)
                mydb.commit()
                fkMetrica = cursor._last_insert_id
                valorCaptura = psutil.disk_usage('C:/').total
                consulta = "INSERT INTO captura_historico (valorCapturado, fkMetrica) VALUES (%s, %s)" % (valorCaptura, fkMetrica)
                cursor.execute(consulta)
                mydb.commit()
                print(f"Disco de id {id_disco_cadastrado} cadastrado com sucesso!\n")
            except Exception as e:
                print(f"Erro ao cadastrar o disco: {e}")
        
        except Exception as e:
            print(f"Erro ao obter o número de série da placa-mãe ou ao buscar discos no Windows: {e}")

def cadastrarRede(fkComputador):
    system = platform.system()
    if system == "Windows":
        especificacao = subprocess.check_output('wmic nic get Name', shell=True, text=True)
        especificacao = especificacao.replace(" ","").split("\n")[2]
    elif system == "Linux":
        especificacao = subprocess.check_output('lspci | grep -i ethernet', shell=True, text=True)
    consulta = "INSERT INTO componente (componente, especificacao, fkMaquina) VALUES ('%s', '%s', %s)" % ('Rede', especificacao, fkComputador)
    print("Executando a consulta SQL: '%s'", consulta)
    cursor.execute(consulta)
    mydb.commit()
    redeCadastrado = cursor._last_insert_id
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('velocidadeDownload', null, null, %s)" % (redeCadastrado)
    cursor.execute(consulta)
    consulta = "INSERT INTO metrica (metrica, limiteMinimo, limiteMaximo, fkComponente) VALUES ('velocidadeUpload', null, null, %s)" % (redeCadastrado)
    cursor.execute(consulta)
    mydb.commit()
    print(f"Chip de rede de id {redeCadastrado} cadastrado com sucesso!\n")
    

def cadastrarMaquina():
    hostname = socket.gethostname()
    endereco_mac = psutil.net_if_addrs()["Ethernet"][0].address
    numero_serie = obterSerialPlacaMae()
    print('\nCadastrando a máquina no banco de dados:\nNumero Serial: %s\nHostname: %s\nEndereço MAC %s' % (numero_serie, endereco_mac, hostname))
    fkFilial = int(input("Insira o id da filial a qual essa máquina pertence: "))
    consulta = "INSERT INTO maquina(numeroSerial, enderecoMac, hostname, fkFilial) VALUES ('%s', '%s', '%s', %s)" % (numero_serie, endereco_mac, hostname, fkFilial)
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
                print("Executando a consulta: %s" % consulta)
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
SELECT idComponente, componente, metrica, idMetrica from componente join maquina on idMaquina = fkMaquina join metrica on idComponente = fkComponente where idMaquina = %s
        """
    cursor.execute(consulta_ids, (idComputador,))
    resultados = cursor.fetchall()

    # Executa a consulta para obter os IDs da CPU e da Memória
    while True:
        for consulta in resultados:
            if(consulta[1] == "Processador"):
                if(consulta[2] == "porcentagemUso"):
                    cpuPorcentagemUso = psutil.cpu_percent(interval=None)
                    insert = "INSERT INTO captura_historico (idCapturaHistorico, valorCapturado, fkMetrica) VALUES (default, %s, %s)" % (cpuPorcentagemUso, consulta[3])
                    cursor.execute(insert)
                elif(consulta[2] == "processos"):
                    total = 0
                    for processo in psutil.process_iter(['name']):
                         total+=1
                    insert = "INSERT INTO captura_historico (idCapturaHistorico, valorCapturado, fkMetrica) VALUES (default, '%s', %s)" % (total, consulta[3])
                    cursor.execute(insert)
                elif(consulta[2] == "tempoAtividade"):
                    boot_time = round(psutil.boot_time())
                    agora = time.time()
                    tempoLigado = int(agora - boot_time)
                    insert = "INSERT INTO captura_historico (idCapturaHistorico, valorCapturado, fkMetrica) VALUES (default, %s, %s)" % (tempoLigado, consulta[3])
                    cursor.execute(insert)
            elif(consulta[1] == "RAM"):
                if(consulta[2] == "porcentagemUso"):
                    ramPorcentagemUso = psutil.virtual_memory().percent
                    insert = "INSERT INTO captura_historico (idCapturaHistorico, valorCapturado, fkMetrica) VALUES (default, %s, %s)" % (ramPorcentagemUso, consulta[3])
                    cursor.execute(insert)
            elif(consulta[1] == "Armazenamento"):
                if(consulta[2] == "porcentagemUso"):
                    discoPorcentagemUso = psutil.disk_usage('C:/').percent
                    insert = "INSERT INTO captura_historico (idCapturaHistorico, valorCapturado, fkMetrica) VALUES (default, %s, %s)" % (discoPorcentagemUso, consulta[3])
                    cursor.execute(insert)
            elif(consulta[1] == "Rede"):
                if(consulta[2] == "velocidadeDownload"):
                    redeDownload1 = psutil.net_io_counters().bytes_sent
                    time.sleep(2)
                    redeDownload2 = psutil.net_io_counters().bytes_sent
                    redeDownload = redeDownload2 - redeDownload1
                    insert = "INSERT INTO captura_historico (idCapturaHistorico, valorCapturado, fkMetrica) VALUES (default, %s, %s)" % (redeDownload, consulta[3])
                    cursor.execute(insert)
                elif(consulta[2] == "velocidadeUpload"):
                    redeUpload1 = psutil.net_io_counters().bytes_recv
                    time.sleep(2)
                    redeUpload2 = psutil.net_io_counters().bytes_recv
                    redeUpload = redeUpload2 - redeUpload1
                    insert = "INSERT INTO captura_historico (idCapturaHistorico, valorCapturado, fkMetrica) VALUES (default, %s, %s)" % (redeUpload, consulta[3])
                    cursor.execute(insert)
            mydb.commit()
        time.sleep(10)




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
    mydb = mysql.connector.connect(
        host="localhost",
        user="innova_client",
        password="Innovaair@123",
        database="innovaair"
    )
    cursor = mydb.cursor()

    menuInicial()
except Error as e:
    print("Houve um problema com a comunicação com o banco de dados\n")
    print(e)
    exit(0)






