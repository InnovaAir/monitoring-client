import mysql.connector
from mysql.connector import Error
import time
import os

def listaDeMaquinas():   
    while True:
        os.system('cls') 
        print("\nQual tipo de medida deseja visualizar?")
        print("1 - Média por máquina (média dos valores de uso de cada máquina selecionada)")
        print("2 - Média total (média geral considerando todas as máquinas monitoradas)")
        
        medida = int(input())
        
        if (medida == 1 or medida == 2):
            if(medida == 1):
                while True:
                    os.system('cls') 
                    print("Consultando máquinas cadastradas...")
                    # time.sleep(2)
                    instrucaoMYSQL = "select idComputador, apelido, hostname from Computador;"
                    cursor.execute(instrucaoMYSQL)
                    resultados = cursor.fetchall()
                    os.system('cls') 
                    print(f"|  ID | APELIDO{' ' * 13} | HOSTNAME{' ' * 27} |")

                    ids_disponiveis = set()

                    for linha in resultados:
                        print(f"|  {linha[0]:<2} | {linha[1]:<20} | {linha[2]:<35} |")
                        ids_disponiveis.add(linha[0])

                    print("\nEscolha qual a máquina deseja monitorar")
                    
                    opcao=int(input("Digite o ID: "))

                    
                    if opcao in ids_disponiveis:
                        opcaoComponente = qualComponente()
                        # CASO ELE ESCOLHA MONITORAMENTO INDIVIDUAL E COMPONENTE CPU, QUE SERÁ APENAS %
                        if opcaoComponente == 1:
                            # os.system('cls') 
                            
                            # instrucaoMYSQL = """
                            #     SELECT datahora ,m.percentualUso
                            #     FROM MetricaCPU m
                            #     JOIN CPU c ON m.fkCpu = c.idCpu
                            #     JOIN Computador comp ON c.fkComputador = comp.idComputador
                            #     WHERE comp.idComputador = %s;"""
                            
                            # cursor.execute(instrucaoMYSQL, (opcao,)) 
                            # resultados = cursor.fetchall()

                            # for cpu in resultados:
                            #     print(cpu[0], cpu[1])

                            exibirCPUpercentual(opcao)
                            return
                        else: 
                            # CASO ELE ESCOLHA OUTROS COMPONENTES A NÃO SER CPU, QUE TEM A POSSIBILIDADE DE SER % E BITS
                            opcaoMetrica = qualMetrica() 
                            if(opcaoMetrica == 1):
                                # CASO SEJA EM PERCENTUAL
                                if(opcaoComponente == 2):
                                    # Caso seja Memoria
                                    # instrucaoMYSQL = """SELECT mm.dataHora, mm.percentualUso
                                    #                     FROM MetricaMemoria mm
                                    #                     JOIN Memoria m ON mm.fkMemoria = m.idMemoria
                                    #                     JOIN Computador c ON m.fkComputador = c.idComputador
                                    #                     WHERE c.idComputador = %s
                                    #                     ORDER BY mm.dataHora DESC;"""
                                    # cursor.execute(instrucaoMYSQL, (opcao,)) 
                                    # resultados = cursor.fetchall()
                                    # for memoria in resultados:
                                    #      print(memoria[0], memoria[1])

                                    exibirMemoriaEmPercentual(opcao)
                                    return
                                elif(opcaoComponente == 3):
                                    # Caso seja Disco
                                        # instrucaoMYSQL = """SELECT md.dataHora, md.percentualUso
                                        #                     FROM MetricaDisco md
                                        #                     JOIN Disco d ON md.fkDisco = d.idDisco
                                        #                     JOIN Computador c ON d.fkComputador = c.idComputador
                                        #                     WHERE c.idComputador = %s
                                        #                     ORDER BY md.dataHora DESC;"""
                                        # cursor.execute(instrucaoMYSQL, (opcao,)) 
                                        # resultados = cursor.fetchall()
                                        # for disco in resultados:
                                        #     print(disco[0], disco[1])
                                    exibirDiscoEmPercentual(opcao)
                                    return
                                elif(opcaoComponente == 4):
                                    # Caso seja todos os componentes
                                    # instrucaoMYSQL = """SELECT 'Memória' AS Componente, mm.dataHora, mm.percentualUso
                                    #                     FROM MetricaMemoria mm
                                    #                     JOIN Memoria m ON mm.fkMemoria = m.idMemoria
                                    #                     JOIN Computador c ON m.fkComputador = c.idComputador
                                    #                     WHERE c.idComputador = %s
                                    #                     UNION ALL
                                    #                     SELECT 'Disco', md.dataHora, md.percentualUso
                                    #                     FROM MetricaDisco md
                                    #                     JOIN Disco d ON md.fkDisco = d.idDisco
                                    #                     JOIN Computador c ON d.fkComputador = c.idComputador
                                    #                     WHERE c.idComputador = %s
                                    #                     ORDER BY dataHora DESC;"""
                                    # cursor.execute(instrucaoMYSQL, (opcao,)) 
                                    # resultados = cursor.fetchall()

                                    # for todos in resultados:
                                    #         print(todos)
                                    exibirTodosEmPercentual(opcao)
                                    return
                            else:
                                # CASO SEJA EM BITS
                                if(opcaoComponente == 2):
                                    # Caso seja Memoria
                                    # instrucaoMYSQL = """SELECT mm.dataHora, mm.quantidadeLivre, mm.quantidadeUsada
                                    #                     FROM MetricaMemoria mm
                                    #                     JOIN Memoria m ON mm.fkMemoria = m.idMemoria
                                    #                     JOIN Computador c ON m.fkComputador = c.idComputador
                                    #                     WHERE c.idComputador = %s
                                    #                     ORDER BY mm.dataHora DESC;"""
                                    # cursor.execute(instrucaoMYSQL, (opcao,)) 
                                    # resultados = cursor.fetchall()

                                    # for memoria in resultados:
                                    #         print(memoria[0], memoria[1], memoria1)

                                    exibirMemoriaEmBits(opcao)
                                    return
                                elif(opcaoComponente == 3):
                                    # Caso seja Disco
                                    # instrucaoMYSQL = """SELECT md.dataHora, md.quantidadeLivre, md.quantidadeUsada
                                    #                     FROM MetricaDisco md
                                    #                     JOIN Disco d ON md.fkDisco = d.idDisco
                                    #                     JOIN Computador c ON d.fkComputador = c.idComputador
                                    #                     WHERE c.idComputador = %s
                                    #                     ORDER BY md.dataHora DESC;"""
                                    # cursor.execute(instrucaoMYSQL, (opcao,)) 
                                    # resultados = cursor.fetchall()

                                    # for disco in resultados:
                                    #         print(disco[0], disco[1], disco[3])
                                    exibirDiscoEmBits(opcao)
                                    return
                                elif(opcaoComponente == 4):
                                    # Caso seja todos os componentes
                                    # instrucaoMYSQL = """SELECT 'Memória' AS Componente, mm.dataHora, mm.        quantidadeLivre, mm.quantidadeUsada
                                    #                     FROM MetricaMemoria mm
                                    #                     JOIN Memoria m ON mm.fkMemoria = m.idMemoria
                                    #                     JOIN Computador c ON m.fkComputador = c.idComputador
                                    #                     WHERE c.idComputador = %s
                                    #                     UNION ALL
                                    #                     SELECT 'Disco', md.dataHora, md.quantidadeLivre, md.quantidadeUsada
                                    #                     FROM MetricaDisco md
                                    #                     JOIN Disco d ON md.fkDisco = d.idDisco
                                    #                     JOIN Computador c ON d.fkComputador = c.idComputador
                                    #                     WHERE c.idComputador = %s
                                    #                     ORDER BY dataHora DESC;"""
                                    # cursor.execute(instrucaoMYSQL, (opcao,)) 
                                    # resultados = cursor.fetchall()

                                    # for todos in resultados:
                                    #         print(todos)
                                    exibirTodosEmBits(opcao)
                                    return
                                return

                    else:
                        print("Máquina inexistente. Tente novamente.")


            elif(medida == 2):
                opcaoComponente = qualComponente()
                if(opcaoComponente == 1):
                    #  Se for CPU
                    # instrucaoMYSQL = """SELECT dataHora , percentualUso  FROM MetricaCPU;"""
                    # cursor.execute(instrucaoMYSQL) 
                    # resultados = cursor.fetchall()

                    # for cpu in resultados:
                    #     print(cpu[0], cpu[1])
                    exibirCpuTodasMaquinasPercentual() 
                    return

                elif(opcaoComponente == 2):
                    #  Se for Memoria
                    opcaoMetrica = qualMetrica()
                    if(opcaoMetrica == 1):
                        # Se for Percentual
                        # instrucaoMYSQL = """SELECT dataHora , percentualUso FROM MetricaMemoria;"""
                        # cursor.execute(instrucaoMYSQL) 
                        # resultados = cursor.fetchall()

                        # for memoria in resultados:
                        #      print(memoria[0], memoria[1])
                        exibirMemoriaTodasMaquinasPercentual()
                        return
                        
                    elif(opcaoMetrica == 2):
                    # Se for Bits
                        # instrucaoMYSQL = """SELECT dataHora, quantidadeLivre , quantidadeUsada FROM MetricaMemoria;"""
                        # cursor.execute(instrucaoMYSQL) 
                        # resultados = cursor.fetchall()

                        # for memoria in resultados:
                        #     print(memoria[0], memoria[1], memoria[2])
                        exibirMemoriaTodasMaquinasBits()
                        return
                    
                elif(opcaoComponente == 3):
                    #  Se for Disco
                    opcaoMetrica = qualMetrica()
                    if(opcaoMetrica == 1):
                        # Se for Percentual
                        # instrucaoMYSQL = """SELECT dataHora, percentualUso FROM MetricaDisco;"""
                        # cursor.execute(instrucaoMYSQL) 
                        # resultados = cursor.fetchall()

                        # for disco in resultados:
                        #     print(disco[0], disco[1])
                        exibirDiscoTodasMaquinasPercentual()
                        return

                    elif(opcaoMetrica == 2):
                    # Se for Bits
                        # instrucaoMYSQL = """SELECT dataHora, quantidadeLivre ,  quantidadeUsada FROM MetricaDisco;"""
                        # cursor.execute(instrucaoMYSQL) 
                        # resultados = cursor.fetchall()

                        # for disco in resultados:
                        #     print(disco[0], disco[1], disco[2])
                        exibirDiscoTodasMaquinasBits()
                        return

                elif(opcaoComponente == 4):
                    #  Se for todos os componentes
                    opcaoMetrica = qualMetrica()
                    if(opcaoMetrica == 1):
                        # Se for Percentual
                        # instrucaoMYSQL = """SELECT 'Memória' AS Componente,  mm.percentualUso AS mediaPercentual , mm.dataHora as Horario
                        #                     FROM MetricaMemoria mm
                        #                     UNION ALL
                        #                     SELECT 'Disco',  md.percentualUso, md.dataHora as Horario
                        #                     FROM MetricaDisco md
                        #                     UNION ALL
                        #                     SELECT 'CPU', mc.percentualUso, mc.dataHora as Horario
                        #                     FROM MetricaCPU mc;"""
                        # cursor.execute(instrucaoMYSQL) 
                        # resultados = cursor.fetchall()

                        # for disco in resultados:
                        #     print(disco)
                        exibirComponentesTodasMaquinasPercentual()
                        return

                    elif(opcaoMetrica == 2):
                    # Se for Bits
                        # instrucaoMYSQL = """SELECT 'Memória' AS Componente, mm.quantidadeLivre AS mediaLivre, mm.quantidadeUsada AS mediaUsada , mm.dataHora as Horario
                        #                     FROM MetricaMemoria mm
                        #                     UNION ALL
                        #                     SELECT 'Disco', md.quantidadeLivre, md.quantidadeUsada, md.dataHora as Horario
                        #                     FROM MetricaDisco md;"""
                        # cursor.execute(instrucaoMYSQL) 
                        # resultados = cursor.fetchall()

                        # for disco in resultados:
                        #     print(disco[0], disco[1], disco[2])
                        exibirComponentesTodasMaquinasBits()
                        return

        else:
            print("Opção inválida. Tente novamente.")
    
    
