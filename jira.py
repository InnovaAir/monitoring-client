import mysql.connector
import time
import urllib.request
import base64
import json

mydb = mysql.connector.connect(
        host="localhost",
        user="innova_admin",
        password="InnovaairAdmin@123",
        database="innovaair"
    )
cursor = mydb.cursor()
idCliente = 1

# select = f"SELECT idCapturaAlerta, gravidade, hostname, terminal, setor, momento FROM captura_alerta join metrica on fkMetrica = idMetrica join componente on fkComponente = idComponente join Maquina on fkMaquina = idMaquina join filial on fkFilial = idFilial where momento >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"

# select = f"SELECT idCliente, idFilial FROM cliente join filial on fkCliente = idCliente where idCliente != 1"
# cursor.execute(select)
def main():
    select = f"SELECT idCapturaAlerta, gravidade, hostname, terminal, setor, componente FROM captura_alerta join metrica on fkMetrica = idMetrica join componente on fkComponente = idComponente join Maquina on fkMaquina = idMaquina join filial on fkFilial = idFilial join cliente on fkCliente = idCliente where momento >= DATE_SUB(NOW(), INTERVAL 1 HOUR) and idCliente = {idCliente} order by idCapturaAlerta desc"
    cursor.execute(select)
    retorno = cursor.fetchall()
    mydb.commit()
    ultimoId = retorno[0][0]
    print(ultimoId)
    # ABRIR CHAMADO
    while True:
        cursor.execute(select)
        alertas = cursor.fetchall()
        mydb.commit()
        idAtual = alertas[0][0]
        if(idAtual != ultimoId):
            print("diferente")
            ultimoId = idAtual
            alertasDiferentes = list(filter(lambda x: x not in retorno, alertas))
            for alerta in alertasDiferentes:
                usuario = "usuario"
                senha = "senha"

                credenciais = f"{usuario}:{senha}"
                base64_str = base64.b64encode(credenciais.encode('utf-8')).decode('utf-8')
                descricao = f"Máquina de hostname {alerta[2]} do terminal {alerta[3]} e do setor {alerta[4]} emitiu um alerta de gravidade {alerta[1]} vindo do componente {alerta[5]}."
                titulo = f"Alerta {alerta[1]} da Máquina {alerta[2]} do terminal {alerta[4]}"                      
                # URL para onde vai o alerta
                url = "https://inovaair.atlassian.net/rest/api/2/issue"

                # info do alerta 
                dados = {
                  "fields": {
                    "project": {
                      "key": "SUP"
                    },
                    "summary": titulo,
                    "description": descricao,
                    "issuetype": {
                      "name": "task"
                    }
                  }
                }

                dados_json = json.dumps(dados).encode('utf-8')

                # METÓDO POST
                req = urllib.request.Request(url, data=dados_json, method='POST')
                req.add_header("Authorization", f"Basic {base64_str}")
                req.add_header("Content-Type", "application/json")

                try:
                    with urllib.request.urlopen(req) as resposta:
                        conteudo = resposta.read().decode('utf-8')
                        print("Resposta da API:")
                        print(conteudo)
                except urllib.error.HTTPError as e:
                    print(f"Erro HTTP: {e.code} - {e.reason}")
                    print(e.read().decode())
                except urllib.error.URLError as e:
                    print(f"Erro de conexão: {e.reason}")
                

        time.sleep(5)
main()