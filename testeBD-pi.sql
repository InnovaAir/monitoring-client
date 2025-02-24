CREATE DATABASE TesteProjetoPi;

USE TesteProjetoPi;

CREATE TABLE InfosComputer(
idRegistro int primary key auto_increment,
fkComputador int,
	CONSTRAINT fkIdComputador foreign key (fkComputador) references Computer(idComputador),
pacotesRecv float,
pacotesEnv float,
memVirtual float,
cpuUsada float,
tempoAtvd varchar(20),
discoUso float,
horarioLog datetime
);

CREATE TABLE Computer(
idComputador int primary key auto_increment,
SistemaOp varchar(30)
);

INSERT INTO Computer VALUES
(default, "MacOS");

SELECT * FROM Computer;
SELECT * FROM InfosComputer;

DROP TABLE InfosComputer;