def qualComponente():
    while True:
        os.system('cls') 
        print("\nQual componente você deseja monitorar?")
        print("\n1 - CPU\n2 - Memória\n3 - Disco\n4 - Todos os componentes")
        componente = int(input())           
        if (componente == 1 or componente == 2 or componente == 3 or componente == 4):
            return componente;
        else:
            print("Opção inválida. Tente novamente.")

def qualMetrica():
    while True:
        os.system('cls') 
        print("\nQual a prêferencia de métrica?")
        print("\n1 - Percentual (%)\n2 - Bytes")
        metrica = int(input())         
        if (metrica == 1 or metrica == 2 or metrica == 3 or metrica == 4):
            return metrica;
        else:
            print("Opção inválida. Tente novamente.")

def gostariaDeContinuar(medida, componente, metrica , maquina):
    while True:
            print("\nGostaria de continuar o monitoramento?")
            print("\n1 - SIM\n2 - NÂO")
            respostas = int(input())         
            if (respostas == 1 or respostas == 2):
                if(respostas == 1):
                    if medida == 1 and componente == 1 and metrica == 1:
                        exibirCPUpercentual(maquina)
                    elif medida == 1 and componente == 2 and metrica == 1:
                        exibirMemoriaEmPercentual(maquina)
                    elif medida == 1 and componente == 3 and metrica == 1:
                        exibirDiscoEmPercentual(maquina)
                    elif medida == 1 and componente == 4 and metrica == 1:
                        exibirTodosEmPercentual(maquina)
                    elif medida == 1 and componente == 1 and metrica == 2:
                        exibirMemoriaEmBits(maquina)
                    elif medida == 1 and componente == 2 and metrica == 2:
                        exibirDiscoEmBits(maquina)
                    elif medida == 1 and componente == 3 and metrica == 2:
                        exibirMemoriaEmBits(maquina)
                    elif medida == 1 and componente == 4 and metrica == 2:
                        exibirTodosEmBits(maquina)
                    elif medida == 2 and componente == 1 and metrica == 1:
                        exibirCpuTodasMaquinasPercentual()
                    elif medida == 2 and componente == 2 and metrica == 1:
                        exibirMemoriaTodasMaquinasPercentual()
                    elif medida == 2 and componente == 3 and metrica == 1:
                        exibirDiscoTodasMaquinasPercentual()
                    elif medida == 2 and componente == 4 and metrica == 1:
                        exibirComponentesTodasMaquinasPercentual()
                    elif medida == 2 and componente == 1 and metrica == 2:
                        exibirMemoriaTodasMaquinasBits()
                    elif medida == 2 and componente == 2 and metrica == 2:
                        exibirDiscoTodasMaquinasBits()
                    elif medida == 2 and componente == 3 and metrica == 2:
                        exibirMemoriaTodasMaquinasBits()
                    elif medida == 2 and componente == 4 and metrica == 2:
                        exibirComponentesTodasMaquinasBits()

                elif(respostas == 2):
                    print("Encerrando Aplicação...")
                    return
            else:
                print("Opção inválida. Tente novamente.")


