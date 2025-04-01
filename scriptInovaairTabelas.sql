CREATE DATABASE innovaair;
USE innovaair;

CREATE TABLE cliente (
    idCliente INT PRIMARY KEY AUTO_INCREMENT,
    razaoSocial VARCHAR(100),
    cnpj CHAR(14),
    email VARCHAR(255),
    telefone VARCHAR(15)
);

CREATE TABLE pais (
    idPais INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(45)
);

CREATE TABLE estado (
    idEstado INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(45),
    fkPais INT,
    FOREIGN KEY (fkPais) REFERENCES pais(idPais)
);

CREATE TABLE cidade (
    idCidade INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(45),
    fkEstado INT,
    FOREIGN KEY (fkEstado) REFERENCES estado(idEstado)
);

CREATE TABLE filial (
    idFilial INT PRIMARY KEY AUTO_INCREMENT,
    terminal VARCHAR(30),
    setor VARCHAR(30),
    logradouro VARCHAR(100),
    cep CHAR(9),
    numero VARCHAR(10),
    complemento VARCHAR(30),
    fkCliente INT,
    fkCidade INT,
    FOREIGN KEY (fkCliente) REFERENCES cliente(idCliente),
    FOREIGN KEY (fkCidade) REFERENCES cidade(idCidade)
);

CREATE TABLE acesso (
    idAcesso INT PRIMARY KEY AUTO_INCREMENT,
    acesso INT,
    nomeCargo VARCHAR(45)
);

CREATE TABLE usuario (
    idUsuario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(45),
    tipoUsuario TINYINT,
    email VARCHAR(255),
    senha VARCHAR(30),
    fkCliente INT,
    fkAcesso INT,
    FOREIGN KEY (fkCliente) REFERENCES cliente(idCliente),
    FOREIGN KEY (fkAcesso) REFERENCES acesso(idAcesso)
);

CREATE TABLE maquina (
    idMaquina INT PRIMARY KEY AUTO_INCREMENT,
    fkFilial INT,
    numeroSerial VARCHAR(45),
    enderecoMac VARCHAR(45),
    hostname VARCHAR(45),
    FOREIGN KEY (fkFilial) REFERENCES filial(idFilial)
);

CREATE TABLE componente (
    idComponente INT PRIMARY KEY AUTO_INCREMENT,
    fkMaquina INT,
    componente VARCHAR(45),
    especificacao VARCHAR(45),
    FOREIGN KEY (fkMaquina) REFERENCES maquina(idMaquina)
);

CREATE TABLE metrica (
    idMetrica INT PRIMARY KEY AUTO_INCREMENT,
    metrica VARCHAR(45),
    limiteMaximo INT,
    limiteMinimo INT,
    fkComponente INT,
    FOREIGN KEY (fkComponente) REFERENCES componente(idComponente)
);

CREATE TABLE alerta (
    idAlerta INT PRIMARY KEY AUTO_INCREMENT,
    valorCapturado INT,
    momento DATETIME DEFAULT CURRENT_TIMESTAMP,
    fkMetrica INT,
    FOREIGN KEY (fkMetrica) REFERENCES metrica(idMetrica)
);

insert into pais values
(default, 'Brasil');

insert into estado values
(default, 'São Paulo', 1);

insert into cidade values
(default, 'São Paulo', 1);
    
insert into cliente values
(default, 'LATAM', '02012862000160', 'latam@latam.org', '1234567890');
    
insert into filial values
(default, 'Terminal 1', 'Setor 1', 'Av. Washington Luís', '04626-911', null, null, 1, 1);

insert into acesso values
(default, 7, 'gerente');
    
insert into maquina values
(default, 1, '20230715-001-123', '00:11:22-33-44-55', 'maquina01');
    
insert into componente values
(default, 1, 'processador', 'ryzen 3'),
(default, 1, 'ram', 'kingston ddr4'),
(default, 1, 'ssd', 'sandisk plus');
    
insert into metrica values
(default, 'usoPorcentagem', 90, 25, 1),
(default, 'usoPorcentagem', 80, 45, 2),
(default, 'usoPorcentagem', 85, 30, 3);