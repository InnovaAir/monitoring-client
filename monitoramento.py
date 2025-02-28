import mysql.connector
from mysql.connector import Error
import time
import os

def listaDeMaquinas():   
    while True:
        print("\nQual tipo de medida deseja visualizar?")
        print("1 - Média por máquina (média dos valores de uso de cada máquina selecionada)")
        print("2 - Média total (média geral considerando todas as máquinas monitoradas)")
        
        medida = int(input())
        
        if (medida == 1 or medida == 2):
            if(medida == 1):
                while True:
                    instrucaoMYSQL = "select idComputador, apelido, hostname from Computador;"
                    cursor.execute(instrucaoMYSQL)

                    resultados = cursor.fetchall()
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
                                    #         print(memoria[0], memoria[1], memoria[3])

                                    exibirMemoriaEmBits(opcao)
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

                    else:
                        print("Opção inválida. Tente novamente.")


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
                        
                    elif(opcaoMetrica == 2):
                    # Se for Bits
                        # instrucaoMYSQL = """SELECT dataHora, quantidadeLivre , quantidadeUsada FROM MetricaMemoria;"""
                        # cursor.execute(instrucaoMYSQL) 
                        # resultados = cursor.fetchall()

                        # for memoria in resultados:
                        #     print(memoria[0], memoria[1], memoria[2])
                        exibirMemoriaTodasMaquinasBits()
                    
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

                    elif(opcaoMetrica == 2):
                    # Se for Bits
                        # instrucaoMYSQL = """SELECT dataHora, quantidadeLivre ,  quantidadeUsada FROM MetricaDisco;"""
                        # cursor.execute(instrucaoMYSQL) 
                        # resultados = cursor.fetchall()

                        # for disco in resultados:
                        #     print(disco[0], disco[1], disco[2])
                        exibirDiscoTodasMaquinasBits()

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

        else:
            print("Opção inválida. Tente novamente.")
    
    
def qualComponente():
    while True:
        print("\nQual componente você deseja monitorar?")
        print("\n1 - CPU\n2 - Memória\n3 - Disco\n4 - Todos os componentes")
        componente = int(input())           
        if (componente == 1 or componente == 2 or componente == 3 or componente == 4):
            return componente;
        else:
            print("Opção inválida. Tente novamente.")

def qualMetrica():
    while True:
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
        WHERE comp.idComputador = %s;"""
    
    cursor.execute(instrucaoMYSQL, (opcao,)) 
    resultados = cursor.fetchall()

    for cpu in resultados:
        print(cpu[0], cpu[1])
    
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
    for memoria in resultados:
        print(memoria[0], memoria[1])
    
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
    for disco in resultados:
        print(disco[0], disco[1])
    
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
    cursor.execute(instrucaoMYSQL, (opcao,)) 
    resultados = cursor.fetchall()

    for todos in resultados:
            print(todos)
    
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
            print(disco[0], disco[1], disco[3])
            
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
        user="aluno",
        password="sptech",
        database="innovair"
    )
    cursor = mydb.cursor()

    listaDeMaquinas()
except Error as e:
    print("Houve um problema com a comunicação com o banco de dados\n")
    print(e)
    exit(0)
# else:
#     # print("Conexão estabelecida com banco de dados... Prosseguindo com execução")
    