# SELECTS
def exibirCPUpercentual(opcao):
    os.system('cls') 
    instrucaoMYSQL = """
        SELECT datahora ,m.percentualUso
        FROM MetricaCPU m
        JOIN CPU c ON m.fkCpu = c.idCpu
        JOIN Computador comp ON c.fkComputador = comp.idComputador
        WHERE comp.idComputador = %s ORDER BY datahora DESC;"""
    
    cursor.execute(instrucaoMYSQL, (opcao,)) 
    resultados = cursor.fetchall()

    listaHorario =[]
    listaUso =[]

    temDez = 0

    if(len(resultados) > 10):
        temDez = 10
    else: 
        temDez = len(resultados)

    for posicao in range(temDez):
        cpu = resultados[posicao]
        horario = cpu[0]
        percentual = cpu[1]

        listaHorario.append(horario)
        listaUso.append(percentual)

    media = round((sum(listaUso) / len(listaUso)) ,2) 
    clafissicacaoUso = ""
    formatado = listaHorario[0].strftime("%d/%m/%Y às %H:%M")

    if(media >= 85):
        clafissicacaoUso = "Crítico"
    elif (media >= 60):
        clafissicacaoUso = "Alto"
    elif (media >= 40):
        clafissicacaoUso = "Moderado (Ideal)"
    elif (media >= 20):
        clafissicacaoUso = "Baixo (Ideal)"
    elif (media >= 0):
        clafissicacaoUso = "Muito Baixo (Ideal)"

    print("Média do percentual de USO da CPU dos últimos 10 registros")
    print("Percentual: ", media , "%")
    print("Classificação: ", clafissicacaoUso)
    print("Último registro no dia" , formatado)

    gostariaDeContinuar(1 , 1 , 1 , opcao)

