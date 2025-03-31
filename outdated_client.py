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
            input("Bem vindo ao client InnovaAir, digite uma opção para prosseguir:\n1. Realizar login\n2. Sair\n"))
        match (opcao):
            case 1:
                email = input("\nInforme seu e-mail:\n")
                senha = input("Informe sua senha:\n")
                if (login(email, senha)):
                    home()
                    saiu = True
                else:
                    print("Login ou senha inválidos, tente novamente!")
            case 2:
                print("Até mais :)")
                saiu = True
                exit()

def login(email, senha):
    if email == 'teste@email.com' and senha == '123':
        return True
    else:
        return False
    # validacao no banco de dados
    # Consulta SQL para verificar se o usuário existe com o email e senha fornecidos
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
                consulta = "SELECT idComputador FROM Computador WHERE numeroSeriePlacaMae = '%s'" % numeroSeriePlacaMae
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
    # resgatando frequencia da CPU
    frequencia_cpu = psutil.cpu_freq()
    frequencia = frequencia_cpu.max
    #resgatando cores
    cores = psutil.cpu_count(True)

    consulta = "INSERT INTO CPU (modelo, frequencia, cores, fkComputador) VALUES ('%s', %.2f, %d, %d)" % (modelo, frequencia, cores, fkComputador)
    print("Executando a consulta SQL: '%s'", consulta)
    cursor.execute(consulta)
    mydb.commit()
    id_cpu_cadastrada = cursor._last_insert_id
    print("\nCPU de id %d cadastrado\n" % id_cpu_cadastrada)

