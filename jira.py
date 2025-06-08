import mysql.connector
import time
import urllib.request
import base64
import json
from datetime import datetime

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="urubu100",
        database="innovaair",
        port=3307
    )
cursor = mydb.cursor()
idCliente = 2

# select = f"SELECT idCapturaAlerta, gravidade, hostname, terminal, setor, momento FROM captura_alerta join metrica on fkMetrica = idMetrica join componente on fkComponente = idComponente join Maquina on fkMaquina = idMaquina join filial on fkFilial = idFilial where momento >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"

# select = f"SELECT idCliente, idFilial FROM cliente join filial on fkCliente = idCliente where idCliente != 1"
# cursor.execute(select)
def main():
    select = f"""
    SELECT idCapturaAlerta,
      gravidade, 
      hostname,
      aeroporto, 
      setor, 
      componente 
      idMaquina, 
      momento
      FROM captura_alerta 
      JOIN metrica 
      ON fkMetrica = idMetrica 
      JOIN componente on fkComponente = idComponente 
      JOIN maquina on fkMaquina = idMaquina 
      JOIN filial on fkFilial = idFilial 
      JOIN cliente on fkCliente = idCliente
      JOIN endereco on fkEndereco = idEndereco
      WHERE momento >= DATE_SUB(NOW(), INTERVAL 1 HOUR) and idCliente = {idCliente} ORDER BY idCapturaAlerta desc
      """
      
    cursor.execute(select)
    retorno = cursor.fetchall()
    mydb.commit()

    ultimoId = 0

    if len(retorno) != 0:
      ultimoId = retorno[0][0]
      
    print(ultimoId)
    
    # ABRIR CHAMADO
    while True:
        cursor.execute(select)
        alertas = cursor.fetchall()
        
        mydb.commit()
        
        idAtual = 0
        
        if len(alertas) != 0:
          idAtual = alertas[0][0]          
          
        print(idAtual)
        
        if(idAtual != ultimoId):
            print("diferente")
            ultimoId = idAtual
            alertasDiferentes = list(filter(lambda x: x not in retorno, alertas))
            for alerta in alertasDiferentes:
                usuario = "diogo.tateno@sptech.school"
                senha = ""

                credenciais = f"{usuario}:{senha}"
                base64_str = base64.b64encode(credenciais.encode('utf-8')).decode('utf-8')

                titulo = f"[{alerta[1]}] {alerta[5]} - {alerta[2]} ({alerta[3]}/{alerta[4]})"                      

                descricao = f"""*DETALHES DO ALERTA*
                *ID do Alerta:* {alerta[0]}
                *Máquina:* {alerta[2]} (ID: {alerta[5]})
                *Localização:* {alerta[3]} - {alerta[4]}
                *Componente Afetado:* {alerta[5]}
                *Nível de Gravidade:* {alerta[1]}

                *AÇÕES NECESSÁRIAS*
                - [ ] Verificar status atual da máquina e/ou componente
                - [ ] Analisar logs do sistema
                - [ ] Executar diagnóstico da máquina
                - [ ] Aplicar correção se necessário
                - [ ] Validar funcionamento após intervenção

                *INFORMAÇÕES TÉCNICAS*
                - Data/Hora do Alerta: {alerta[6]}
                - Sistema de Monitoramento: ID {alerta[0]}

                ---
                _Chamado gerado automaticamente pelo sistema de monitoramento_"""
                
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