def exibirMemoriaEmPercentual(opcao):
    os.system('cls') 
    instrucaoMYSQL = """SELECT mm.dataHora, mm.percentualUso
                        FROM MetricaMemoria mm
                        JOIN Memoria m ON mm.fkMemoria = m.idMemoria
                        JOIN Computador c ON m.fkComputador = c.idComputador
                        WHERE c.idComputador = %s
                        ORDER BY mm.dataHora DESC;"""
    cursor.execute(instrucaoMYSQL, (opcao,)) 
    resultados = cursor.fetchall()
    
    listaHorario =[]
    listaUso =[]

    temDez = 0

    if(len(resultados) > 10):
        temDez = 10
    else: 
        temDez = len(resultados)

    for posicao in range(temDez):
        memoria = resultados[posicao]
        horario = memoria[0]
        percentual = memoria[1]

        listaHorario.append(horario)
        listaUso.append(percentual)

    media = round((sum(listaUso) / len(listaUso)) ,2) 
    clafissicacaoUso = ""
    formatado = listaHorario[0].strftime("%d/%m/%Y às %H:%M")

    if(media >= 80):
        clafissicacaoUso = "Crítico"
    elif (media >= 30):
        clafissicacaoUso = "Moderado (Ideal)"
    elif (media >= 0):
        clafissicacaoUso = "Baixo (Ideal)"

    print("Média do percentual de USO da MEMÓRIA dos últimos 10 registros")
    print("Percentual: ", media , "%")
    print("Classificação: ", clafissicacaoUso)
    print("Último registro no dia" , formatado)

    gostariaDeContinuar(1, 2, 1 , opcao)


