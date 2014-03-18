SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`perfil`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`perfil` (
  `idPerfil` INT(11) NOT NULL COMMENT 'id do Perfil de Usuario',
  `Nome` TEXT NOT NULL COMMENT 'Nome do Perfil de Usuario',
  UNIQUE INDEX `idPerfil` (`idPerfil` ASC),
  INDEX `idPerfil` (),
  PRIMARY KEY (`idPerfil`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `mydb`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`usuario` (
  `idUsuario` INT(11) NOT NULL COMMENT 'id do Usuario do Sistema',
  `Email` TEXT NOT NULL COMMENT 'Email do Usuario',
  `Senha` TEXT NOT NULL COMMENT 'Senha Do Usuario',
  `idPerfil` INT NULL,
  UNIQUE INDEX `idUsuario` (`idUsuario` ASC),
  PRIMARY KEY (`idUsuario`),
  INDEX `idPerfil_idx` (`idPerfil` ASC),
  CONSTRAINT `idPerfil`
    FOREIGN KEY (`idPerfil`)
    REFERENCES `mydb`.`perfil` (`idPerfil`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `mydb`.`regiao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`regiao` (
  `idRegiao` INT NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idRegiao`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`endereço`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`endereço` (
  `idRegiao` INT(11) NOT NULL COMMENT 'id Do Usuario do Sistema',
  `CEP` INT(11) NOT NULL COMMENT 'CEP',
  `Complemento` TEXT NOT NULL COMMENT 'Complemento do Endereço',
  `Telefone` INT(11) NOT NULL COMMENT 'Telefone da Residência',
  PRIMARY KEY (`idRegiao`),
  INDEX `idUsuario` (`idRegiao` ASC),
  CONSTRAINT `idUsuario`
    FOREIGN KEY (`idRegiao`)
    REFERENCES `mydb`.`regiao` (`idRegiao`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `mydb`.`responsavel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`responsavel` (
  `idUsuario` INT(11) NOT NULL COMMENT 'Id do Usuario do sistema',
  `Nome` TEXT NOT NULL COMMENT 'Nome Do Responsável',
  `idCelular` INT(11) NOT NULL COMMENT 'Id do Celular',
  PRIMARY KEY (`idUsuario`),
  INDEX `idUsuario` (`idUsuario` ASC),
  CONSTRAINT `idUsuario`
    FOREIGN KEY ()
    REFERENCES `mydb`.`usuario` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `CEP`
    FOREIGN KEY ()
    REFERENCES `mydb`.`endereço` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `mydb`.`colegio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`colegio` (
  `idColegio` INT NOT NULL,
  `Nome` VARCHAR(45) NULL,
  PRIMARY KEY (`idColegio`),
  INDEX `idColegio` (`idColegio` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`aluno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`aluno` (
  `idUsuario` INT(11) NOT NULL COMMENT 'id do Usuario do Sistema',
  `Nome` TEXT NOT NULL COMMENT 'Nome do Aluno',
  `AnoEscolar` YEAR NOT NULL COMMENT 'Ano Escolar do Aluno ',
  `idColegio` INT(11) NOT NULL COMMENT 'id do Colegio',
  PRIMARY KEY (`idUsuario`),
  INDEX `idColegio_idx` (`idColegio` ASC),
  CONSTRAINT `idUsuario`
    FOREIGN KEY (`idUsuario`)
    REFERENCES `mydb`.`responsavel` (`idUsuario`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `idColegio`
    FOREIGN KEY (`idColegio`)
    REFERENCES `mydb`.`colegio` (`idColegio`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `mydb`.`materia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`materia` (
  `idMateria` INT(11) NOT NULL COMMENT 'id da Materia',
  `Nome` TEXT NOT NULL COMMENT 'Nome da Materia',
  PRIMARY KEY (`idMateria`),
  INDEX `idMateria` (`idMateria` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `mydb`.`instituicao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`instituicao` (
  `idInstituicao` INT(11) NOT NULL COMMENT 'id da Instituicao de Ensino',
  `Nome` TEXT NOT NULL COMMENT 'Nome da Instituicao de Ensino',
  PRIMARY KEY (`idInstituicao`),
  INDEX `idInstituicao` (`idInstituicao` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `mydb`.`professor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`professor` (
  `idUsuario` INT(11) NOT NULL COMMENT 'id do Usuario do sistema',
  `Nome` TEXT NOT NULL COMMENT 'Nome do Professor',
  `idInstituicao` INT(11) NOT NULL COMMENT 'id da Instituição de Ensino do Professor',
  `Curso` TEXT NOT NULL COMMENT 'id do Curso do professor',
  `idMateria` INT(11) NOT NULL COMMENT 'id da Materia que o professor leciona',
  `HorasAula` INT(11) NOT NULL COMMENT 'Horas Aula acumulada',
  `Celular` TEXT NOT NULL COMMENT 'id Do Celular do Professor',
  PRIMARY KEY (`idUsuario`),
  INDEX `idUsuario` (`idUsuario` ASC),
  INDEX `idMateiria_idx` (`idMateria` ASC),
  INDEX `idInstituicao_idx` (`idInstituicao` ASC),
  CONSTRAINT `idUsuario`
    FOREIGN KEY (`idUsuario`)
    REFERENCES `mydb`.`usuario` (`idUsuario`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `idMateiria`
    FOREIGN KEY (`idMateria`)
    REFERENCES `mydb`.`materia` (`idMateria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idInstituicao`
    FOREIGN KEY (`idInstituicao`)
    REFERENCES `mydb`.`instituicao` (`idInstituicao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `mydb`.`horario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`horario` (
  `idHorario` INT NOT NULL,
  `horaInicio` TIME NULL,
  `horaFinal` TIME NULL,
  PRIMARY KEY (`idHorario`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`aula`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`aula` (
  `idResponsavel` INT(11) NOT NULL COMMENT 'id do Responsavel',
  `idFilho` INT(11) NOT NULL COMMENT 'id do Filho',
  `idMateria` INT(11) NOT NULL COMMENT 'id da Materia',
  `idProfessor` INT(11) NOT NULL COMMENT 'id do Professor',
  `Conteudo` INT(11) NOT NULL COMMENT 'Conteudo',
  `idHorario` INT NOT NULL COMMENT 'Hora de Inicio da Aula',
  PRIMARY KEY (`idResponsavel`, `idFilho`, `idMateria`),
  INDEX `idAluno_idx` (`idFilho` ASC),
  INDEX `idMateria_idx` (`idMateria` ASC),
  INDEX `idProfessor_idx` (`idProfessor` ASC),
  CONSTRAINT `idResponsavel`
    FOREIGN KEY (`idResponsavel`)
    REFERENCES `mydb`.`responsavel` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idFilho`
    FOREIGN KEY (`idFilho`)
    REFERENCES `mydb`.`aluno` (`idUsuario`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `idMateria`
    FOREIGN KEY (`idMateria`)
    REFERENCES `mydb`.`materia` (`idMateria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idProfessor`
    FOREIGN KEY (`idProfessor`)
    REFERENCES `mydb`.`professor` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idHorario`
    FOREIGN KEY ()
    REFERENCES `mydb`.`horario` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `mydb`.`lista_regiao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`lista_regiao` (
  `idUsuario` INT NOT NULL,
  `idRegiao` INT NOT NULL,
  INDEX `idUsuario` (`idUsuario` ASC),
  CONSTRAINT `idRegiao`
    FOREIGN KEY (`idRegiao`)
    REFERENCES `mydb`.`regiao` (`idRegiao`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `idUsuario`
    FOREIGN KEY (`idUsuario`)
    REFERENCES `mydb`.`usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`lista_horário`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`lista_horário` (
  `idUsuario` INT NOT NULL,
  `idHorário` INT NOT NULL,
  INDEX `idUsuario` (),
  INDEX `idHorario_idx` (`idHorário` ASC),
  INDEX `idUsuario_idx` (`idUsuario` ASC),
  CONSTRAINT `idUsuario`
    FOREIGN KEY (`idUsuario`)
    REFERENCES `mydb`.`professor` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idHorario`
    FOREIGN KEY (`idHorário`)
    REFERENCES `mydb`.`horario` (`idHorario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
