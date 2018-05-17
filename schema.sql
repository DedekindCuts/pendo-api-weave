-- MySQL dump 10.13  Distrib 5.7.21, for osx10.13 (x86_64)
--
-- Host: localhost    Database: Pendo
-- ------------------------------------------------------
-- Server version	5.7.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `Pendo`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Pendo` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `Pendo`;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts` (
  `accountId` varchar(255) NOT NULL DEFAULT '',
  `shortaccountId` varchar(255) NOT NULL DEFAULT '',
  `accountName` varchar(255) NOT NULL DEFAULT '',
  `salesforceId` varchar(255) NOT NULL DEFAULT '',
  `lastupdated` varchar(255) DEFAULT NULL,
  `firstvisit` varchar(255) DEFAULT NULL,
  `lastvisit` varchar(255) DEFAULT NULL,
  UNIQUE KEY `accountId_2` (`accountId`,`accountName`,`salesforceId`),
  KEY `shortaccountId` (`shortaccountId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`nick.larsen`@`localhost`*/ /*!50003 TRIGGER `shortaccountId (accounts)` BEFORE INSERT ON `accounts` FOR EACH ROW SET NEW.shortaccountId = REPLACE(NEW.accountId, '-', '') */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Temporary table structure for view `active_accounts`
--

DROP TABLE IF EXISTS `active_accounts`;
/*!50001 DROP VIEW IF EXISTS `active_accounts`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `active_accounts` AS SELECT 
 1 AS `accountId`,
 1 AS `shortaccountId`,
 1 AS `accountName`,
 1 AS `firstvisit`,
 1 AS `Account Status`,
 1 AS `Onboarding Status`,
 1 AS `Onboarder`,
 1 AS `Billing Start Date`,
 1 AS `Completed Port Date`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `clean_accounts`
--

DROP TABLE IF EXISTS `clean_accounts`;
/*!50001 DROP VIEW IF EXISTS `clean_accounts`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `clean_accounts` AS SELECT 
 1 AS `accountId`,
 1 AS `shortaccountId`,
 1 AS `accountName`,
 1 AS `firstvisit`,
 1 AS `Account Status`,
 1 AS `Onboarding Status`,
 1 AS `Onboarder`,
 1 AS `Billing Start Date`,
 1 AS `Completed Port Date`,
 1 AS `Date Canceled`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `dates`
--

DROP TABLE IF EXISTS `dates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dates` (
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `feature_events`
--

DROP TABLE IF EXISTS `feature_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feature_events` (
  `accountId` varchar(255) NOT NULL,
  `visitorId` varchar(255) NOT NULL,
  `day` date NOT NULL,
  `featureId` varchar(255) NOT NULL,
  `numEvents` int(11) NOT NULL,
  `numMinutes` int(11) NOT NULL,
  `server` varchar(255) DEFAULT NULL,
  `remoteIp` varchar(255) DEFAULT NULL,
  `parameters` varchar(255) DEFAULT NULL,
  `userAgent` varchar(1000) DEFAULT NULL,
  `appId` varchar(255) DEFAULT NULL,
  `accountIdCopy` varchar(255) NOT NULL DEFAULT '',
  `shortaccountId` varchar(255) DEFAULT NULL,
  KEY `accountId` (`accountId`),
  KEY `features` (`featureId`),
  KEY `day` (`day`),
  KEY `shortaccountId` (`shortaccountId`),
  KEY `features, visitors` (`visitorId`),
  CONSTRAINT `features` FOREIGN KEY (`featureId`) REFERENCES `features` (`id`),
  CONSTRAINT `features, accounts` FOREIGN KEY (`accountId`) REFERENCES `accounts` (`accountId`),
  CONSTRAINT `features, shortaccounts` FOREIGN KEY (`shortaccountId`) REFERENCES `accounts` (`shortaccountId`),
  CONSTRAINT `features, visitors` FOREIGN KEY (`visitorId`) REFERENCES `visitors` (`visitorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`nick.larsen`@`localhost`*/ /*!50003 TRIGGER `shortaccountId` BEFORE INSERT ON `feature_events` FOR EACH ROW SET NEW.shortaccountId = REPLACE(NEW.accountId, '-', '') */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `features`
--

DROP TABLE IF EXISTS `features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `features` (
  `id` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `guide_events`
--

DROP TABLE IF EXISTS `guide_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `guide_events` (
  `accountId` varchar(255) NOT NULL,
  `shortaccountId` varchar(255) DEFAULT NULL,
  `visitorId` varchar(255) NOT NULL,
  `browserTime` datetime NOT NULL,
  `guideId` varchar(255) NOT NULL,
  `guideStepId` varchar(255) NOT NULL,
  `country` varchar(255) DEFAULT NULL,
  `elementPath` varchar(255) DEFAULT NULL,
  `eventId` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `loadTime` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `remoteIp` varchar(255) DEFAULT NULL,
  `serverName` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `userAgent` varchar(255) DEFAULT NULL,
  `accountIds` varchar(255) NOT NULL,
  KEY `guides` (`guideId`),
  KEY `browserTime` (`browserTime`),
  KEY `shortaccountId` (`shortaccountId`),
  KEY `guides, accounts` (`accountId`),
  KEY `guides, visitors` (`visitorId`),
  CONSTRAINT `guides` FOREIGN KEY (`guideId`) REFERENCES `guides` (`id`),
  CONSTRAINT `guides, accounts` FOREIGN KEY (`accountId`) REFERENCES `accounts` (`accountId`),
  CONSTRAINT `guides, shortaccounts` FOREIGN KEY (`shortaccountId`) REFERENCES `accounts` (`shortaccountId`),
  CONSTRAINT `guides, visitors` FOREIGN KEY (`visitorId`) REFERENCES `visitors` (`visitorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`nick.larsen`@`localhost`*/ /*!50003 TRIGGER `shortaccountId (guide_events)` BEFORE INSERT ON `guide_events` FOR EACH ROW SET NEW.shortaccountId = REPLACE(NEW.accountId, '-', '') */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `guides`
--

DROP TABLE IF EXISTS `guides`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `guides` (
  `id` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kpi_base`
--

DROP TABLE IF EXISTS `kpi_base`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kpi_base` (
  `Account name` varchar(255) NOT NULL DEFAULT '',
  `Location ID` varchar(255) NOT NULL DEFAULT '',
  `week_id` int(11) NOT NULL DEFAULT '0',
  `First day of week` date DEFAULT NULL,
  `Page events` decimal(32,0) DEFAULT NULL,
  `Feature events` decimal(32,0) DEFAULT NULL,
  `Days active` bigint(21) DEFAULT NULL,
  `Days using feature SMS Send` bigint(21) DEFAULT NULL,
  `Days using page Messages` bigint(21) DEFAULT NULL,
  PRIMARY KEY (`Location ID`,`week_id`),
  KEY `week_id` (`week_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `page_events`
--

DROP TABLE IF EXISTS `page_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `page_events` (
  `accountId` varchar(255) NOT NULL,
  `visitorId` varchar(255) NOT NULL,
  `day` date NOT NULL,
  `pageId` varchar(255) NOT NULL,
  `numEvents` int(11) NOT NULL,
  `numMinutes` int(11) NOT NULL,
  `server` varchar(255) DEFAULT NULL,
  `remoteIp` varchar(255) DEFAULT NULL,
  `parameters` varchar(255) DEFAULT NULL,
  `userAgent` varchar(1000) DEFAULT NULL,
  `appId` varchar(255) DEFAULT NULL,
  `shortaccountId` varchar(255) DEFAULT NULL,
  KEY `accountId` (`accountId`),
  KEY `visitorId` (`visitorId`),
  KEY `day` (`day`),
  KEY `pages` (`pageId`),
  KEY `shortaccountId` (`shortaccountId`),
  CONSTRAINT `pages` FOREIGN KEY (`pageId`) REFERENCES `pages` (`id`),
  CONSTRAINT `pages, accounts` FOREIGN KEY (`accountId`) REFERENCES `accounts` (`accountId`),
  CONSTRAINT `pages, shortaccounts` FOREIGN KEY (`shortaccountId`) REFERENCES `accounts` (`shortaccountId`),
  CONSTRAINT `pages, visitors` FOREIGN KEY (`visitorId`) REFERENCES `visitors` (`visitorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`nick.larsen`@`localhost`*/ /*!50003 TRIGGER `shortaccountId (page_events)` BEFORE INSERT ON `page_events` FOR EACH ROW SET NEW.shortaccountId = REPLACE(NEW.accountId, '-', '') */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `pages`
--

DROP TABLE IF EXISTS `pages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pages` (
  `id` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `poll_events`
--

DROP TABLE IF EXISTS `poll_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `poll_events` (
  `accountId` varchar(255) NOT NULL,
  `shortaccountId` varchar(255) DEFAULT NULL,
  `visitorId` varchar(255) NOT NULL,
  `browserTime` datetime NOT NULL,
  `guideId` varchar(255) DEFAULT NULL,
  `guideStepId` varchar(255) DEFAULT NULL,
  `pollId` varchar(255) NOT NULL,
  `pollResponse` text,
  `country` varchar(255) DEFAULT NULL,
  `elementPath` varchar(255) DEFAULT NULL,
  `eventId` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `loadTime` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `remoteIp` varchar(255) DEFAULT NULL,
  `serverName` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `userAgent` varchar(255) DEFAULT NULL,
  `accountIds` varchar(255) NOT NULL,
  KEY `polls` (`guideId`),
  KEY `browserTime` (`browserTime`),
  KEY `shortaccountId` (`shortaccountId`),
  KEY `polls, accounts` (`accountId`),
  KEY `polls, visitors` (`visitorId`),
  CONSTRAINT `polls` FOREIGN KEY (`guideId`) REFERENCES `guides` (`id`),
  CONSTRAINT `polls, accounts` FOREIGN KEY (`accountId`) REFERENCES `accounts` (`accountId`),
  CONSTRAINT `polls, shortaccounts` FOREIGN KEY (`shortaccountId`) REFERENCES `accounts` (`shortaccountId`),
  CONSTRAINT `polls, visitors` FOREIGN KEY (`visitorId`) REFERENCES `visitors` (`visitorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`nick.larsen`@`localhost`*/ /*!50003 TRIGGER `shortaccountId (poll_events)` BEFORE INSERT ON `poll_events` FOR EACH ROW SET NEW.shortaccountId = REPLACE(NEW.accountId, '-', '') */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `test_5`
--

DROP TABLE IF EXISTS `test_5`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `test_5` (
  `accountId` varchar(255) NOT NULL DEFAULT '',
  `shortaccountId` varchar(255) NOT NULL DEFAULT '',
  `accountName` varchar(255) NOT NULL DEFAULT '',
  `firstvisit` varchar(255) DEFAULT NULL,
  `Billing Start Date` varchar(255) DEFAULT NULL,
  `Date Canceled` varchar(255) DEFAULT NULL,
  `Reason for Cancel` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `visitors`
--

DROP TABLE IF EXISTS `visitors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `visitors` (
  `visitorId` varchar(255) NOT NULL DEFAULT '',
  `accountId` varchar(255) DEFAULT '',
  `shortaccountId` varchar(255) DEFAULT NULL,
  `lastupdated` datetime DEFAULT NULL,
  `firstvisit` datetime DEFAULT NULL,
  `lastvisit` datetime DEFAULT NULL,
  `lastbrowsername` varchar(255) DEFAULT NULL,
  `lastbrowserversion` varchar(255) DEFAULT NULL,
  `lastoperatingsystem` varchar(255) DEFAULT NULL,
  `lastservername` varchar(255) DEFAULT NULL,
  `lastuseragent` varchar(1000) DEFAULT NULL,
  UNIQUE KEY `visitorId_2` (`visitorId`,`accountId`),
  KEY `visitorId` (`visitorId`),
  KEY `shortaccountId` (`shortaccountId`),
  KEY `visitors, accounts` (`accountId`),
  CONSTRAINT `visitors, accounts` FOREIGN KEY (`accountId`) REFERENCES `accounts` (`accountId`),
  CONSTRAINT `visitors, shortaccounts` FOREIGN KEY (`shortaccountId`) REFERENCES `accounts` (`shortaccountId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`nick.larsen`@`localhost`*/ /*!50003 TRIGGER `shortaccountId (visitors)` BEFORE INSERT ON `visitors` FOR EACH ROW SET NEW.shortaccountId = REPLACE(NEW.accountId, '-', '') */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `weeks`
--

DROP TABLE IF EXISTS `weeks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weeks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `year` int(4) DEFAULT NULL,
  `week` int(2) DEFAULT NULL,
  `first` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `year` (`year`,`week`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'Pendo'
--

--
-- Current Database: `Pendo`
--

USE `Pendo`;

--
-- Final view structure for view `active_accounts`
--

/*!50001 DROP VIEW IF EXISTS `active_accounts`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`nick.larsen`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `active_accounts` AS select `a`.`accountId` AS `accountId`,`a`.`shortaccountId` AS `shortaccountId`,`a`.`accountName` AS `accountName`,`a`.`firstvisit` AS `firstvisit`,`s`.`Account Status` AS `Account Status`,`s`.`Onboarding Status` AS `Onboarding Status`,`s`.`Onboarder` AS `Onboarder`,`s`.`Billing Start Date` AS `Billing Start Date`,`s`.`Completed Port Date` AS `Completed Port Date` from (`pendo`.`accounts` `a` join `salesforce`.`accounts` `s` on((`a`.`accountId` = `s`.`Location ID`))) where ((`s`.`Account Status` in ('Active','Onboarding','Onboarding (Active)')) and (`a`.`shortaccountId` <> '')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `clean_accounts`
--

/*!50001 DROP VIEW IF EXISTS `clean_accounts`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`nick.larsen`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `clean_accounts` AS select `a`.`accountId` AS `accountId`,`a`.`shortaccountId` AS `shortaccountId`,`a`.`accountName` AS `accountName`,`a`.`firstvisit` AS `firstvisit`,`s`.`Account Status` AS `Account Status`,`s`.`Onboarding Status` AS `Onboarding Status`,`s`.`Onboarder` AS `Onboarder`,`s`.`Billing Start Date` AS `Billing Start Date`,`s`.`Completed Port Date` AS `Completed Port Date`,`s`.`Date Canceled` AS `Date Canceled` from (`pendo`.`accounts` `a` join `salesforce`.`accounts` `s` on((`a`.`accountId` = `s`.`Location ID`))) where ((`s`.`Account Status` in ('Active','Onboarding','Onboarding (Active)','Canceled')) and (`a`.`shortaccountId` <> '')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-17 14:11:06
