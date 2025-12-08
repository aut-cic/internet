--
-- Table structure for table `raddaily`
--
DROP TABLE IF EXISTS `raddaily`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = utf8 */;

CREATE TABLE
  `raddaily` (
    `id` int (11) NOT NULL AUTO_INCREMENT,
    `username` varchar(64) NOT NULL,
    `usageorig` bigint (20) NOT NULL,
    `usagediscount` bigint (20) NOT NULL,
    `createddate` date NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`, `createddate`)
  ) ENGINE = InnoDB AUTO_INCREMENT = 1606824 DEFAULT CHARSET = latin1;

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raddaily`
--
LOCK TABLES `raddaily` WRITE;

/*!40000 ALTER TABLE `raddaily` DISABLE KEYS */;

INSERT INTO
  `raddaily`
VALUES
  (399, 'parham.alvani', 51465, 51465, CURDATE()),
  (
    16355,
    'parham.alvani',
    88199357,
    88168952,
    DATE_SUB(CURDATE(), INTERVAL 1 DAY)
  ),
  (
    1897,
    'parham.alvani',
    68497715,
    68408799,
    DATE_SUB(CURDATE(), INTERVAL 2 DAY)
  ),
  (
    3012,
    'parham.alvani',
    3664185241,
    1772631461,
    DATE_SUB(CURDATE(), INTERVAL 5 DAY)
  ),
  (
    4679,
    'bbakhshi',
    38549530,
    16896149,
    '2020-11-05'
  ),
  (
    4569,
    'parham.alvani',
    225226325,
    89699337,
    '2020-11-05'
  ),
  (
    6255,
    'parham.alvani',
    16870257,
    5517320,
    '2020-11-06'
  )
