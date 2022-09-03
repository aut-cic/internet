--
-- Table structure for table `radusergroup`
--
DROP TABLE
  IF EXISTS `radusergroup`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = utf8 */;

CREATE TABLE
  `radusergroup` (
    `username` varchar(64) NOT NULL DEFAULT '',
    `groupname` varchar(64) NOT NULL DEFAULT '',
    `priority` int (11) NOT NULL DEFAULT '1',
    `id` int (11) NOT NULL AUTO_INCREMENT,
    `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `username` (`username` (32))
  ) ENGINE = InnoDB AUTO_INCREMENT = 17906 DEFAULT CHARSET = latin1;

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radusergroup`
--
/*!40000 ALTER TABLE `radusergroup` DISABLE KEYS */;

INSERT INTO
  `radusergroup`
VALUES
  (
    'parham.alvani',
    'Faculty',
    1,
    86,
    '2022-06-29 00:09:04'
  ),
  ('bbakhshi', 'Faculty', 1, 5, NULL),
  (
    'mohammadhfatemi',
    'BSc',
    1,
    8304,
    '2022-05-09 00:10:29'
  );

/*!40000 ALTER TABLE `radusergroup` ENABLE KEYS */;
