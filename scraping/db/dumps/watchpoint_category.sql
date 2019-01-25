CREATE DATABASE  IF NOT EXISTS `watchpoint` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
USE `watchpoint`;
-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: watchpoint
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `category` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `View_count` int(11) DEFAULT '0',
  `Parent_Id` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `Parent_Id_idx` (`Parent_Id`),
  CONSTRAINT `Parent_Id` FOREIGN KEY (`Parent_Id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36035 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Computer',936,NULL),(2,'Telefonie & accessoires',867,NULL),(3,'Tablets & smart devices',326,NULL),(4,'Audio & hifi',230,NULL),(5,'Televisie & home cinema',174,NULL),(6,'Huis, tuin & beauty',179,NULL),(7,'Componenten en randapparatuur',375,NULL),(8,'Printers',136,NULL),(9,'Camera\'s en accessoires',758,NULL),(27739,'Alles-in-één-desktops',983,1),(27823,'Cadeaus',241,1),(27824,'Desktops',654,1),(27831,'Barebones',150,1),(28037,'PC-games',1000,27823),(28040,'Xbox One-games',687,27823),(28182,'F1 games & toebehoren',1073,27823),(28464,'Monitoren',904,7),(28815,'Muizen',100,7),(28886,'Toetsenborden',191,7),(28958,'Toetsenbord + Muis-sets',653,28958),(29028,'Muismatten',294,28815),(29085,'Tekentablets',712,3),(29212,'Rugzakken',277,29213),(29213,'Tassen & Hoezen',450,1),(29282,'Laptopsleeves',220,29213),(29481,'Tassen voor harde schijf',949,29213),(29522,'Cd/dvd-opbergsystemen',488,29213),(29901,'Cartridges',793,8),(30110,'Toners',102,8),(30230,'Dataopslag & geheugen',531,1),(30284,'Interne harde schijven',100,30230),(30341,'Externe SSD\'s',550,30230),(30375,'Interne SSD\'s',508,30230),(30425,'Usb-sticks',887,30230),(30476,'Micro SD kaarten',512,30230),(30478,'Cardreaders',1101,30230),(30479,'SD kaarten',369,30230),(30488,'Geheugenkaarthouder',943,30230),(30532,'Netwerk & Internet',9,1),(30563,'Mifi routers',816,30532),(30632,'Wifi versterkers',452,30532),(30704,'Switches',1013,30532),(30804,'Powerline-adapters',111,30532),(30842,'Beveiligingscamera\'s',1115,30532),(30849,'Wifi adapters',441,30532),(30851,'Usb-hubs',62,30532),(30855,'Bluetooth-adapters',188,30532),(30865,'Access points',755,30532),(30936,'Telefoonhoesjes',809,2),(31006,'Screenprotectors',583,2),(31078,'Powerbanks',486,2),(31141,'Houders',684,2),(31144,'Telefoonbuttons',761,31141),(31171,'Fietshouders',554,31141),(31172,'Dockingstations',490,31141),(31212,'Draadloze opladers',785,31215),(31215,'Opladers',56,2),(31221,'Autoladers',326,31215),(31246,'Wearable accessoires',262,3),(31283,'Kabels',332,1),(31287,'Consolekabels',876,31283),(31346,'Bluetooth headsets',982,31346),(31416,'GPS trackers',1083,2),(31555,'Carkits',71,2),(31627,'Reparatie & reserveondedelen',704,2),(31700,'Selfiesticks',909,2),(31769,'Hoesjes',35,29213),(32088,'Activity trackers',1047,32095),(32095,'Smartwatches',331,3),(32149,'Sporthorloges',914,3),(32309,'E-readers',1178,3),(32373,'Navigatie',749,3),(32445,'Motornavigatie',210,32373),(32473,'Fietsnavigatie',4,32373),(32489,'Vrachtwagennavigatie',589,32373),(32500,'Wandelnavigatie',535,32373),(32517,'Campernavigatie',908,32373),(32523,'Speakers',536,4),(32587,'Wifi speakers',1000,32523),(32649,'Soundbars',567,32523),(33044,'Soundplates',571,32523),(33047,'Koptelefoons',1153,4),(33048,'On-ear koptelefoons',455,33047),(33056,'Gaming headsets',17,33047),(33116,'In-ear oordopjes',1119,4),(33184,'Koptelefoon cases',744,33047),(33231,'Gaming headset stands',363,33047),(33236,'Koptelefoon houders',785,33047),(33279,'Televisies',437,5),(33613,'Home Cinema-sets',1029,5),(33683,'Microsets',233,4),(33751,'Beamers',481,5),(34076,'Spiegelreflexcamera\'s',506,9),(34110,'Systeemcamera\'s',1085,9),(34179,'Vlog camera\'s',311,9),(34194,'Compactcamera\'s',700,9),(34202,'Onderwatercamera\'s',166,9),(34218,'Bridge camera\'s',1131,9),(34235,'Instant camera\'s',360,9),(34286,'Wegwerpcamera\'s',805,9),(34338,'Action camera\'s',545,9),(34387,'Compressoren',311,6),(34460,'Multitools voor grote klussen',1000,6),(34531,'Multitools voor kleine klussen',1074,6),(34603,'Heteluchtpistolen',806,6),(34675,'Tackers',810,6),(34678,'Nieten',431,6),(34747,'Lijmpistolen',925,6),(34819,'Freesmachines',934,6),(34923,'Universeelsnijders',695,6),(34953,'Knabbelscharen',674,6),(34972,'Polijstmachines',86,6),(35044,'Bouwstofzuigers',810,6),(35090,'Kruimelzuigers',189,6),(35181,'Aszuigers',917,6),(35196,'Betonmolens',420,6),(35215,'Betonmixers',546,6),(35239,'Bouwlampen',274,6),(35311,'Laptops',931,1);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-01-25  1:37:08
