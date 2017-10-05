-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema NBA-games
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `NBA-games` ;

-- -----------------------------------------------------
-- Schema NBA-games
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `NBA-games` DEFAULT CHARACTER SET utf8 ;
USE `NBA-games` ;

-- -----------------------------------------------------
-- Table `NBA-games`.`team`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `NBA-games`.`team` ;

CREATE TABLE IF NOT EXISTS `NBA-games`.`team` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(5) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `division` VARCHAR(45) NOT NULL,
  `conference` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `code_UNIQUE` (`code` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `NBA-games`.`game`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `NBA-games`.`game` ;

CREATE TABLE IF NOT EXISTS `NBA-games`.`game` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(20) NOT NULL,
  `season` VARCHAR(12) NULL,
  `date` DATE NULL,
  `time` VARCHAR(45) NULL,
  `type` VARCHAR(20) NULL,
  `dce` ENUM('D', 'C', 'E') NULL,
  `winner` ENUM('H', 'A') NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `code_UNIQUE` (`code` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `NBA-games`.`team_stat`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `NBA-games`.`team_stat` ;

CREATE TABLE IF NOT EXISTS `NBA-games`.`team_stat` (
  `game_id` INT NOT NULL,
  `ha` ENUM('H', 'A') NOT NULL,
  `team_id` INT NULL,
  `result` ENUM('W', 'L') NULL,
  `STLP` DOUBLE NULL,
  `FT` TINYINT(3) UNSIGNED NULL,
  `b2PA` TINYINT(3) UNSIGNED NULL,
  `FG` TINYINT(3) UNSIGNED NULL,
  `DRB` TINYINT(3) UNSIGNED NULL,
  `ORBP` DOUBLE NULL,
  `AST` TINYINT(3) UNSIGNED NULL,
  `b3PAr` DOUBLE NULL,
  `PF` TINYINT(3) UNSIGNED NULL,
  `FGA` TINYINT(3) UNSIGNED NULL,
  `DRBr` DOUBLE NULL,
  `b2P` TINYINT(3) UNSIGNED NULL,
  `ORBr` DOUBLE NULL,
  `TOVP` DOUBLE NULL,
  `ASTP` DOUBLE NULL,
  `FTAr` DOUBLE NULL,
  `FIC` DOUBLE NULL,
  `eFGP` DOUBLE NULL,
  `FGP` DOUBLE NULL,
  `b2PAr` DOUBLE NULL,
  `PlusMinus` SMALLINT(3) NULL,
  `USGP` DOUBLE NULL,
  `DRtg` DOUBLE NULL,
  `b2PP` DOUBLE NULL,
  `DRBP` DOUBLE NULL,
  `ORtg` DOUBLE NULL,
  `TRBP` DOUBLE NULL,
  `ORB` TINYINT(3) UNSIGNED NULL,
  `b3P` TINYINT(3) UNSIGNED NULL,
  `TOV` TINYINT(3) UNSIGNED NULL,
  `STLonTOV` DOUBLE NULL,
  `TSA` DOUBLE NULL,
  `ASTonTOV` DOUBLE NULL,
  `b3PA` TINYINT(3) UNSIGNED NULL,
  `BLKP` DOUBLE NULL,
  `FTP` DOUBLE NULL,
  `PTS` TINYINT(3) UNSIGNED NULL,
  `HOB` DOUBLE NULL,
  `STL` TINYINT(3) UNSIGNED NULL,
  `TRB` TINYINT(3) UNSIGNED NULL,
  `FTA` TINYINT(3) UNSIGNED NULL,
  `BLK` TINYINT(3) UNSIGNED NULL,
  `FTr` DOUBLE NULL,
  `TSP` DOUBLE NULL,
  `FTonFGA` DOUBLE NULL,
  `b3PP` DOUBLE NULL,
  PRIMARY KEY (`game_id`, `ha`),
  INDEX `fk_scores_2_idx` (`team_id` ASC),
  CONSTRAINT `fk_scores_1`
    FOREIGN KEY (`game_id`)
    REFERENCES `NBA-games`.`game` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_scores_2`
    FOREIGN KEY (`team_id`)
    REFERENCES `NBA-games`.`team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `NBA-games`.`score`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `NBA-games`.`score` ;

CREATE TABLE IF NOT EXISTS `NBA-games`.`score` (
  `game_id` INT NOT NULL,
  `period` VARCHAR(10) NOT NULL,
  `ha` ENUM('H', 'A') NOT NULL,
  `score` TINYINT(3) UNSIGNED NULL,
  PRIMARY KEY (`game_id`, `period`, `ha`),
  CONSTRAINT `fk_score_1`
    FOREIGN KEY (`game_id`)
    REFERENCES `NBA-games`.`game` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SET SQL_MODE = '';
GRANT USAGE ON *.* TO ml;
 DROP USER ml;
SET SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
CREATE USER 'ml' IDENTIFIED BY 'ml99__NBA+-*';

GRANT ALL ON `NBA-games`.* TO 'ml';

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
