SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`tb_perfil`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_perfil` (
  `id_perfil` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id do Perfil de Usuario',
  `nome` VARCHAR(20) NOT NULL COMMENT 'Nome do Perfil de Usuario',
  `ativo` TINYINT UNSIGNED NOT NULL,
  UNIQUE INDEX `idPerfil` (`id_perfil` ASC),
  PRIMARY KEY (`id_perfil`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `mydb`.`tb_usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_usuario` (
  `id_usuario` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id do Usuario do Sistema',
  `fk_id_perfil` INT(11) UNSIGNED NOT NULL,
  `nome` VARCHAR(80) NOT NULL,
  `email` VARCHAR(200) NOT NULL COMMENT 'Email do Usuario',
  `senha` VARCHAR(128) NOT NULL COMMENT 'Senha Do Usuario',
  `numero_filhos` INT UNSIGNED NULL,
  `ano_escolar` INT NULL,
  `colegio` VARCHAR(70) NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  UNIQUE INDEX `idUsuario` (`id_usuario` ASC),
  PRIMARY KEY (`id_usuario`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  INDEX `fk_tb_usuario_tb_perfil1_idx` (`fk_id_perfil` ASC),
  CONSTRAINT `fk_tb_usuario_tb_perfil1`
    FOREIGN KEY (`fk_id_perfil`)
    REFERENCES `mydb`.`tb_perfil` (`id_perfil`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `mydb`.`tb_operacao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_operacao` (
  `id_operacao` INT(11) UNSIGNED NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_operacao`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_erro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_erro` (
  `id_erro` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `excessao` TEXT NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_erro`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_perfil_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_perfil_his` (
  `id_perfil_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_perfil` INT(11) UNSIGNED NOT NULL,
  `nome` VARCHAR(20) NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_usuario_operacao` INT(11) UNSIGNED NOT NULL,
  `fk_id_operacao` INT UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_perfil_his`),
  INDEX `fk_tb_perfil_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  INDEX `fk_tb_perfil_his_tb_usuario1_idx` (`fk_id_usuario_operacao` ASC),
  CONSTRAINT `fk_tb_perfil_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_perfil_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario_operacao`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_usuario_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_usuario_his` (
  `id_usuario_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_usuario` INT UNSIGNED NOT NULL,
  `fk_id_perfil` INT UNSIGNED NOT NULL,
  `nome` VARCHAR(80) NOT NULL,
  `email` VARCHAR(200) NOT NULL,
  `senha` VARCHAR(128) NOT NULL,
  `numero_filhos` INT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_usuario_operacao` INT(11) UNSIGNED NOT NULL,
  `fk_id_operacao` INT UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario_his`),
  UNIQUE INDEX `id_usuario_his_UNIQUE` (`id_usuario_his` ASC),
  INDEX `fk_tb_usuario_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  INDEX `fk_tb_usuario_his_tb_usuario1_idx` (`fk_id_usuario_operacao` ASC),
  CONSTRAINT `fk_tb_usuario_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_usuario_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario_operacao`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_pais`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_pais` (
  `id_pais` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(50) NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_pais`),
  UNIQUE INDEX `id_pais_UNIQUE` (`id_pais` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_pais_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_pais_his` (
  `id_pais_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_pais` INT UNSIGNED NOT NULL,
  `nome` VARCHAR(50) NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_usuario_operacao` INT(11) UNSIGNED NOT NULL,
  `fk_id_operacao` INT(11) UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_pais_his`),
  UNIQUE INDEX `id_pais_his_UNIQUE` (`id_pais_his` ASC),
  INDEX `fk_tb_pais_his_tb_usuario1_idx` (`fk_id_usuario_operacao` ASC),
  INDEX `fk_tb_pais_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  CONSTRAINT `fk_tb_pais_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario_operacao`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_pais_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_estado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_estado` (
  `id_estado` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `fk_id_pais` INT UNSIGNED NOT NULL,
  `nome` VARCHAR(50) NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_estado`),
  UNIQUE INDEX `id_estado_UNIQUE` (`id_estado` ASC),
  INDEX `fk_tb_estado_tb_pais1_idx` (`fk_id_pais` ASC),
  CONSTRAINT `fk_tb_estado_tb_pais1`
    FOREIGN KEY (`fk_id_pais`)
    REFERENCES `mydb`.`tb_pais` (`id_pais`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_estado_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_estado_his` (
  `id_estado_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_estado` INT UNSIGNED NOT NULL,
  `fk_id_pais` INT UNSIGNED NOT NULL,
  `nome` VARCHAR(50) NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_usuario_operacao` INT(11) UNSIGNED NOT NULL,
  `fk_id_operacao` INT(11) UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_estado_his`),
  UNIQUE INDEX `id_estado_his_UNIQUE` (`id_estado_his` ASC),
  INDEX `fk_tb_estado_his_tb_usuario1_idx` (`fk_id_usuario_operacao` ASC),
  INDEX `fk_tb_estado_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  CONSTRAINT `fk_tb_estado_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario_operacao`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_estado_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_cidade`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_cidade` (
  `id_cidade` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `fk_id_estado` INT UNSIGNED NOT NULL,
  `nome` VARCHAR(80) NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_cidade`),
  UNIQUE INDEX `id_cidade_UNIQUE` (`id_cidade` ASC),
  INDEX `fk_tb_cidade_tb_estado1_idx` (`fk_id_estado` ASC),
  CONSTRAINT `fk_tb_cidade_tb_estado1`
    FOREIGN KEY (`fk_id_estado`)
    REFERENCES `mydb`.`tb_estado` (`id_estado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_cidade_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_cidade_his` (
  `id_cidade_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_cidade` INT UNSIGNED NOT NULL,
  `fk_id_estado` INT UNSIGNED NOT NULL,
  `nome` VARCHAR(80) NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_usuario_operacao` INT(11) UNSIGNED NOT NULL,
  `fk_id_operacao` INT(11) UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_cidade_his`),
  UNIQUE INDEX `id_cidade_his_UNIQUE` (`id_cidade_his` ASC),
  INDEX `fk_tb_cidade_his_tb_usuario1_idx` (`fk_id_usuario_operacao` ASC),
  INDEX `fk_tb_cidade_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  CONSTRAINT `fk_tb_cidade_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario_operacao`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_cidade_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_endereco`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_endereco` (
  `id_endereco` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `fk_id_usuario` INT(11) UNSIGNED NOT NULL,
  `fk_id_cidade` INT UNSIGNED NOT NULL,
  `endereco` VARCHAR(250) NOT NULL,
  `complemento` VARCHAR(100) NULL,
  `CEP` INT UNSIGNED NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_endereco`),
  UNIQUE INDEX `id_endereco_UNIQUE` (`id_endereco` ASC),
  INDEX `fk_tb_endereco_tb_usuario1_idx` (`fk_id_usuario` ASC),
  INDEX `fk_tb_endereco_tb_cidade1_idx` (`fk_id_cidade` ASC),
  CONSTRAINT `fk_tb_endereco_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_endereco_tb_cidade1`
    FOREIGN KEY (`fk_id_cidade`)
    REFERENCES `mydb`.`tb_cidade` (`id_cidade`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_endereco_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_endereco_his` (
  `id_endereco_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_endereco` INT UNSIGNED NOT NULL,
  `fk_id_usuario` INT UNSIGNED NOT NULL,
  `fk_id_cidade` INT UNSIGNED NOT NULL,
  `endereco` VARCHAR(250) NOT NULL,
  `complemento` VARCHAR(100) NULL,
  `CEP` INT UNSIGNED NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_usuario_operacao` INT(11) UNSIGNED NOT NULL,
  `fk_id_operacao` INT(11) UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_endereco_his`),
  UNIQUE INDEX `id_endereco_his_UNIQUE` (`id_endereco_his` ASC),
  INDEX `fk_tb_endereco_his_tb_usuario1_idx` (`fk_id_usuario_operacao` ASC),
  INDEX `fk_tb_endereco_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  CONSTRAINT `fk_tb_endereco_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario_operacao`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_endereco_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_telefone`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_telefone` (
  `id_telefone` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `fk_id_usuario` INT(11) UNSIGNED NOT NULL,
  `numero` INT UNSIGNED NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_telefone`),
  UNIQUE INDEX `id_telefone_UNIQUE` (`id_telefone` ASC),
  INDEX `fk_tb_telefone_tb_usuario1_idx` (`fk_id_usuario` ASC),
  CONSTRAINT `fk_tb_telefone_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_telefone_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_telefone_his` (
  `id_telefone_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_telefone` INT UNSIGNED NOT NULL,
  `fk_id_usuario` INT UNSIGNED NOT NULL,
  `numero` INT UNSIGNED NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_usuario_operacao` INT(11) UNSIGNED NOT NULL,
  `fk_id_operacao` INT(11) UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_telefone_his`),
  UNIQUE INDEX `id_telefone_his_UNIQUE` (`id_telefone_his` ASC),
  INDEX `fk_tb_telefone_his_tb_usuario1_idx` (`fk_id_usuario_operacao` ASC),
  INDEX `fk_tb_telefone_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  CONSTRAINT `fk_tb_telefone_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario_operacao`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_telefone_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_curso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_curso` (
  `id_curso` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(70) NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_curso`),
  UNIQUE INDEX `id_curso_UNIQUE` (`id_curso` ASC),
  UNIQUE INDEX `nome_UNIQUE` (`nome` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_curso_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_curso_his` (
  `id_curso_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_curso` INT UNSIGNED NOT NULL,
  `nome` VARCHAR(70) NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_usuario_operacao` INT(11) UNSIGNED NOT NULL,
  `fk_id_operacao` INT(11) UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_curso_his`),
  UNIQUE INDEX `id_curso_his_UNIQUE` (`id_curso_his` ASC),
  INDEX `fk_tb_curso_his_tb_usuario1_idx` (`fk_id_usuario_operacao` ASC),
  INDEX `fk_tb_curso_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  CONSTRAINT `fk_tb_curso_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario_operacao`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_curso_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ta_usuario_x_curso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ta_usuario_x_curso` (
  `id_usuario` INT(11) UNSIGNED NOT NULL,
  `id_curso` INT UNSIGNED NOT NULL,
  `finalizado` TINYINT UNSIGNED NOT NULL COMMENT '0 - não\n1 - si' /* comment truncated */ /*
*/,
  `semestre` INT UNSIGNED NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_usuario`, `id_curso`),
  INDEX `fk_tb_usuario_has_tb_curso_tb_curso1_idx` (`id_curso` ASC),
  INDEX `fk_tb_usuario_has_tb_curso_tb_usuario1_idx` (`id_usuario` ASC),
  CONSTRAINT `fk_tb_usuario_has_tb_curso_tb_usuario1`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_usuario_has_tb_curso_tb_curso1`
    FOREIGN KEY (`id_curso`)
    REFERENCES `mydb`.`tb_curso` (`id_curso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `mydb`.`ta_usuario_x_curso_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ta_usuario_x_curso_his` (
  `id_usuario_x_curso_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_usuario` INT UNSIGNED NOT NULL,
  `id_curso` INT UNSIGNED NOT NULL,
  `finalizado` TINYINT UNSIGNED NOT NULL,
  `semestre` INT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_usuario_operacao` INT(11) UNSIGNED NOT NULL,
  `fk_id_operacao` INT(11) UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario_x_curso_his`),
  UNIQUE INDEX `id_usuario_x_curso_his_UNIQUE` (`id_usuario_x_curso_his` ASC),
  INDEX `fk_ta_usuario_x_curso_his_tb_usuario1_idx` (`fk_id_usuario_operacao` ASC),
  INDEX `fk_ta_usuario_x_curso_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  CONSTRAINT `fk_ta_usuario_x_curso_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario_operacao`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ta_usuario_x_curso_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_materia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_materia` (
  `id_materia` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(50) NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_materia`),
  UNIQUE INDEX `id_materia_UNIQUE` (`id_materia` ASC),
  UNIQUE INDEX `nome_UNIQUE` (`nome` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_materia_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_materia_his` (
  `id_materia_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_materia` INT UNSIGNED NOT NULL,
  `nome` VARCHAR(50) NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_usuario_operacao` INT(11) UNSIGNED NOT NULL,
  `fk_id_operacao` INT(11) UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_materia_his`),
  UNIQUE INDEX `id_material_his_UNIQUE` (`id_materia_his` ASC),
  INDEX `fk_tb_materia_his_tb_usuario1_idx` (`fk_id_usuario_operacao` ASC),
  INDEX `fk_tb_materia_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  CONSTRAINT `fk_tb_materia_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario_operacao`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_materia_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ta_usuario_x_materia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ta_usuario_x_materia` (
  `id_usuario` INT(11) UNSIGNED NOT NULL,
  `id_materia` INT UNSIGNED NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_usuario`, `id_materia`),
  INDEX `fk_tb_usuario_has_tb_materia_tb_materia1_idx` (`id_materia` ASC),
  INDEX `fk_tb_usuario_has_tb_materia_tb_usuario1_idx` (`id_usuario` ASC),
  CONSTRAINT `fk_tb_usuario_has_tb_materia_tb_usuario1`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_usuario_has_tb_materia_tb_materia1`
    FOREIGN KEY (`id_materia`)
    REFERENCES `mydb`.`tb_materia` (`id_materia`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `mydb`.`ta_usuario_x_materia_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ta_usuario_x_materia_his` (
  `id_usuario_x_materia_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_usuario` INT UNSIGNED NOT NULL,
  `id_materia` INT UNSIGNED NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_usuario_operacao` INT(11) UNSIGNED NOT NULL,
  `fk_id_operacao` INT(11) UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario_x_materia_his`),
  UNIQUE INDEX `id_usuario_x_materia_his_UNIQUE` (`id_usuario_x_materia_his` ASC),
  INDEX `fk_ta_usuario_x_materia_his_tb_usuario1_idx` (`fk_id_usuario_operacao` ASC),
  INDEX `fk_ta_usuario_x_materia_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  CONSTRAINT `fk_ta_usuario_x_materia_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario_operacao`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ta_usuario_x_materia_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_horario_livre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_horario_livre` (
  `id_horario_livre` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `fk_id_usuario` INT(11) UNSIGNED NOT NULL,
  `horario_inicial` TIME NOT NULL,
  `horario_final` TIME NOT NULL,
  `data_horario_livre` DATE NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_horario_livre`),
  UNIQUE INDEX `id_horario_livre_UNIQUE` (`id_horario_livre` ASC),
  INDEX `fk_tb_horario_livre_tb_usuario1_idx` (`fk_id_usuario` ASC),
  CONSTRAINT `fk_tb_horario_livre_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_horario_livre_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_horario_livre_his` (
  `id_horario_livre_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_horario_livre` INT UNSIGNED NOT NULL,
  `fk_id_usuario` INT UNSIGNED NOT NULL,
  `horario_inicial` TIME NOT NULL,
  `horario_final` TIME NOT NULL,
  `data_horario_livre` DATE NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_operacao` INT(11) UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_horario_livre_his`),
  UNIQUE INDEX `id_horario_livre_his_UNIQUE` (`id_horario_livre_his` ASC),
  INDEX `fk_tb_horario_livre_his_tb_usuario1_idx` (`fk_id_usuario` ASC),
  INDEX `fk_tb_horario_livre_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  CONSTRAINT `fk_tb_horario_livre_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_horario_livre_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_aula`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_aula` (
  `id_aula` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `fk_id_usuario_pai` INT(11) UNSIGNED NOT NULL,
  `fk_id_usuario_aluno` INT(11) UNSIGNED NOT NULL,
  `fk_id_usuario_professor` INT(11) UNSIGNED NOT NULL,
  `horario_inicial` TIME NOT NULL,
  `horario_final` TIME NOT NULL,
  `data_aula` DATE NOT NULL,
  `conteudo` TEXT NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_aula`),
  UNIQUE INDEX `id_aula_UNIQUE` (`id_aula` ASC),
  INDEX `fk_tb_aula_tb_usuario1_idx` (`fk_id_usuario_pai` ASC),
  INDEX `fk_tb_aula_tb_usuario2_idx` (`fk_id_usuario_aluno` ASC),
  INDEX `fk_tb_aula_tb_usuario3_idx` (`fk_id_usuario_professor` ASC),
  CONSTRAINT `fk_tb_aula_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario_pai`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_aula_tb_usuario2`
    FOREIGN KEY (`fk_id_usuario_aluno`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_aula_tb_usuario3`
    FOREIGN KEY (`fk_id_usuario_professor`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ta_aula_x_materia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ta_aula_x_materia` (
  `id_aula` INT UNSIGNED NOT NULL,
  `id_materia` INT UNSIGNED NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_aula`, `id_materia`),
  INDEX `fk_tb_aula_has_tb_materia_tb_materia1_idx` (`id_materia` ASC),
  INDEX `fk_tb_aula_has_tb_materia_tb_aula1_idx` (`id_aula` ASC),
  CONSTRAINT `fk_tb_aula_has_tb_materia_tb_aula1`
    FOREIGN KEY (`id_aula`)
    REFERENCES `mydb`.`tb_aula` (`id_aula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_aula_has_tb_materia_tb_materia1`
    FOREIGN KEY (`id_materia`)
    REFERENCES `mydb`.`tb_materia` (`id_materia`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_aula_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_aula_his` (
  `id_aula_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_aula` INT UNSIGNED NOT NULL,
  `fk_id_usuario_pai` INT UNSIGNED NOT NULL,
  `fk_id_usuario_aluno` INT UNSIGNED NOT NULL,
  `fk_id_usuario_professor` INT UNSIGNED NOT NULL,
  `horario_inicial` TIME NOT NULL,
  `horario_final` TIME NOT NULL,
  `data_aula` DATE NOT NULL,
  `conteudo` TEXT NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_usuario` INT(11) UNSIGNED NOT NULL,
  `fk_id_operacao` INT(11) UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_aula_his`),
  UNIQUE INDEX `id_aula_his_UNIQUE` (`id_aula_his` ASC),
  INDEX `fk_tb_aula_his_tb_usuario1_idx` (`fk_id_usuario` ASC),
  INDEX `fk_tb_aula_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  CONSTRAINT `fk_tb_aula_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_aula_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ta_aula_x_materia_his`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ta_aula_x_materia_his` (
  `id_aula_x_materia_his` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_aula` INT UNSIGNED NOT NULL,
  `id_material` INT UNSIGNED NOT NULL,
  `ativo` TINYINT UNSIGNED NOT NULL,
  `fk_id_usuario` INT(11) UNSIGNED NOT NULL,
  `fk_id_operacao` INT(11) UNSIGNED NOT NULL,
  `data` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_aula_x_materia_his`),
  UNIQUE INDEX `id_aula_x_materia_his_UNIQUE` (`id_aula_x_materia_his` ASC),
  INDEX `fk_ta_aula_x_materia_his_tb_usuario1_idx` (`fk_id_usuario` ASC),
  INDEX `fk_ta_aula_x_materia_his_tb_operacao1_idx` (`fk_id_operacao` ASC),
  CONSTRAINT `fk_ta_aula_x_materia_his_tb_usuario1`
    FOREIGN KEY (`fk_id_usuario`)
    REFERENCES `mydb`.`tb_usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ta_aula_x_materia_his_tb_operacao1`
    FOREIGN KEY (`fk_id_operacao`)
    REFERENCES `mydb`.`tb_operacao` (`id_operacao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
