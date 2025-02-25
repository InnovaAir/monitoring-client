import mysql.connector
from mysql.connector import Error
import psutil
import time
import socket, platform, cpuinfo
from datetime import datetime;

# mycursor = mydb.cursor()
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
    # validacao no banco de dados

    return True


def resgatarIdComputador():
    # Recupera as informações de rede e endereços MAC
    net_info = psutil.net_if_addrs()

    for interface, addresses in net_info.items():
        for address in addresses:
            if address.family == psutil.AF_LINK:
                mac_address = address.address
                print(f"Verificando MAC Address: {mac_address}")

                # Consulta o banco de dados para encontrar o computador com o MAC Address
                consulta = "SELECT idComputador FROM computador WHERE endMac = '%s'" % mac_address
                cursor.execute(consulta)
                print("Executando a consulta: %s" % consulta)

                # Recupera o resultado da consulta
                myresult = cursor.fetchall()

                if len(myresult) > 0:
                    # Se o computador for encontrado, retorna o ID
                    id_computador = myresult[0][0]  # Pega o primeiro resultado e a primeira coluna (idComputador)
                    print(f"Máquina com MAC Address {mac_address} encontrada! ID: {id_computador}")
                    return id_computador
                else:
                    print(f"Máquina com MAC Address {mac_address} ainda não cadastrada!")

    print("Nenhum computador encontrado com os MAC Addresses disponíveis.")
    return None

def home():
    saiu = False
    while (saiu == False):
        opcao = int(input(
            "\nBem vindo ao client InnovaAir, digite uma opção para prosseguir: \n1. Iniciar captura de dados computacionais.\n2. Verificar informações do computador\n3. Sair\n"))
        match (opcao):
            case 1:
                print("Verificando se a máquina já está cadastrada no banco de dados...")
                cadastrada = verificarMaquinaCadastrada()
                if (cadastrada):
                    id_computador = resgatarIdComputador()
                    capturarDados(id_computador)
            case 2:
                exibirDadosComputacionais()
            case 3:
                print("\nAté mais :)")
                saiu = True
                exit()


def get_first_mac_address():
    interfaces = psutil.net_if_addrs()

    for interfaces, addresses in interfaces.items():
        for address in addresses:
            if address.family == psutil.AF_LINK:
                return address.address

    return None

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

    discos = psutil.disk_partitions(all=True)

    for disco in discos:
        # Obtém informações sobre o uso do disco
        uso_disco = psutil.disk_usage(disco.mountpoint)

        # Extrai as informações necessárias
        capacidade = uso_disco.total / (1024 ** 3)  # Converte para GB
        montagem = disco.mountpoint
        sistema_arquivos = disco.fstype

        consulta = """
        INSERT INTO Disco (capacidade, montagem, sistemaArquivos, fkComputador)
        VALUES (%.2f, "'%s'", '%s', %d)
        """ % (capacidade, montagem, sistema_arquivos, fkComputador)

        print("Executando a consulta: '%s'" % consulta)

        cursor.execute(consulta)
        mydb.commit()

        id_disco_cadastrado = cursor.lastrowid
        print("Disco de id %d cadastrado\n" % id_disco_cadastrado)


def cadastrarMaquina():
    hostname = socket.gethostname()
    os = platform.system()
    os_version = platform.version()
    os_final = os + " " + os_version
    architecture = platform.machine()
    apelido = input('Digite um apelido para a máquina:\n')
    mac_address = get_first_mac_address()
    print('\nCadastrando a máquina no banco de dados:\nApelido: %s\nSistema Operacional: %s\nHostname: %s\nArquitetura: %s\nEndereço MAC %s' % (apelido, os_final, hostname, architecture, mac_address))
    consulta = "INSERT INTO Computador(apelido, endMac, sistemaOperacional, hostname, arquitetura, fkFilial) VALUES ('%s', '%s', '%s', '%s', '%s', 1)" % (apelido, mac_address,os_final, hostname, architecture)
    cursor.execute(consulta)
    mydb.commit()
    id_computador_cadastrado = cursor._last_insert_id
    print("Computador de id %d cadastrado" % id_computador_cadastrado)
    print("\nCadastrando componentes do computador...")
    cadastrarCPU(id_computador_cadastrado)
    cadastrarMemoria(id_computador_cadastrado)
    cadastrarDiscos(id_computador_cadastrado)

def verificarMaquinaCadastrada():
    # recuperando MAC Address
    net_info = psutil.net_if_addrs()
    for interface, addresses in net_info.items():
        for address in addresses:
            if address.family == psutil.AF_LINK:
                consulta = "SELECT * FROM computador WHERE endMac = '%s'" % address.address
                cursor.execute(consulta)
                print("Executando a consulta: %s" % consulta)
                myresult = cursor.fetchall()
                if (len(myresult) > 0):
                    print("Máquina com MAC Address %s encontrada!" % address.address)
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
            consulta_cpu = "INSERT INTO metricaCPU (percentualUso, fkCpu) VALUES (%.2f, %d)" % (cpuPercent, id_cpu)
            consulta_memoria = "INSERT INTO metricaMemoria (percentualUso, quantidadeLivre, quantidadeUsada, fkMemoria) VALUES (%.2f, %.2f, %.2f, %d)" % (memVirtualPerc, memVirtualFree, memVirtualUsed, id_memoria)
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
        print("Disco encontrado com montagem em %s com o Filesystem %s possui %.2f GB de tamanho\n" % (
        disco.device, disco.fstype, (psutil.disk_usage(disco.device).total / (1024 ** 3))))


try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="pythoncollector",
        password="pythonklyn123",
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






