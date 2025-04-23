# DROP DATABASE innovaair;

CREATE DATABASE IF NOT EXISTS innovaair;
USE innovaair;

# CRIAÇÃO DAS TABELAS
CREATE TABLE IF NOT EXISTS cliente (
  idCliente INT PRIMARY KEY AUTO_INCREMENT,
  razaoSocial VARCHAR(105) NOT NULL,
  cnpj CHAR(14) NOT NULL,
  email VARCHAR(255) NOT NULL,
  telefone VARCHAR(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS cargo (
  idCargo INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(45) NOT NULL,
  nivelAcesso INT NOT NULL
);

CREATE TABLE IF NOT EXISTS usuario (
  idUsuario INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(45) NOT NULL,
  email VARCHAR(255) NOT NULL,
  senha VARCHAR(30) NOT NULL,
  fkCliente INT NOT NULL,
  fkCargo INT NOT NULL,
  CONSTRAINT fk_usuario_cliente FOREIGN KEY (fkCliente) REFERENCES cliente (idCliente),
  CONSTRAINT fk_usuario_cargo FOREIGN KEY (fkCargo) REFERENCES cargo(idCargo)
);

CREATE TABLE IF NOT EXISTS endereco (
  idEndereco INT PRIMARY KEY AUTO_INCREMENT,
  cep CHAR(9) NOT NULL,
  logradouro VARCHAR(100) NOT NULL,
  numero VARCHAR(45) NOT NULL,
  complemento VARCHAR(45),
  bairro VARCHAR(45) NOT NULL,
  cidade VARCHAR(45) NOT NULL,
  estado VARCHAR(45) NOT NULL,
  regiao VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS filial (
  idFilial INT PRIMARY KEY AUTO_INCREMENT,
  terminal VARCHAR(30) NOT NULL,
  setor VARCHAR(30) NOT NULL,
  fkCliente INT NOT NULL,
  fkEndereco INT NOT NULL,
  CONSTRAINT fk_filial_cliente FOREIGN KEY (fkCliente) REFERENCES cliente (idCliente),
  CONSTRAINT fk_filial_endereco FOREIGN KEY (fkEndereco) REFERENCES endereco (idEndereco)
);

CREATE TABLE IF NOT EXISTS usuarioFilial(
	fkUsuario INT NOT NULL,
    fkFilial INT NOT NULL,
    primary key (fkUsuario, fkFilial)
);

CREATE TABLE IF NOT EXISTS maquina (
  idMaquina INT PRIMARY KEY AUTO_INCREMENT,
  fkFilial INT NOT NULL, #Fk Não-Relacional // Por ser outro database
  numeroSerial VARCHAR(45) NOT NULL,
  enderecoMac VARCHAR(45) NOT NULL,
  hostname VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS componente (
  idComponente INT PRIMARY KEY AUTO_INCREMENT,
  fkMaquina INT NOT NULL,
  componente VARCHAR(45) NOT NULL,
  especificacao VARCHAR(100) NOT NULL,
  CONSTRAINT fk_componente_maquina FOREIGN KEY (fkMaquina) REFERENCES maquina (idMaquina)
);

CREATE TABLE IF NOT EXISTS metrica (
  idMetrica INT PRIMARY KEY AUTO_INCREMENT,
  metrica VARCHAR(45) NOT NULL,
  limiteMaximo INT,
  limiteMinimo INT,
  fkComponente INT NOT NULL,
  CONSTRAINT fk_metrica_componente FOREIGN KEY (fkComponente) REFERENCES componente (idComponente)
);

CREATE TABLE IF NOT EXISTS captura_alerta (
  idCapturaAlerta INT PRIMARY KEY AUTO_INCREMENT,
  valorCapturado FLOAT NOT NULL,
  momento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  gravidade VARCHAR(20) NOT NULL,
  fkMetrica INT NOT NULL,
  CONSTRAINT fk_alerta_metrica FOREIGN KEY (fkMetrica) REFERENCES metrica (idMetrica)
);

CREATE TABLE IF NOT EXISTS captura_historico (
  idCapturaHistorico INT PRIMARY KEY AUTO_INCREMENT,
  valorCapturado FLOAT NOT NULL,
  momento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fkMetrica INT NOT NULL,
  CONSTRAINT fk_historico_metrica FOREIGN KEY (fkMetrica) REFERENCES metrica (idMetrica)
);

INSERT INTO cliente (razaoSocial, cnpj, email, telefone)
VALUES ('TAM LINHAS AÉREAS S.A. A LATAM', '12345678000188', 'contato@latam.com.br', '1133224455');

INSERT INTO endereco VALUES
(default, '04626-911', 'Av. Washington Luís', 'S/N',  'Aeroporto de Congonhas', 'Campo Belo', 'São Paulo', 'SP', 'Sudeste');

INSERT INTO filial VALUES
(default, "1", "1", 1, 1);

INSERT INTO cargo VALUES
(1, 'Gerente', 7);

INSERT INTO usuario VALUES
(default, 'Roberto', 'roberto@latam.com', '123456', 1, 1);

SELECT * from maquina;
SELECT * from componente;
SELECT * from metrica;
SELECT idComponente, componente, metrica, limiteMinimo, limiteMaximo, idMetrica from componente join maquina on idMaquina = fkMaquina join metrica on idComponente = fkComponente where idMaquina = 1;
desc captura_historico;
select * from captura_historico;
SELECT razaoSocial, idFilial, idMaquina, componente, especificacao, metrica, valorCapturado, momento from maquina join componente on idMaquina = fkMaquina join metrica on idComponente = fkComponente join captura_historico on idMetrica = fkMetrica join filial on idFilial = fkFilial join cliente on idCliente = fkCliente;
# Trigger para inserir os alertas
/*
DELIMITER //
CREATE TRIGGER after_insert_captura
AFTER INSERT ON captura_historico
FOR EACH ROW
BEGIN
    DECLARE v_limite_max INT;
	DECLARE v_limite_min INT;

    -- Busca o limiteMaximo da métrica correspondente
    SELECT limiteMaximo, limiteMinimo
    INTO v_limite_max, v_limite_min
    FROM metrica
    WHERE idMetrica = NEW.fkMetrica;
    
    -- Se o valor da nova captura for maior que o limite, cria alerta
    IF NEW.valorCapturado > v_limite_max THEN
        INSERT INTO captura_alerta (valorCapturado, momento, fkMetrica, gravidade)
        VALUES (NEW.valorCapturado, NOW(), NEW.fkMetrica, 'Grave');
    ELSEIF NEW.valorCapturado >= ((v_limite_min + v_limite_min)/2) and NEW.valorCapturado < v_limite_max THEN
		INSERT INTO captura_alerta (valorCapturado, momento, fkMetrica, gravidade)
        VALUES (NEW.valorCapturado, NOW(), NEW.fkMetrica, 'Médio');
	ELSEIF NEW.valorCapturado < ((v_limite_min + v_limite_min)/2) and NEW.valorCapturado > v_limite_min THEN
		INSERT INTO captura_alerta (valorCapturado, momento, fkMetrica, gravidade)
        VALUES (NEW.valorCapturado, NOW(), NEW.fkMetrica, 'Baixo');   
	ELSE 
		INSERT INTO captura_alerta (valorCapturado, momento, fkMetrica, gravidade)
        VALUES (NEW.valorCapturado, NOW(), NEW.fkMetrica, 'Nenhuma');
    END IF;
END//
DELIMITER ;