def exibirDiscoEmPercentual(opcao):
    os.system('cls') 
    instrucaoMYSQL = """SELECT md.dataHora, md.percentualUso
                        FROM MetricaDisco md
                        JOIN Disco d ON md.fkDisco = d.idDisco
                        JOIN Computador c ON d.fkComputador = c.idComputador
                        WHERE c.idComputador = %s
                        ORDER BY md.dataHora DESC;"""
    cursor.execute(instrucaoMYSQL, (opcao,)) 
    resultados = cursor.fetchall()
    
    listaHorario =[]
    listaUso =[]

    temDez = 0

    if(len(resultados) > 10):
        temDez = 10
    else: 
        temDez = len(resultados)

    for posicao in range(temDez):
        disco = resultados[posicao]
        horario = disco[0]
        percentual = disco[1]

        listaHorario.append(horario)
        listaUso.append(percentual)

    media = round((sum(listaUso) / len(listaUso)) ,2) 
    formatado = listaHorario[0].strftime("%d/%m/%Y às %H:%M")

    print("Média do percentual de USO da DISCO dos últimos 10 registros")
    print("Percentual: ", media , "%")
    print("Último registro no dia" , formatado)
    
    gostariaDeContinuar(1, 3, 1 , opcao)

def exibirTodosEmPercentual(opcao):
    os.system('cls') 
    instrucaoMYSQL = """SELECT 'Memória' AS Componente, mm.dataHora, mm.percentualUso
                        FROM MetricaMemoria mm
                        JOIN Memoria m ON mm.fkMemoria = m.idMemoria
                        JOIN Computador c ON m.fkComputador = c.idComputador
                        WHERE c.idComputador = %s
                        UNION ALL
                        SELECT 'Disco', md.dataHora, md.percentualUso
                        FROM MetricaDisco md
                        JOIN Disco d ON md.fkDisco = d.idDisco
                        JOIN Computador c ON d.fkComputador = c.idComputador
                        WHERE c.idComputador = %s
                        ORDER BY dataHora DESC;"""
    
    cursor.execute(instrucaoMYSQL, (opcao, opcao)) 
    resultados = cursor.fetchall()

    listaHorarioMemoria = []
    listaUsoMemoria = []

    listaHorarioDisco = []
    listaUsoDisco = []


    for verificarComponente in resultados:
        tupla = verificarComponente
        if( tupla[0] == 'Memória' ):
            horarioMemoria = tupla[1]
            percentualMemoria = tupla[2]
            listaHorarioMemoria.append(horarioMemoria)
            listaUsoMemoria.append(percentualMemoria)

        elif ( tupla[0] == 'Disco' ):
            horarioDisco = tupla[1]
            percentualDisco = tupla[2]
            listaHorarioDisco.append(horarioDisco)
            listaUsoDisco.append(percentualDisco)


    mediaMemoria = round((sum(listaUsoMemoria[0:10]) / 10 ) ,2) 
    clafissicacaoUsoMemoria = ""
    formatado = listaHorarioMemoria[0].strftime("%d/%m/%Y às %H:%M")

    if(mediaMemoria >= 80):
        clafissicacaoUsoMemoria = "Crítico"
    elif (mediaMemoria >= 30):
        clafissicacaoUsoMemoria = "Moderado (Ideal)"
    elif (mediaMemoria >= 0):
        clafissicacaoUsoMemoria = "Baixo (Ideal)"

    print("------------------------->MEMÓRIA<-------------------------")
    print("Média do percentual de USO da MEMÓRIA dos últimos 10 registros")
    print("Percentual: ", mediaMemoria , "%")
    print("Classificação: ", clafissicacaoUsoMemoria)

    print("\n-------------------------->DISCO<--------------------------")
    print("Percentual de uso: ", listaUsoDisco[0] , "%")

    print("\n-----> Último registro no dia" , formatado)

    gostariaDeContinuar(1, 4, 1 , opcao)


