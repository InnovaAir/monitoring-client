#!/bin/bash

echo "Atualizando pacotes do sistema"
sudo apt update -y && sudo apt upgrade -y

echo "Instalando pacote python-venv para criação de ambientes virtuais em sistemas baseados em Debian"
sudo apt install python3.12-venv -y

cd

echo "Criando ambiente virtual em /home/ubuntu/ambiente_virtual"
python3 -m venv /home/ubuntu/ambiente_virtual

echo "Acessando ambiente virtual criado"
source /home/ubuntu/ambiente_virtual/bin/activate

echo "Instalando pacotes necessários"
pip install psutil mysql-connector-python

deactivate

# Instala o MySQL Server
echo "Instalando o MySQL Server"
sudo apt install mysql-server -y

# Inicia o serviço do MySQL
echo "Iniciando o serviço MySQL"
sudo service mysql start

# Define variáveis para o banco de dados e usuário
DB_NAME="innovaair"
DB_USER="pythoncollector"
DB_PASS="password123!"

echo "Criando banco de dados e usuário pythoncollector"
sudo mysql -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME};"
sudo mysql -e "DROP USER IF EXISTS '${DB_USER}'@'localhost';"
sudo mysql -e "CREATE USER '${DB_USER}'@'localhost' IDENTIFIED WITH mysql_native_password BY '${DB_PASS}';"
sudo mysql -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# SQL script with corrected database name (innovaair) and variable handling
SQL_SCRIPT=$(cat <<EOF
USE ${DB_NAME};

CREATE TABLE IF NOT EXISTS Cliente (
  idCliente INT NOT NULL AUTO_INCREMENT,
  razaoSocial VARCHAR(105) NULL,
  CNPJ CHAR(14) NULL,
  email VARCHAR(255) NULL,
  telefone VARCHAR(11) NULL,
  responsavel VARCHAR(50) NULL,
  PRIMARY KEY (idCliente)
);

CREATE TABLE IF NOT EXISTS Usuario (
  idUsuario INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(45) NULL,
  tipoUsuario TINYINT NULL,
  email VARCHAR(255) NULL,
  senha VARCHAR(30) NULL,
  fkCliente INT NOT NULL,
  PRIMARY KEY (idUsuario),
  FOREIGN KEY (fkCliente) REFERENCES Cliente(idCliente) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Filial (
  idFilial INT NOT NULL AUTO_INCREMENT,
  aeroporto VARCHAR(50) NULL,
  terminal VARCHAR(30) NULL,
  setor VARCHAR(30) NULL,
  fkCliente INT NOT NULL,
  PRIMARY KEY (idFilial),
  FOREIGN KEY (fkCliente) REFERENCES Cliente(idCliente) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Computador (
  idComputador INT NOT NULL AUTO_INCREMENT,
  apelido VARCHAR(100) NULL,
  codigoMaquina VARCHAR(100) NULL,
  sistemaOperacional VARCHAR(100) NULL,
  hostname VARCHAR(100) NULL,
  arquitetura VARCHAR(100) NULL,
  fkFilial INT NOT NULL,
  PRIMARY KEY (idComputador),
  FOREIGN KEY (fkFilial) REFERENCES Filial(idFilial) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Metrica (
  idMetrica INT NOT NULL AUTO_INCREMENT,
  nomeComponente VARCHAR(45) NULL,
  unidadeMedida VARCHAR(10) NULL,
  nomeMetrica VARCHAR(45) NULL,
  PRIMARY KEY (idMetrica)
);

CREATE TABLE IF NOT EXISTS Memoria (
  idMemoria INT NOT NULL AUTO_INCREMENT,
  tamanho DOUBLE NULL,
  fkComputador INT NOT NULL,
  PRIMARY KEY (idMemoria, fkComputador),
  CONSTRAINT fk_Memoria_Computador1
    FOREIGN KEY (fkComputador)
    REFERENCES ${DB_NAME}.Computador (idComputador)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS CPU (
  idCpu INT NOT NULL AUTO_INCREMENT,
  modelo VARCHAR(45) NULL,
  frequencia DOUBLE NULL,
  cores INT NULL,
  fkComputador INT NOT NULL,
  PRIMARY KEY (idCpu, fkComputador),
  CONSTRAINT fk_CPU_Computador1
    FOREIGN KEY (fkComputador)
    REFERENCES ${DB_NAME}.Computador (idComputador)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Disco (
  idDisco INT NOT NULL AUTO_INCREMENT,
  tipo CHAR(3) NULL,
  capacidade DOUBLE NULL,
  montagem VARCHAR(45) NULL,
  sistemaArquivos VARCHAR(45) NULL,
  fkComputador INT NOT NULL,
  PRIMARY KEY (idDisco, fkComputador),
  CONSTRAINT fk_Disco_Computador1
    FOREIGN KEY (fkComputador)
    REFERENCES ${DB_NAME}.Computador (idComputador)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Threshold (
  fkComputador INT NOT NULL,
  fkMetrica INT NOT NULL,
  minimo DOUBLE NULL,
  maximo DOUBLE NULL,
  PRIMARY KEY (fkComputador, fkMetrica),
  CONSTRAINT fk_Computador_has_Metrica_Computador1
    FOREIGN KEY (fkComputador)
    REFERENCES ${DB_NAME}.Computador (idComputador)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_Computador_has_Metrica_Metrica1
    FOREIGN KEY (fkMetrica)
    REFERENCES ${DB_NAME}.Metrica (idMetrica)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Registro (
  idRegistro INT NOT NULL AUTO_INCREMENT,
  cpu_percentual DOUBLE NULL,
  ram_disponivel_percentual DOUBLE NULL,
  ram_disponivel_gb DOUBLE NULL,
  disco_uso_percentual VARCHAR(45) NULL,
  disco_disponivel_gb VARCHAR(45) NULL,
  dataHora DATETIME NULL,
  PRIMARY KEY (idRegistro)
);

INSERT INTO Cliente (razaoSocial, CNPJ, email, telefone, responsavel) VALUES
('InovAir Soluções em TI', '12345678000199', 'contato@inovair.com', '11987654321', 'João Silva'),
('AeroTech Consultoria', '98765432000111', 'contato@aerotech.com', '21987654321', 'Maria Oliveira'),
('CloudNova Serviços', '45678912000122', 'contato@cloudnova.com', '31987654321', 'Carlos Souza');

INSERT INTO Usuario (nome, tipoUsuario, email, senha, fkCliente) VALUES
('Ana Costa', 1, 'ana.costa@inovair.com', 'senha123', 1),
('Pedro Alves', 2, 'pedro.alves@aerotech.com', 'senha456', 2),
('Luiza Fernandes', 1, 'luiza.fernandes@cloudnova.com', 'senha789', 3);
EOF
)

# Executa o script SQL
echo "Executando script SQL para criar tabelas e inserir dados"
echo "$SQL_SCRIPT" | sudo mysql -u "${DB_USER}" -p"${DB_PASS}" "${DB_NAME}"

echo "Script finalizado!"
