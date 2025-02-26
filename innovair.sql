create database innovair;
use innovair;

create table Usuario(
idUsuario int primary key auto_increment,
nome varchar(100),
email varchar(100),
senha varchar(100)
);

create table Cliente(
id int primary key auto_increment,
razaoSocial varchar(45)
);
insert into cliente (razaoSocial) values ('Cliente 1');

create table Computador (
idComputador INT PRIMARY KEY AUTO_INCREMENT,
apelido varchar(100),
UUID varchar(100),
hostname varchar(100),
fabricante varchar(100),
arquitetura varchar(100),
sistemaOperacional varchar(100),
fkFilial INT,
constraint fkFilialComputador FOREIGN KEY (fkFilial) REFERENCES cliente(id) ON DELETE CASCADE
);

create table CPU (
idCpu INT primary key auto_increment,
modelo varchar(100),
frequencia double,
cores int,
fkComputador INT,
CONSTRAINT fkCPUComputador FOREIGN KEY (fkComputador) REFERENCES computador(idComputador) ON DELETE CASCADE
);

create table Memoria (
idMemoria INT PRIMARY KEY AUTO_INCREMENT,
tamanho DOUBLE,
fkComputador INT,
CONSTRAINT fkMemoriaComputador FOREIGN KEY (fkComputador) REFERENCES computador(idComputador) ON DELETE CASCADE
);


create table Disco (
idDisco int primary key auto_increment,
capacidade double,
sistemaArquivos varchar(100),
montagem varchar(100),
fkComputador INT,
CONSTRAINT fkDiscoComputador FOREIGN KEY (fkComputador) REFERENCES computador(idComputador) ON DELETE CASCADE
);

create table metricaCPU (
idMetricaCPU int primary key auto_increment,
dataHora timestamp default current_timestamp,
percentualUso double,
fkCPU int,
CONSTRAINT fkCPUMetrica foreign key (fkCPU) references cpu (idCpu) ON DELETE CASCADE
);


create table metricaMemoria (
idMetricaMemoria int primary key auto_increment,
dataHora timestamp default current_timestamp,
percentualUso double,
quantidadeLivre double,
quantidadeUsada double,
fkMemoria int,
CONSTRAINT fkMemoriaMetrica foreign key (fkMemoria) references memoria (idMemoria) ON DELETE CASCADE
);
DELETE FROM computador where idComputador > 0;

show tables;