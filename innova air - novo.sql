create database if not exists innovaair;
use innovaair;


CREATE TABLE IF NOT EXISTS `innovaair`.`Cliente` (
  `idCliente` INT NOT NULL AUTO_INCREMENT,
  `razaoSocial` VARCHAR(105) NULL,
  `CNPJ` CHAR(14) NULL,
  `email` VARCHAR(255) NULL,
  `telefone` VARCHAR(11) NULL,
  `resposanvel` VARCHAR(50) NULL,
  PRIMARY KEY (`idCliente`));

  CREATE TABLE IF NOT EXISTS `innovaair`.`Usuario` (
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NULL,
  `tipoUsuario` TINYINT NULL,
  `email` VARCHAR(255) NULL,
  `senha` VARCHAR(30) NULL,
  `fkCliente` INT NOT NULL,
  PRIMARY KEY (`idUsuario`),
  INDEX `fk_Usuario_Cliente_idx` (`fkCliente` ASC) VISIBLE,
  CONSTRAINT `fk_Usuario_Cliente`
    FOREIGN KEY (`fkCliente`)
    REFERENCES `innovaair`.`Cliente` (`idCliente`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

    CREATE TABLE IF NOT EXISTS `innovaair`.`Filial` (
  `idFilial` INT NOT NULL AUTO_INCREMENT,
  `aeroporto` VARCHAR(50) NULL,
  `terminal` VARCHAR(30) NULL,
  `setor` VARCHAR(30) NULL,
  `fkCliente` INT NOT NULL,
  PRIMARY KEY (`idFilial`),
  INDEX `fk_Filial_Cliente1_idx` (`fkCliente` ASC) VISIBLE,
  CONSTRAINT `fk_Filial_Cliente1`
    FOREIGN KEY (`fkCliente`)
    REFERENCES `innovaair`.`Cliente` (`idCliente`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

CREATE TABLE IF NOT EXISTS `innovaair`.`Computador` (
  `idComputador` INT NOT NULL AUTO_INCREMENT,
  `apelido` VARCHAR(100) NULL,
  `codigoMaquina` VARCHAR(100) NULL,
  `sistemaOperacional` VARCHAR(100) NULL,
  `hostname` VARCHAR(100) NULL,
  `arquitetura` VARCHAR(100) NULL,
  `fkFilial` INT NOT NULL,
  PRIMARY KEY (`idComputador`),
  INDEX `fk_Maquina_Filial1_idx` (`fkFilial` ASC) VISIBLE,
  CONSTRAINT `fk_Maquina_Filial1`
    FOREIGN KEY (`fkFilial`)
    REFERENCES `innovaair`.`Filial` (`idFilial`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

    CREATE TABLE IF NOT EXISTS `innovaair`.`CPU` (
  `idCpu` INT NOT NULL AUTO_INCREMENT,
  `modelo` VARCHAR(45) NULL,
  `frequencia` DOUBLE NULL,
  `cores` INT NULL,
  `fkComputador` INT NOT NULL,
  PRIMARY KEY (`idCpu`, `fkComputador`),
  INDEX `fk_CPU_Computador1_idx` (`fkComputador` ASC) VISIBLE,
  CONSTRAINT `fk_CPU_Computador1`
    FOREIGN KEY (`fkComputador`)
    REFERENCES `innovaair`.`Computador` (`idComputador`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

CREATE TABLE IF NOT EXISTS `innovaair`.`Disco` (
  `idDisco` INT NOT NULL AUTO_INCREMENT,
  `tipo` CHAR(3) NULL,
  `capacidade` DOUBLE NULL,
  `montagem` VARCHAR(45) NULL,
  `sistemaArquivos` VARCHAR(45) NULL,
  `fkComputador` INT NOT NULL,
  PRIMARY KEY (`idDisco`, `fkComputador`),
  INDEX `fk_Disco_Computador1_idx` (`fkComputador` ASC) VISIBLE,
  CONSTRAINT `fk_Disco_Computador1`
    FOREIGN KEY (`fkComputador`)
    REFERENCES `innovaair`.`Computador` (`idComputador`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


CREATE TABLE IF NOT EXISTS `innovaair`.`Memoria` (
  `idMemoria` INT NOT NULL AUTO_INCREMENT,
  `tamanho` DOUBLE NULL,
  `fkComputador` INT NOT NULL,
  PRIMARY KEY (`idMemoria`, `fkComputador`),
  INDEX `fk_Memoria_Computador1_idx` (`fkComputador` ASC) INVISIBLE,
  CONSTRAINT `fk_Memoria_Computador1`
    FOREIGN KEY (`fkComputador`)
    REFERENCES `innovaair`.`Computador` (`idComputador`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);
    
    CREATE TABLE IF NOT EXISTS `innovaair`.`Metrica` (
  `idMetrica` INT NOT NULL AUTO_INCREMENT,
  `nomeComponente` VARCHAR(45) NULL,
  `unidadeMedida` VARCHAR(10) NULL,
  `nomeMetrica` VARCHAR(45) NULL,
  PRIMARY KEY (`idMetrica`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `innovaair`.`Threshold` (
  `fkComputador` INT NOT NULL,
  `fkMetrica` INT NOT NULL,
  `minimo` DOUBLE NULL,
  `maximo` DOUBLE NULL,
  PRIMARY KEY (`fkComputador`, `fkMetrica`),
  INDEX `fk_Computador_has_Metrica_Metrica1_idx` (`fkMetrica` ASC) VISIBLE,
  INDEX `fk_Computador_has_Metrica_Computador1_idx` (`fkComputador` ASC) VISIBLE,
  CONSTRAINT `fk_Computador_has_Metrica_Computador1`
    FOREIGN KEY (`fkComputador`)
    REFERENCES `innovaair`.`Computador` (`idComputador`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Computador_has_Metrica_Metrica1`
    FOREIGN KEY (`fkMetrica`)
    REFERENCES `innovaair`.`Metrica` (`idMetrica`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `innovaair`.`Registro` (
  `idRegistro` INT NOT NULL AUTO_INCREMENT,
  `cpu_percentual` DOUBLE NULL,
  `ram_disponivel_percentual` DOUBLE NULL,
  `ram_disponivel_gb` DOUBLE NULL,
  `disco_uso_percentual` VARCHAR(45) NULL,
  `disco_disponivel_gb` VARCHAR(45) NULL,
  `dataHora` DATETIME NULL,
  PRIMARY KEY (`idRegistro`))
ENGINE = InnoDB;



INSERT INTO `innovaair`.`Cliente` (`razaoSocial`, `CNPJ`, `email`, `telefone`, `resposanvel`)
VALUES
('InovAir Soluções em TI', '12345678000199', 'contato@inovair.com', '11987654321', 'João Silva'),
('AeroTech Consultoria', '98765432000111', 'contato@aerotech.com', '21987654321', 'Maria Oliveira'),
('CloudNova Serviços', '45678912000122', 'contato@cloudnova.com', '31987654321', 'Carlos Souza');

INSERT INTO `innovaair`.`Usuario` (`nome`, `tipoUsuario`, `email`, `senha`, `fkCliente`)
VALUES
('Ana Costa', 1, 'ana.costa@inovair.com', 'senha123', 1),
('Pedro Alves', 2, 'pedro.alves@aerotech.com', 'senha456', 2),
('Luiza Fernandes', 1, 'luiza.fernandes@cloudnova.com', 'senha789', 3);

INSERT INTO `innovaair`.`Filial` (`aeroporto`, `terminal`, `setor`, `fkCliente`)
VALUES
('Aeroporto de Guarulhos', 'Terminal 1', 'Setor A', 1),
('Aeroporto Santos Dumont', 'Terminal 2', 'Setor B', 2),
('Aeroporto de Confins', 'Terminal 1', 'Setor C', 3);

insert into Metrica (nomeComponente, unidadeMedida, nomeMetrica) VALUES
('CPU', '%', 'Percentual de uso da CPU'),
('RAM', '%', 'Percentual de uso da RAM'),
('Disco', '%', 'Percentual de uso do disco'),
('Disco', 'GB', 'GB usados no disco'),
('RAM', 'GB', 'GB usados da RAM');



