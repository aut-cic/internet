--
-- Table structure for table `radusergroup`
--

DROP TABLE IF EXISTS `radusergroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radusergroup` (
  `username` varchar(64) NOT NULL DEFAULT '',
  `groupname` varchar(64) NOT NULL DEFAULT '',
  `priority` int(11) NOT NULL DEFAULT '1',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `username` (`username`(32))
) ENGINE=InnoDB AUTO_INCREMENT=17906 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radusergroup`
--

LOCK TABLES `radusergroup` WRITE;
/*!40000 ALTER TABLE `radusergroup` DISABLE KEYS */;
INSERT INTO `radusergroup` VALUES ('parham.alvani','Faculty',1,86,'2022-06-29 00:09:04'),('bbakhshi','Faculty',1,5,NULL),('mohammadhfatemi','BSc',1,8304,'2022-05-09 00:10:29');
/*!40000 ALTER TABLE `radusergroup` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


--
-- Table structure for table `raddaily`
--

DROP TABLE IF EXISTS `raddaily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `raddaily` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `usageorig` bigint(20) NOT NULL,
  `usagediscount` bigint(20) NOT NULL,
  `createddate` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`,`createddate`)
) ENGINE=InnoDB AUTO_INCREMENT=1606824 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raddaily`
--

LOCK TABLES `raddaily` WRITE;
/*!40000 ALTER TABLE `raddaily` DISABLE KEYS */;

INSERT INTO `raddaily` VALUES (399,'parham.alvani',51465,51465,'2020-11-02'),(16355,'parham.alvani',88199357,88168952,'2020-11-11'),(1897,'parham.alvani',68497715,68408799,'2020-11-03'),(3012,'parham.alvani',3664185241,1772631461,'2020-11-04'),(4679,'bbakhshi',38549530,16896149,'2020-11-05'),(4569,'parham.alvani',225226325,89699337,'2020-11-05'),(6255,'parham.alvani',16870257,5517320,'2020-11-06')
