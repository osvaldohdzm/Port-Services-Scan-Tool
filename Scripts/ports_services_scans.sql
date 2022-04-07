-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.6.3-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for ports_services_scans
DROP DATABASE IF EXISTS `ports_services_scans`;
CREATE DATABASE IF NOT EXISTS `ports_services_scans` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `ports_services_scans`;

-- Dumping structure for table ports_services_scans.hosts
DROP TABLE IF EXISTS `hosts`;
CREATE TABLE IF NOT EXISTS `hosts` (
  `host_id` int(11) NOT NULL AUTO_INCREMENT,
  `scan_id` int(11) NOT NULL,
  `ip` varchar(50) DEFAULT NULL,
  `mac_address` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `hostname` varchar(50) DEFAULT NULL,
  `operative_system` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`host_id`) USING BTREE,
  KEY `FK_hosts_scans` (`scan_id`) USING BTREE,
  CONSTRAINT `FK_hosts_scans` FOREIGN KEY (`scan_id`) REFERENCES `scans` (`scan_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4352 DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table ports_services_scans.ports
DROP TABLE IF EXISTS `ports`;
CREATE TABLE IF NOT EXISTS `ports` (
  `scan_id` int(11) NOT NULL,
  `port_id` int(11) NOT NULL AUTO_INCREMENT,
  `host_ip` varchar(50) NOT NULL DEFAULT '',
  `number` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `service_name` varchar(100) DEFAULT NULL,
  `product` varchar(100) DEFAULT NULL,
  `version` varchar(50) DEFAULT NULL,
  `operative_system` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`port_id`),
  KEY `FK_ports_scans` (`scan_id`),
  CONSTRAINT `FK_ports_scans` FOREIGN KEY (`scan_id`) REFERENCES `scans` (`scan_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=31459 DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table ports_services_scans.scans
DROP TABLE IF EXISTS `scans`;
CREATE TABLE IF NOT EXISTS `scans` (
  `scan_id` int(12) NOT NULL AUTO_INCREMENT,
  `start` datetime DEFAULT NULL,
  `end` datetime DEFAULT NULL,
  `version` varchar(50) DEFAULT NULL,
  `arguments` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`scan_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9147 DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
