CREATE DATABASE IF NOT EXISTS innovaair;

USE innovaair;

/* Ordem de código de database:  */
-- tabelas do cliente

CREATE TABLE IF NOT EXISTS cliente(
  idCliente int not null primary key AUTO_INCREMENT,
  cnpj char(14) not null,
  razaoSocial varchar(45) not null,
  email varchar(255) not null,
  telefone char(11) not null,
  fkResponsavel int not null
)

CREATE TABLE IF NOT EXISTS usuario(
  idUsuario int not null primary key AUTO_INCREMENT,
  tipoUsuario tinyint not null ,
  email varchar(255) not null ,
  senha varchar(30) not null,
  fkCliente int not null,
  UNIQUE (idUsuario)
)

ALTER TABLE cliente add constraint fkClienteResponsavel foreign key (fkResponsavel) REFERENCES usuario(idUsuario);
ALTER TABLE usuario add constraint fkClienteUsuario foreign key (fkCliente) references cliente(idCliente);

CREATE TABLE IF NOT EXISTS filial(
  idFilial int not null primary key AUTO_INCREMENT,
  terminal varchar(30) not null,
  setor varchar(30) not null,
  logradouro varchar(100) not null,
  cep char(9) not null,
  numero varchar(10) not null,
  complemento varchar(30) not null,
  fkCliente int not null,
  fkCidade int not null
)


CREATE TABLE IF NOT EXISTS cidade (
  idCidade INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(45) NOT NULL,
  fkEstado INT NOT NULL
  );

CREATE TABLE IF NOT EXISTS estado (
  idEstado INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(45) NOT NULL,
  fkPais INT NOT NULL
  );

CREATE TABLE IF NOT EXISTS pais (
  idPais INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(45) NOT NULL
  );

ALTER TABLE filial add constraint fkFilialCliente foreign key (fkCliente) references cliente(idCliente);
ALTER TABLE filial add constraint fkCidadeFilial foreign key (fkCidade) references cidade(idCidade);
ALTER TABLE cidade add constraint fkEstadoCidade foreign key (fkEstado) references estado(idEstado);
ALTER TABLE estado add constraint fkPaisEstado foreign key (fkPais) references pais(idPais);

-- tabelas de captura

CREATE TABLE IF NOT EXISTS identificacaoMaquina (
  idIdentificacao INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  fkFilial INT NOT NULL,
  numeroSerial VARCHAR(45) NOT NULL,
  enderecoMac VARCHAR(45) NOT NULL,
  hostname VARCHAR(45) NOT NULL
  );

ALTER TABLE identificacaoMaquina add constraint fkFilialMaquina foreign key (fkFilial) references filial(idFilial);

CREATE TABLE IF NOT EXISTS cadastroMaquina (
  idCadastro INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  fkIdentificacao INT NOT NULL,
  componente VARCHAR(45) NOT NULL,
  metrica VARCHAR(45) NOT NULL,
  limiteMaximo INT NOT NULL,
  limiteMinimo INT NOT NULL
  );

-- Sem-relacionamento

CREATE TABLE IF NOT EXISTS maquina_n (
  idCaptura INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  cpu1 INT NOT NULL,
  mem1 INT NOT NULL,
  rede1 INT NOT NULL,
  rede2 INT NOT NULL,
  disco1 INT NOT NULL,
  disco2 INT NOT NULL
  );

  CREATE TABLE IF NOT EXISTS alerta_n (
  idAlerta INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  cpu1 INT NOT NULL,
  mem1 INT NOT NULL,
  rede1 INT NOT NULL,
  rede2 INT NOT NULL,
  disco1 INT NOT NULL,
  disco2 INT NOT NULL,
  cpu1_boolean TINYINT NOT NULL,
  mem1_boolean TINYINT NOT NULL,
  rede1_boolean_copy1 TINYINT NOT NULL,
  rede2_boolean TINYINT NOT NULL,
  disco1_boolean TINYINT NOT NULL,
  disco2_boolean TINYINT NOT NULL
  );