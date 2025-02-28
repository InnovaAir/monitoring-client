import mysql.connector
from mysql.connector import Error
import time
import os



def listaDeMaquinas():
    instrucaoMYSQL = "select idComputador, apelido, hostname from Computador;"
    cursor.execute(instrucaoMYSQL)

    resultados = cursor.fetchall()
    print("|  ID |  APELIDO |     HOSTNAME      |")
    ids_disponiveis = set()

    for linha in resultados:
        print('| ', linha[0] , ' | ', linha[1] , ' | ' , linha[2], ' |')
        ids_disponiveis.add(linha[0]) 
    
    while True:
        print("\nQual tipo de medida deseja visualizar?")
        print("1 - Média por máquina (média dos valores de uso de cada máquina selecionada)")
        print("2 - Média total (média geral considerando todas as máquinas monitoradas)")
        
        medida = int(input())
        
        if (medida == 1 or medida == 2):
            if(medida == 1):
                while True:
                    print("\nEscolha qual a máquina deseja monitorar")
                    
                    opcao=int(input("Digite o ID: "))

                    
                    if opcao in ids_disponiveis:
                        opcaoComponente = qualComponente()
                        # CASO ELE ESCOLHA MONITORAMENTO INDIVIDUAL E COMPONENTE CPU, QUE SERÁ APENAS %
                        if opcaoComponente == 1:
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
                        else: 
                            # CASO ELE ESCOLHA OUTROS COMPONENTES A NÃO SER CPU, QUE TEM A POSSIBILIDADE DE SER % E BITS
                            opcaoMetrica = qualMetrica() 
                            if(opcaoMetrica == 1):
                                # CASO SEJA EM PERCENTUAL
                                if(opcaoComponente == 2):
                                    # Caso seja Memoria
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

                                elif(opcaoComponente == 3):
                                    # Caso seja Disco
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
                                elif(opcaoComponente == 4):
                                    # Caso seja todos os componentes
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
                            else:
                                # CASO SEJA EM BITS
                                if(opcaoComponente == 2):
                                    # Caso seja Memoria
                                    instrucaoMYSQL = """SELECT mm.dataHora, mm.quantidadeLivre, mm.quantidadeUsada
                                                        FROM MetricaMemoria mm
                                                        JOIN Memoria m ON mm.fkMemoria = m.idMemoria
                                                        JOIN Computador c ON m.fkComputador = c.idComputador
                                                        WHERE c.idComputador = %s
                                                        ORDER BY mm.dataHora DESC;"""
                                    cursor.execute(instrucaoMYSQL, (opcao,)) 
                                    resultados = cursor.fetchall()

                                    for memoria in resultados:
                                            print(memoria[0], memoria[1], memoria[3])

                                elif(opcaoComponente == 3):
                                    # Caso seja Disco
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
                                elif(opcaoComponente == 4):
                                    # Caso seja todos os componentes
                                    instrucaoMYSQL = """SELECT 'Memória' AS Componente, mm.dataHora, mm.        quantidadeLivre, mm.quantidadeUsada
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

                    else:
                        print("Opção inválida. Tente novamente.")


            elif(medida == 2):
                opcaoComponente = qualComponente()
                if(opcaoComponente == 1):
                    #  Se for CPU
                    instrucaoMYSQL = """SELECT dataHora , percentualUso  FROM MetricaCPU;"""
                    cursor.execute(instrucaoMYSQL) 
                    resultados = cursor.fetchall()

                    for cpu in resultados:
                        print(cpu[0], cpu[1])

                elif(opcaoComponente == 2):
                    #  Se for Memoria
                    opcaoMetrica = qualMetrica()
                    if(opcaoMetrica == 1):
                        # Se for Percentual
                        instrucaoMYSQL = """SELECT dataHora , percentualUso FROM MetricaMemoria;"""
                        cursor.execute(instrucaoMYSQL) 
                        resultados = cursor.fetchall()

                        for memoria in resultados:
                             print(memoria[0], memoria[1])
                        
                    elif(opcaoMetrica == 2):
                    # Se for Bits
                        instrucaoMYSQL = """SELECT dataHora, quantidadeLivre , quantidadeUsada FROM MetricaMemoria;"""
                        cursor.execute(instrucaoMYSQL) 
                        resultados = cursor.fetchall()

                        for memoria in resultados:
                            print(memoria[0], memoria[1], memoria[2])
                    
                elif(opcaoComponente == 3):
                    #  Se for Disco
                    opcaoMetrica = qualMetrica()
                    if(opcaoMetrica == 1):
                        # Se for Percentual
                        instrucaoMYSQL = """SELECT dataHora, percentualUso FROM MetricaDisco;"""
                        cursor.execute(instrucaoMYSQL) 
                        resultados = cursor.fetchall()

                        for disco in resultados:
                            print(disco[0], disco[1])

                    elif(opcaoMetrica == 2):
                    # Se for Bits
                        instrucaoMYSQL = """SELECT dataHora, quantidadeLivre ,  quantidadeUsada FROM MetricaDisco;"""
                        cursor.execute(instrucaoMYSQL) 
                        resultados = cursor.fetchall()

                        for disco in resultados:
                            print(disco[0], disco[1], disco[2])

                elif(opcaoComponente == 4):
                    #  Se for todos os componentes
                    opcaoMetrica = qualMetrica()
                    if(opcaoMetrica == 1):
                        # Se for Percentual
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

                    elif(opcaoMetrica == 2):
                    # Se for Bits
                        instrucaoMYSQL = """SELECT 'Memória' AS Componente, mm.quantidadeLivre AS mediaLivre, mm.quantidadeUsada AS mediaUsada , mm.dataHora as Horario
                                            FROM MetricaMemoria mm
                                            UNION ALL
                                            SELECT 'Disco', md.quantidadeLivre, md.quantidadeUsada, md.dataHora as Horario
                                            FROM MetricaDisco md;"""
                        cursor.execute(instrucaoMYSQL) 
                        resultados = cursor.fetchall()

                        for disco in resultados:
                            print(disco[0], disco[1], disco[2])

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
else:
    print("Conexão estabelecida com banco de dados... Prosseguindo com execução")