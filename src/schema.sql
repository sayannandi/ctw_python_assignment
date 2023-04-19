CREATE DATABASE IF NOT EXISTS ctw;

USE ctw;

CREATE TABLE IF NOT EXISTS `financial_data` (
  `symbol` VARCHAR(10) NOT NULL,
  `date` DATE NOT NULL,
  `open_price` FLOAT(10,2) unsigned NOT NULL,
  `close_price` FLOAT(10,2) unsigned NOT NULL,
  `volume` BIGINT unsigned NOT NULL,
  PRIMARY KEY (`symbol`, `date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;