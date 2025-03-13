from datetime import datetime

import mysql.connector
from mysql.connector import Error
import psutil
import time

def verificaPossuiMetricas(idComputador):
    consulta = "SELECT * from Regra where fkComputador = %d" % idComputador
    cursor.execute(consulta)
    print("Executando a consulta: %s" % consulta)

    # Recupera o resultado da consulta
    myresult = cursor.fetchall()

    if len(myresult) > 0:
        # Se as métricas forem encontradas, serão exibidas
        metricas = myresult[0][0]
        print(f"Métricas encontradas para a máquina de ID {idComputador}: {metricas}\n")
        return True
    else:
        print(f"Métricas não encontrada para essa máquina!\n")
        return False

def exibirTodasMetricas():
    consulta = "SELECT * from Metrica"
    cursor.execute(consulta)
    myresult = cursor.fetchall()
    # Percorrendo o vetor de métricas
    for metrica in myresult:
        print("""
           ID da métrica: %d
           Componente da métrica: %s
           Unidade de medida da métrica: %s
           Nome da métrica: %s
           """ % (metrica[0], metrica[1], metrica[2], metrica[3]))
    return myresult


def exibirMetricas(idComputador):
    consulta = "SELECT idMetrica, nomeComponente, unidadeMedida, nomeMetrica from Regra JOIN Metrica ON Metrica.idMetrica = MetricaPorComputador.fkMetrica WHERE fkComputador = %s" % idComputador
    cursor.execute(consulta)
    myresult = cursor.fetchall()
    # Percorrendo o vetor de métricas
    print("Métricas do computador de ID: %d" % idComputador)
    for metrica in myresult:
        print("""
               ID da métrica: %d
               Componente da métrica: %s
               Unidade de medida da métrica: %s
               Nome da métrica: %s
               """ % (metrica[0], metrica[1], metrica[2], metrica[3]))
    return myresult

def cadastrarMetricas(idComputador):


    while (True):
        opcao = int(input("""
        Cadastro de métricas - Digite uma opção
        1. Seguir modelo padrão de métricas
        2. Escolher métricas específicas
        3. Ver métricas cadastradas
        4. Sair
        """))

        match (opcao):
            case 1:
                # Cadastrar métricas padrão
                print("Cadastrando métricas padrões...")
                break
            case 2:
                # Solicitar métricas específicas
                print("Métricas específicas...")
            case 3:
                exibirMetricas(idComputador)
            case 4:
                break
            case _:
                print("Número inválido, tente novamente.")




  # if (verificaPossuiMetricas(idComputador) == False):
      # print("Atualmente você não possui nenhuma métrica cadastrada, selecione qual métrica deseja capturar para essa máquina")

def resgatarIdComputador(codigoMaquina):
    consulta = "SELECT idComputador FROM computador WHERE codigoMaquina = '%s'" % codigoMaquina
    cursor.execute(consulta)
    print("Executando a consulta: %s" % consulta)

    # Recupera o resultado da consulta
    myresult = cursor.fetchall()

    if len(myresult) > 0:
        # Se o computador for encontrado, retorna o ID
        id_computador = myresult[0][0]
        print(f"Máquina encontrada no sistema.ID: {id_computador}")
        return id_computador
    else:
        print(f"Máquina não encontrada!")

    return None

