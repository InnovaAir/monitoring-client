CREATE DATABASE IF NOT EXISTS innovair;
USE innovair;

CREATE TABLE IF NOT EXISTS Cliente (
  idCliente INT NOT NULL AUTO_INCREMENT,
  razaoSocial VARCHAR(105),
  CNPJ VARCHAR(18),
  email VARCHAR(255),
  telefone VARCHAR(15),
  responsavel VARCHAR(50),
  PRIMARY KEY (idCliente)
);

CREATE TABLE IF NOT EXISTS Usuario (
  idUsuario INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(45),
  tipoUsuario TINYINT,
  email VARCHAR(255),
  senha VARCHAR(100),
  fkCliente INT NOT NULL,
  PRIMARY KEY (idUsuario),
  INDEX fk_Usuario_Cliente_idx (fkCliente),
  CONSTRAINT fk_Usuario_Cliente FOREIGN KEY (fkCliente)
    REFERENCES Cliente (idCliente)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Filial (
  idFilial INT NOT NULL AUTO_INCREMENT,
  aeroporto VARCHAR(50),
  terminal VARCHAR(30),
  setor VARCHAR(30),
  fkCliente INT NOT NULL,
  PRIMARY KEY (idFilial),
  INDEX fk_Filial_Cliente1_idx (fkCliente),
  CONSTRAINT fk_Filial_Cliente1 FOREIGN KEY (fkCliente)
    REFERENCES Cliente (idCliente)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Computador (
  idComputador INT NOT NULL AUTO_INCREMENT,
  apelido VARCHAR(100),
  numeroSeriePlacaMae VARCHAR(100),
  sistemaOperacional VARCHAR(100),
  hostname VARCHAR(100),
  arquitetura VARCHAR(100),
  fkFilial INT NOT NULL,
  PRIMARY KEY (idComputador),
  INDEX fk_Maquina_Filial1_idx (fkFilial),
  CONSTRAINT fk_Maquina_Filial1 FOREIGN KEY (fkFilial)
    REFERENCES Filial (idFilial)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS CPU (
  idCpu INT NOT NULL AUTO_INCREMENT,
  modelo VARCHAR(45),
  frequencia DOUBLE,
  cores INT,
  fkComputador INT NOT NULL,
  PRIMARY KEY (idCpu),
  INDEX fk_CPU_Computador1_idx (fkComputador),
  CONSTRAINT fk_CPU_Computador1 FOREIGN KEY (fkComputador)
    REFERENCES Computador (idComputador)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Disco (
  idDisco INT NOT NULL AUTO_INCREMENT,
  tipo CHAR(3),
  capacidade DOUBLE,
  montagem VARCHAR(45),
  sistemaArquivos VARCHAR(45),
  fkComputador INT NOT NULL,
  PRIMARY KEY (idDisco),
  INDEX fk_Disco_Computador1_idx (fkComputador),
  CONSTRAINT fk_Disco_Computador1 FOREIGN KEY (fkComputador)
    REFERENCES Computador (idComputador)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Memoria (
  idMemoria INT NOT NULL AUTO_INCREMENT,
  tamanho DOUBLE,
  fkComputador INT NOT NULL,
  PRIMARY KEY (idMemoria),
  INDEX fk_Memoria_Computador1_idx (fkComputador),
  CONSTRAINT fk_Memoria_Computador1 FOREIGN KEY (fkComputador)
    REFERENCES Computador (idComputador)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS MetricaCPU (
  idMetricaCPU INT NOT NULL AUTO_INCREMENT,
  dataHora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  percentualUso DOUBLE,
  fkCpu INT NOT NULL,
  PRIMARY KEY (idMetricaCPU),
  INDEX fk_MetricaCPU_CPU1_idx (fkCpu),
  CONSTRAINT fk_MetricaCPU_CPU1 FOREIGN KEY (fkCpu)
    REFERENCES CPU (idCpu)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS MetricaMemoria (
  idMetricaMemoria INT NOT NULL AUTO_INCREMENT,
  dataHora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  percentualUso DOUBLE,
  quantidadeLivre DOUBLE,
  quantidadeUsada DOUBLE,
  fkMemoria INT NOT NULL,
  PRIMARY KEY (idMetricaMemoria),
  INDEX fk_MetricaMemoria_Memoria1_idx (fkMemoria),
  CONSTRAINT fk_MetricaMemoria_Memoria1 FOREIGN KEY (fkMemoria)
    REFERENCES Memoria (idMemoria)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS MetricaDisco (
  idMetricaDisco INT NOT NULL AUTO_INCREMENT,
  dataHora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  percentualUso DOUBLE,
  quantidadeLivre DOUBLE,
  quantidadeUsada DOUBLE,
  fkDisco INT NOT NULL,
  PRIMARY KEY (idMetricaDisco),
  INDEX fk_MetricaDisco_Disco1_idx (fkDisco),
  CONSTRAINT fk_MetricaDisco_Disco1 FOREIGN KEY (fkDisco)
    REFERENCES Disco (idDisco)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- Inserts de exemplo

INSERT INTO Cliente (razaoSocial, CNPJ, email, telefone, responsavel)
VALUES ('Innova Ltda', '12345678000195', 'contato@innova.com', '11987654321', 'João Silva');

INSERT INTO Filial (aeroporto, terminal, setor, fkCliente)
VALUES ('Guarulhos', 'T1', 'TI', 1);

INSERT INTO Computador (apelido, numeroSeriePlacaMae, sistemaOperacional, hostname, arquitetura, fkFilial)
VALUES ('Comp01', 'ABC123456', 'Windows 10', 'comp01.local', 'x64', 1);

INSERT INTO CPU (modelo, frequencia, cores, fkComputador)
VALUES ('Intel Core i7', 3.6, 8, 1);

INSERT INTO Memoria (tamanho, fkComputador)
VALUES (16, 1);

INSERT INTO Disco (tipo, capacidade, montagem, sistemaArquivos, fkComputador)
VALUES ('SSD', 512, '/dev/sda1', 'NTFS', 1);

INSERT INTO MetricaCPU (percentualUso, fkCpu)
VALUES (45.2, 1), (50.8, 1), (38.5, 1), (60.3, 1), (72.1, 1);

INSERT INTO MetricaMemoria (percentualUso, quantidadeLivre, quantidadeUsada, fkMemoria)
VALUES (55.4, 4.5, 5.5, 1), (60.1, 3.8, 6.2, 1), (47.9, 5.3, 4.7, 1), (70.6, 2.9, 7.1, 1), (80.2, 2.1, 7.9, 1);

INSERT INTO MetricaDisco (percentualUso, quantidadeLivre, quantidadeUsada, fkDisco)
VALUES (40.2, 100.5, 67.8, 1), (55.8, 80.3, 90.1, 1), (72.6, 60.0, 120.4, 1), (81.3, 45.2, 135.6, 1), (92.7, 25.6, 154.3, 1);

SELECT dataHora, percentualUso FROM MetricaCPU ORDER BY dataHora DESC LIMIT 1;

SELECT dataHora, percentualUso FROM MetricaMemoria;
SELECT dataHora, quantidadeLivre, quantidadeUsada FROM MetricaMemoria;

SELECT dataHora, percentualUso FROM MetricaDisco;
SELECT dataHora, quantidadeLivre, quantidadeUsada FROM MetricaDisco;

SELECT 'Memória' AS Componente, mm.percentualUso AS mediaPercentual, mm.dataHora AS Horario
FROM MetricaMemoria mm
UNION ALL
SELECT 'Disco', md.percentualUso, md.dataHora
FROM MetricaDisco md
UNION ALL
SELECT 'CPU', mc.percentualUso, mc.dataHora
FROM MetricaCPU mc;

SELECT 'Memória' AS Componente, mm.quantidadeLivre AS mediaLivre, mm.quantidadeUsada AS mediaUsada, mm.dataHora AS Horario
FROM MetricaMemoria mm
UNION ALL
SELECT 'Disco', md.quantidadeLivre, md.quantidadeUsada, md.dataHora AS Horario
FROM MetricaDisco md;

SELECT md.dataHora, md.quantidadeLivre, md.quantidadeUsada
FROM MetricaDisco md
JOIN Disco d ON md.fkDisco = d.idDisco
JOIN Computador c ON d.fkComputador = c.idComputador
WHERE c.idComputador = 1
ORDER BY md.dataHora DESC;
