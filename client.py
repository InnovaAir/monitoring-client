import mysql.connector
from mysql.connector import Error
import psutil
import time
import socket, platform
from datetime import datetime;

# mycursor = mydb.cursor()
def menuInicial():
    saiu = False
    while (saiu == False):
        opcao = int(
            input("Bem vindo ao client InnovaAir, digite uma opção para prosseguir:\n1. Realizar login\n2. Sair\n"))
        match (opcao):
            case 1:
                email = input("Informe seu e-mail:\n")
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


def home():
    saiu = False
    while (saiu == False):
        opcao = int(input(
            "Bem vindo ao client InnovaAir, digite uma opção para prosseguir: \n1. Iniciar captura de dados computacionais.\n2. Verificar informações do computador\n3. Sair\n"))
        match (opcao):
            case 1:
                capturarDados()
            case 2:
                exibirDadosComputacionais()
            case 3:
                print("Até mais :)")
                saiu = True
                exit()


def get_first_mac_address():
    interfaces = psutil.net_if_addrs()

    for interfaces, addresses in interfaces.items():
        for address in addresses:
            if address.family == psutil.AF_LINK:
                return address.address

    return None


def cadastrarMaquina():
    hostname = socket.gethostname()
    os = platform.system()
    os_version = platform.version()
    os_final = os + " " + os_version
    architecture = platform.machine()
    apelido = input('Digite um apelido para a máquina:\n')
    mac_address = get_first_mac_address()
    print('Cadastrando a máquina no banco de dados:\nApelido: %s\nSistema Operacional: %s\nHostname: %s\nArquitetura: %s\nEndereço MAC %s' % (apelido, os_final, hostname, architecture, mac_address))
    consulta = "INSERT INTO Computador(apelido, endMac, sistemaOperacional, hostname, arquitetura, fkFilial) VALUES ('%s', '%s', '%s', '%s', '%s', 1)" % (apelido, mac_address,os_final, hostname, architecture)
    cursor.execute(consulta)
    mydb.commit()
    print(cursor.rowcount, "registros inseridos.")
    print("Computador cadastrado com sucesso")

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
                else:
                    print("Máquina ainda não cadastrada!")
                    cadastrarMaquina()
    return False


def capturarDados():
    print("Verificando se a máquina já está cadastrada no banco de dados...")
    cadastrada = verificarMaquinaCadastrada()
    if (cadastrada):
        while True:
            cpuPercent = format(psutil.cpu_percent())
            memVirtualPerc = format(psutil.virtual_memory().percent)
            redeBytesSent = psutil.net_io_counters().bytes_sent
            redeBytesRecv = psutil.net_io_counters().bytes_recv
            disco = psutil.disk_usage("C://").used / 1e+9
            # Isso pode servir para ver se um computador de check-in ta transmitindo os dados de maneira correta
            redePacksSent = psutil.net_io_counters().packets_sent
            redePacksRecv = psutil.net_io_counters().packets_recv
            mediaSent = redeBytesSent / redePacksSent if redePacksSent > 0 else 0
            mediaRecv = redeBytesRecv / redePacksRecv if redePacksRecv > 0 else 0
            uptimeSeconds = time.time() - psutil.boot_time()
            # o time.time() pega o número de segundos que se passaram desde o "start" da época.
            # a época seria 1º de janeiro de 1970, à meia-noite UTC (Coordinated Universal Time). Esse momento é conhecido como Unix Epoch.
            # A escolha do 1º de janeiro de 1970 como a "época" tem a ver com a história do Unix, um sistema operacional criado nos anos 60 e 70. Aqui está um resumo:
            # Ao usar segundos desde a época, o Unix poderia calcular facilmente o tempo com um número inteiro. Isso simplifica o uso e a precisão do tempo em sistemas com capacidade limitada de armazenamento e processamento (o que era uma preocupação no início da computação).
            # o psutil.boot_time() retorna exatamente o momento em que o sistema foi iniciado ou reiniciado. Esse é o ponto de referência para medir quanto tempo o seu computador ficou ligado sem ser reiniciado.
            uptimeHours = int(uptimeSeconds / 3600)
            uptimeMinutes = int((uptimeSeconds % 3600) / 60)
            uptimeSeconds = int(uptimeSeconds % 60)

            totalHoras = format(f"{uptimeHours}h {uptimeMinutes}m {uptimeSeconds}s")
            mediaSentf = format(f"{mediaSent:.2f}")
            mediaRecvf = format(f"{mediaRecv:.2f}")
            # % ajuda a pegar o "resto" (quantos segundos ou minutos restaram).
            # 1 hora = 3600 segundos
            # 1 minuto = 60 segundos

            # o if aqui serve para, caso a quantidade de pacotes for 0, a conta não dar erro !! já que divir algo por 0 não da muito certo skjdksjd

            print("-------------------------------------------------------------")
            print(f"Tamanho médio dos pacotes enviados: {mediaSent:.2f} bytes")
            print(f"Tamanho médio dos pacotes recebidos: {mediaRecv:.2f} bytes")
            print(f"Porcentagem de memória vitual: {memVirtualPerc}%")
            print(f"Porcentagem de cpu sendo usada: {cpuPercent}%")
            print(f"Tempo de Atividade: {totalHoras}")
            print(f"Uso do disco: {disco:.2f}")
            print("-------------------------------------------------------------")

            # sql = "INSERT INTO InfosComputer (fkComputador, pacotesRecv, pacotesEnv, memVirtual, cpuUsada, tempoAtvd, discoUso, horarioLog) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            # print(f"Porcentagem de cpu sendo usada: {cpuPercent}%")
            # val = ("1", mediaSent, mediaRecv, memVirtualPerc, cpuPercent, totalHoras, disco, datetime.now())

            # mycursor.execute(sql,val)

            # mydb.commit()

            # print(mycursor.rowcount, "record inserted.")

            time.sleep(1)
        # print(redeBytesSent)
        # print(redeBytesRecv)
        # print(redePacksSent)
        # print(redePacksRecv)

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