def exibirMemoriaEmBits(opcao):
    os.system('cls') 
    instrucaoMYSQL = """SELECT mm.dataHora, mm.quantidadeLivre, mm.quantidadeUsada
                        FROM MetricaMemoria mm
                        JOIN Memoria m ON mm.fkMemoria = m.idMemoria
                        JOIN Computador c ON m.fkComputador = c.idComputador
                        WHERE c.idComputador = %s
                        ORDER BY mm.dataHora DESC;"""
    cursor.execute(instrucaoMYSQL, (opcao,)) 
    resultados = cursor.fetchall()

    for memoria in resultados:
            print(memoria[0], memoria[1], memoria[2])
    
    gostariaDeContinuar(1, 2, 2 , opcao)

def exibirDiscoEmBits(opcao):
    os.system('cls') 
    instrucaoMYSQL = """SELECT md.dataHora, md.quantidadeLivre, md.quantidadeUsada
                        FROM MetricaDisco md
                        JOIN Disco d ON md.fkDisco = d.idDisco
                        JOIN Computador c ON d.fkComputador = c.idComputador
                        WHERE c.idComputador = %s
                        ORDER BY md.dataHora DESC;"""
    cursor.execute(instrucaoMYSQL, (opcao,)) 
    resultados = cursor.fetchall()

    for disco in resultados:
            print(disco[0], disco[1], disco[2])
            
    gostariaDeContinuar(1, 3, 2 , opcao)
    
def exibirTodosEmBits(opcao):
    os.system('cls') 
    instrucaoMYSQL = """SELECT 'Memória' AS Componente, mm.dataHora, mm.quantidadeLivre, mm.quantidadeUsada
                        FROM MetricaMemoria mm
                        JOIN Memoria m ON mm.fkMemoria = m.idMemoria
                        JOIN Computador c ON m.fkComputador = c.idComputador
                        WHERE c.idComputador = %s
                        UNION ALL
                        SELECT 'Disco', md.dataHora, md.quantidadeLivre, md.quantidadeUsada
                        FROM MetricaDisco md
                        JOIN Disco d ON md.fkDisco = d.idDisco
                        JOIN Computador c ON d.fkComputador = c.idComputador
                        WHERE c.idComputador = %s
                        ORDER BY dataHora DESC;"""
    cursor.execute(instrucaoMYSQL, (opcao,)) 
    resultados = cursor.fetchall()

    for todos in resultados:
            print(todos)

    gostariaDeContinuar(1, 4, 2 , opcao)