def capturarDados(idComputador):
    todas_metricas = exibirTodasMetricas()
    metricas_da_maquina = exibirMetricas(idComputador)

    metricasDaMaquinaNome = [metrica[3] for metrica in metricas_da_maquina]

    print("Métricas da máquina:", metricas_da_maquina)
    print("Todas as métricas:", todas_metricas)

    for metrica in todas_metricas:
        if metrica[3] in metricasDaMaquinaNome:
            print(f"Devemos registrar {metrica[3]}")
        else:
            print(f"Não devemos registrar {metrica[3]}")

    registrar_percentual_cpu = False
    registrar_percentual_memoria = False
    registrar_percentual_disco = False
    registrar_gb_memoria = False
    registrar_gb_disco = False

    for metrica in todas_metricas:
        if metrica[3] == "Percentual de uso da CPU" and metrica[3] in metricasDaMaquinaNome:
           registrar_percentual_cpu = True
        elif metrica[3] == "Percentual de uso da RAM" and metrica[3] in metricasDaMaquinaNome:
         registrar_percentual_memoria = True
        elif metrica[3] == "Percentual de uso do disco" and metrica[3] in metricasDaMaquinaNome:
           registrar_percentual_disco = True
        elif metrica[3] == "GB usados da RAM" and metrica[3] in metricasDaMaquinaNome:
           registrar_gb_memoria = True
        elif metrica[3] == "GB usados no disco" and metrica[3] in metricasDaMaquinaNome:
         registrar_gb_disco = True

    #Montando consulta
    percentual_cpu = None
    percentual_disco = None
    percentual_memoria = None
    gb_disco = None
    gb_ram = None

    if registrar_percentual_cpu:
        percentual_cpu = psutil.cpu_percent()

    if registrar_percentual_memoria:
        percentual_memoria = psutil.virtual_memory().percent

    if registrar_gb_memoria:
        gb_ram = psutil.virtual_memory().total / 1024 ** 3

    if registrar_percentual_disco or registrar_gb_disco:
        partitions = psutil.disk_partitions(all=False)

        largest_disk = None
        max_size = 0

        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                if usage.total > max_size:
                    max_size = usage.total
                    largest_disk = partition.mountpoint
            except PermissionError:
                continue

        if largest_disk:
            montagem = largest_disk

            if registrar_percentual_disco:
                percentual_disco = psutil.disk_usage(montagem).percent

            if registrar_gb_disco:
                gb_disco = psutil.disk_usage(montagem).total / 1024 ** 3
        print(percentual_cpu, percentual_disco, percentual_memoria, gb_disco, gb_ram)

        # fazendo a consulta
        query = """
           INSERT INTO Registro
           (cpu_percentual, ram_disponivel_percentual, ram_disponivel_gb, disco_uso_percentual, disco_disponivel_gb, dataHora)
           VALUES (%s, %s, %s, %s, %s, %s)
           """
        valores = (
            percentual_cpu,
            percentual_memoria if percentual_memoria is not None else None,
            gb_ram if gb_ram is not None else None,
            percentual_disco if percentual_disco is not None else None,
            gb_disco if gb_disco is not None else None,
            datetime.now()
        )
        cursor.execute(query, valores)

        mydb.commit()

        print("Registro inserido com sucesso!")




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

def cadastrarDiscos(fkComputador):
    print("\nCadastrando discos...")

    discos = psutil.disk_partitions(all=False)

    for disco in discos:
        try:
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
        except Exception as e:
            print(e)

def cadastrarCPU(fkComputador):
    print("\nCadastrando CPU...")
    # capturando informações da CPU
    frequencia_cpu = psutil.cpu_freq()
    frequencia = frequencia_cpu.max
    #resgatando cores
    cores = psutil.cpu_count(True)

    consulta = "INSERT INTO CPU (frequencia, cores, fkComputador) VALUES (%.2f, %d, %d)" % (frequencia, cores, fkComputador)
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


def cadastrarMaquina():
    apelido = input('Digite um apelido para a máquina:\n')
    codigo = input('Digite um código para a máquina: ')
    consulta = "INSERT INTO Computador(codigoMaquina, apelido, fkFilial) VALUES ('%s', '%s', 1)" % (codigo, apelido)
    cursor.execute(consulta)
    mydb.commit()
    id_computador_cadastrado = cursor._last_insert_id
    print("Computador de id %d cadastrado" % id_computador_cadastrado)
    print("\nCadastrando componentes do computador...")
    cadastrarCPU(id_computador_cadastrado)
    cadastrarMemoria(id_computador_cadastrado)
    cadastrarDiscos(id_computador_cadastrado)

def verificarMaquinaCadastrada(codigoMaquina):
    consulta = "SELECT * FROM computador WHERE codigoMaquina = '%s'" % codigoMaquina
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

def home():
        saiu = False
        while (saiu == False):
            opcao = int(input(
                "\nBem vindo ao client InnovaAir, digite uma opção para prosseguir: \n1. Iniciar captura de dados computacionais.\n2. Verificar informações do computador\n3. Sair\n"))
            match (opcao):
                case 1:
                    print("Verificando se a máquina já está cadastrada no banco de dados...")
                    codigoMaquina = input("Digite o código da sua máquina: ")
                    cadastrada = verificarMaquinaCadastrada(codigoMaquina)
                    if (cadastrada):
                        id_computador = resgatarIdComputador(codigoMaquina)
                        if (verificaPossuiMetricas(id_computador)):
                            while (True):
                                capturarDados(id_computador)
                                time.sleep(5)
                        else:
                            cadastrarMetricas(id_computador)




                case 2:
                    exibirDadosComputacionais()
                case 3:
                    print("\nAté mais :)")
                    saiu = True
                    exit()



def menuInicial():
    saiu = False
    while (saiu == False):
        opcao = int(
            input("Bem vindo ao client InnovaAir, digite uma opção para prosseguir:\n1. Acessar aplicação\n2. Sair\n"))
        match (opcao):
            case 1:
                    home()
                    saiu = True
            case 2:
                print("Até mais :)")
                saiu = True
                exit()

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="pythoncollector",
        password="pythonklyn123",
        database="innovaair"
    )
    cursor = mydb.cursor()

    menuInicial()
except Error as e:
    print("Houve um problema com a comunicação com o banco de dados\n")
    print(e)
    exit(0)
else:
    print("Conexão estabelecida com banco de dados... Prosseguindo com execução")