def cadastrarMemoria(fkComputador):
    print("\nCadastrando memória...")
    memoria_virtual = psutil.virtual_memory()
    memoria_total = memoria_virtual.total

    consulta = "INSERT INTO Memoria (tamanho, fkComputador) VALUES (%.2f, %d)" % ((memoria_total / (1024**3)), fkComputador)
    print("Executando a consulta SQL: '%s'", consulta)
    cursor.execute(consulta)
    mydb.commit()

    id_memoria_cadastrada = cursor._last_insert_id
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
                    INSERT INTO Disco (capacidade, montagem, sistemaArquivos, fkComputador)
                    VALUES (%s, %s, %s, %s)
                    """
                    parametros = (capacidade, disco_nome, sistema_arquivos, fkComputador)

                    print(f"Executando a consulta para cadastrar o disco: {disco_nome}...")

                    cursor.execute(consulta, parametros)
                    mydb.commit()

                    id_disco_cadastrado = cursor.lastrowid
                    print(f"Disco de id {id_disco_cadastrado} cadastrado com sucesso no macOS!\n")
                    
        except Exception as e:
            print(f"Erro ao buscar ou cadastrar discos no macOS: {e}")
    
    elif system == "Windows":  # Se for Windows (verificando versão)
        try:
            if "10" in windows_version:  # Caso seja Windows 10
                print("Sistema operacional: Windows 10")
                # Usando 'wmic' para Windows 10
                result = subprocess.check_output(
                    'wmic baseboard get serialnumber',
                    shell=True,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
                serial = result.strip().split("\n")[-1].strip()
                print(f"Número de série da placa-mãe no Windows 10: {serial}")

            elif "11" in windows_version:  
                print("Sistema operacional: Windows 11")
                # Usando PowerShell para Windows 11
                result = subprocess.check_output(
                    'powershell Get-CimInstance -ClassName Win32_BaseBoard | Select-Object -ExpandProperty SerialNumber',
                    shell=True,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
                serial = result.strip()
                print(f"Número de série da placa-mãe no Windows 11: {serial}")
            else:
                print("Sistema operacional não identificado corretamente.")
                serial = None

            # Agora, coletando os discos no Windows usando psutil
            discos = psutil.disk_partitions(all=False)
            for disco in discos:
                try:
                    # Verifica se o ponto de montagem está válido
                    if not disco.mountpoint or not disco.fstype:
                        print(f"Disco em {disco.device} com montagem {disco.mountpoint} e sistema de arquivos {disco.fstype} é inválido. Ignorando.")
                        continue

                    # Obtém informações sobre o uso do disco
                    uso_disco = psutil.disk_usage(disco.mountpoint)

                    # Extrai as informações necessárias
                    capacidade = uso_disco.total / (1024 ** 3)  # Converte para GB
                    montagem = disco.mountpoint
                    sistema_arquivos = disco.fstype

                    # Verifica se a capacidade do disco é válida
                    if capacidade <= 0:
                        print(f"O disco em {montagem} possui capacidade inválida ({capacidade} GB). Ignorando.")
                        continue

                    # Consulta SQL para inserir as informações no banco de dados
                    consulta = """
                    INSERT INTO Disco (capacidade, montagem, sistemaArquivos, fkComputador)
                    VALUES (%s, %s, %s, %s)
                    """
                    parametros = (capacidade, montagem, sistema_arquivos, fkComputador)

                    # Executa a consulta no banco de dados
                    print(f"Executando a consulta para cadastrar o disco em {montagem}...")

                    cursor.execute(consulta, parametros)
                    mydb.commit()

                    id_disco_cadastrado = cursor.lastrowid
                    print(f"Disco de id {id_disco_cadastrado} cadastrado com sucesso!\n")
                except Exception as e:
                    print(f"Erro ao cadastrar o disco: {e}")
        
        except Exception as e:
            print(f"Erro ao obter o número de série da placa-mãe ou ao buscar discos no Windows: {e}")

    else:
        # Para sistemas não-macOS, usa-se psutil para capturar as partições
        discos = psutil.disk_partitions(all=False)

        for disco in discos:
            try:
                # Verifica se o ponto de montagem está válido
                if not disco.mountpoint or not disco.fstype:
                    print(f"Disco em {disco.device} com montagem {disco.mountpoint} e sistema de arquivos {disco.fstype} é inválido. Ignorando.")
                    continue

                # Obtém informações sobre o uso do disco
                uso_disco = psutil.disk_usage(disco.mountpoint)

                # Extrai as informações necessárias
                capacidade = uso_disco.total / (1024 ** 3)  # Converte para GB
                montagem = disco.mountpoint
                sistema_arquivos = disco.fstype

                # Verifica se a capacidade do disco é válida
                if capacidade <= 0:
                    print(f"O disco em {montagem} possui capacidade inválida ({capacidade} GB). Ignorando.")
                    continue

                # Consulta SQL para inserir as informações no banco de dados
                consulta = """
                INSERT INTO Disco (capacidade, montagem, sistemaArquivos, fkComputador)
                VALUES (%s, %s, %s, %s)
                """
                parametros = (capacidade, montagem, sistema_arquivos, fkComputador)

                # Executa a consulta no banco de dados
                print(f"Executando a consulta para cadastrar o disco em {montagem}...")

                cursor.execute(consulta, parametros)
                mydb.commit()

                id_disco_cadastrado = cursor.lastrowid
                print(f"Disco de id {id_disco_cadastrado} cadastrado com sucesso!\n")
            except Exception as e:
                print(f"Erro ao cadastrar o disco: {e}")

def cadastrarMaquina():
    hostname = socket.gethostname()
    os = platform.system()
    os_version = platform.version()
    os_final = os + " " + os_version
    architecture = platform.machine()
    apelido = input('Digite um apelido para a máquina:\n')
    numero_serie = obterSerialPlacaMae()
    print('\nCadastrando a máquina no banco de dados:\nApelido: %s\nSistema Operacional: %s\nHostname: %s\nArquitetura: %s\nEndereço MAC %s' % (apelido, os_final, hostname, architecture, numero_serie))
    consulta = "INSERT INTO Computador(apelido, numeroSeriePlacaMae, sistemaOperacional, hostname, arquitetura, fkFilial) VALUES ('%s', '%s', '%s', '%s', '%s', 1)" % (apelido, numero_serie,os_final, hostname, architecture)
    cursor.execute(consulta)
    mydb.commit()
    id_Computador_cadastrado = cursor._last_insert_id
    print("Computador de id %d cadastrado" % id_Computador_cadastrado)
    print("\nCadastrando componentes do Computador...")
    cadastrarCPU(id_Computador_cadastrado)
    cadastrarMemoria(id_Computador_cadastrado)
    cadastrarDiscos(id_Computador_cadastrado)

def verificarMaquinaCadastrada():
                consulta = "SELECT * FROM Computador WHERE numeroSeriePlacaMae = '%s'" % obterSerialPlacaMae()
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
        SELECT 
            CPU.idCpu, 
            Memoria.idMemoria
        FROM 
            Computador
        LEFT JOIN 
            CPU ON Computador.idComputador = CPU.fkComputador
        LEFT JOIN 
            Memoria ON Computador.idComputador = Memoria.fkComputador
        WHERE 
            Computador.idComputador = %s;
        """

    # Executa a consulta para obter os IDs da CPU e da Memória
    cursor.execute(consulta_ids, (idComputador,))
    resultado_ids = cursor.fetchone()

    id_cpu = None
    id_memoria = None

    if resultado_ids:
        id_cpu, id_memoria = resultado_ids
        print(f"ID da CPU associada: {id_cpu}")
        print(f"ID da Memória associada: {id_memoria}")
        while True:

            #CPU info
            cpuPercent = psutil.cpu_percent()
            #Memoria info
            memVirtualPerc = psutil.virtual_memory().percent
            memVirtualFree = psutil.virtual_memory().free / (1024**3)
            memVirtualUsed = psutil.virtual_memory().used / (1024**3)



            print("-------------------------------------------------------------")
            print(f"Porcentagem de memória vitual: {memVirtualPerc}%")
            print(f"GB's de memória livre: {memVirtualFree}GB")
            print(f"GB's de memória em uso: {memVirtualUsed}GB1"
                  f"")
            print(f"Porcentagem de cpu sendo usada: {cpuPercent}%")
            print("-------------------------------------------------------------")

            # Preparando consultas
            consulta_cpu = "INSERT INTO MetricaCPU (percentualUso, fkCpu) VALUES (%.2f, %d)" % (cpuPercent, id_cpu)
            consulta_memoria = "INSERT INTO MetricaMemoria (percentualUso, quantidadeLivre, quantidadeUsada, fkMemoria) VALUES (%.2f, %.2f, %.2f, %d)" % (memVirtualPerc, memVirtualFree, memVirtualUsed, id_memoria)
            print("Executando consulta: %s\nExecutando consulta: %s" % (consulta_cpu, consulta_memoria))

            cursor.execute(consulta_cpu)
            mydb.commit()
            cursor.execute(consulta_memoria)
            mydb.commit()
            time.sleep(3)


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
        user="superestagiario",
        password="urubu100",
        database="innovair"
    )
    cursor = mydb.cursor()

    menuInicial()
except Error as e:
    print("Houve um problema com a comunicação com o banco de dados\n")
    print(e)
    exit(0)
else:
    print("Conexão estabelecida com banco de dados... Prosseguindo com execução")