# A PARTIR DAQUI É A MEDIDA DE TODAS AS MÁQUINAS
def exibirCpuTodasMaquinasPercentual():
    os.system('cls') 
    instrucaoMYSQL = """SELECT dataHora , percentualUso  FROM MetricaCPU;"""
    cursor.execute(instrucaoMYSQL) 
    resultados = cursor.fetchall()

    for cpu in resultados:
        print(cpu[0], cpu[1])
    
    gostariaDeContinuar(2, 1, 1 , 0)

def exibirMemoriaTodasMaquinasPercentual():
    os.system('cls') 
    instrucaoMYSQL = """SELECT dataHora , percentualUso FROM MetricaMemoria;"""
    cursor.execute(instrucaoMYSQL) 
    resultados = cursor.fetchall()

    for memoria in resultados:
            print(memoria[0], memoria[1])

    gostariaDeContinuar(2, 2, 1 , 0)

def exibirMemoriaTodasMaquinasBits():
    os.system('cls') 
    instrucaoMYSQL = """SELECT dataHora, quantidadeLivre , quantidadeUsada FROM MetricaMemoria;"""
    cursor.execute(instrucaoMYSQL) 
    resultados = cursor.fetchall()

    for memoria in resultados:
        print(memoria[0], memoria[1], memoria[2])
    
    gostariaDeContinuar(2, 2, 2 , 0)

    
def exibirDiscoTodasMaquinasPercentual():
    os.system('cls') 
    instrucaoMYSQL = """SELECT dataHora, percentualUso FROM MetricaDisco;"""
    cursor.execute(instrucaoMYSQL) 
    resultados = cursor.fetchall()

    for disco in resultados:
        print(disco[0], disco[1])

    gostariaDeContinuar(2, 3, 1 , 0)


def exibirDiscoTodasMaquinasBits():
    os.system('cls') 
    instrucaoMYSQL = """SELECT dataHora, quantidadeLivre ,  quantidadeUsada FROM MetricaDisco;"""
    cursor.execute(instrucaoMYSQL) 
    resultados = cursor.fetchall()

    for disco in resultados:
        print(disco[0], disco[1], disco[2])

    gostariaDeContinuar(2, 3, 2 , 0)




def exibirComponentesTodasMaquinasPercentual():
    os.system('cls') 
    instrucaoMYSQL = """SELECT 'Memória' AS Componente,  mm.percentualUso AS mediaPercentual , mm.dataHora as Horario
                        FROM MetricaMemoria mm
                        UNION ALL
                        SELECT 'Disco',  md.percentualUso, md.dataHora as Horario
                        FROM MetricaDisco md
                        UNION ALL
                        SELECT 'CPU', mc.percentualUso, mc.dataHora as Horario
                        FROM MetricaCPU mc;"""
    cursor.execute(instrucaoMYSQL) 
    resultados = cursor.fetchall()

    for disco in resultados:
        print(disco)

    gostariaDeContinuar(2, 4, 1 , 0)
    
def exibirComponentesTodasMaquinasBits():
    os.system('cls') 
    instrucaoMYSQL = """SELECT 'Memória' AS Componente, mm.quantidadeLivre AS mediaLivre, mm.quantidadeUsada AS mediaUsada , mm.dataHora as Horario
                        FROM MetricaMemoria mm
                        UNION ALL
                        SELECT 'Disco', md.quantidadeLivre, md.quantidadeUsada, md.dataHora as Horario
                        FROM MetricaDisco md;"""
    cursor.execute(instrucaoMYSQL) 
    resultados = cursor.fetchall()

    for disco in resultados:
        print(disco[0], disco[1], disco[2])
    
    gostariaDeContinuar(2, 4, 2 , 0)

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="superestagiario",
        password="urubu100",
        database="innovair"
    )
    cursor = mydb.cursor()

    listaDeMaquinas()
except Error as e:
    print("Houve um problema com a comunicação com o banco de dados\n")
    print(e)
    exit(0)