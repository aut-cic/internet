--
-- Table structure for table `radpackages`
--
DROP TABLE IF EXISTS `radpackages`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = utf8 */;

CREATE TABLE `radpackages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `groupname` varchar(64) NOT NULL,
  `daily_volume` int(12) NOT NULL,
  `weekly_volume` int(12) NOT NULL,
  `monthly_volume` int(12) NOT NULL,
  `priority` int(12) NOT NULL,
  `session` int(11) NOT NULL DEFAULT '3',
  PRIMARY KEY (`id`),
  UNIQUE KEY `groupname` (`groupname`),
  UNIQUE KEY `groupname_2` (`groupname`)
) ENGINE = InnoDB AUTO_INCREMENT = 45 DEFAULT CHARSET = latin1;

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radpackages`
--
LOCK TABLES `radpackages` WRITE;

/*!40000 ALTER TABLE `radpackages` DISABLE KEYS */;

INSERT INTO
  `radpackages`
VALUES
  (2, 'Faculty', 5, 20, 60, 4, 3),
  (3, 'PhD', 4, 16, 48, 8, 3),
  (5, 'BSc', 3, 12, 30, 10, 3),
  (6, 'Staff', 2, 8, 24, 12, 3),
  (7, 'group1', 3, 10, 20, -1, 10),
  (8, 'Other', 1, 3, 8, -2, 3),
  (9, 'ICT', 4, 16, 40, 1, 3),
  (11, 'Jahad', 2, 8, 20, 11, 3),
  (12, 'Foundation', 2, 3, 20, 13, 3),
  (14, 'VideoConf', 4, 16, 40, 5, 3),
  (15, 'PostDoc', 5, 20, 60, 7, 3),
  (16, 'Lecturer', 4, 16, 48, 6, 3),
  (17, 'Lab', 4, 16, 48, 24, 3),
  (19, 'FacultyRetd', 4, 16, 48, 3, 3),
  (20, 'PhDAlumni', 1, 3, 6, 21, 3),
  (21, 'MSc', 3, 12, 36, 9, 3),
  (22, 'BScAlumni', 1, 3, 6, 23, 3),
  (23, 'LibStaff', 4, 16, 48, 14, 3),
  (24, 'LibUser', 3, 12, 36, 25, 3),
  (25, 'StdSciAssn', 3, 12, 36, 15, 3),
  (26, 'StdProAssn', 3, 12, 36, 26, 3),
  (27, 'NetAdmin', 4, 16, 40, 2, 50),
  (28, 'AfflStaff', 2, 8, 24, 18, 3),
  (29, 'AfflSrv', 1, 3, 6, 17, 3),
  (30, 'AfflCo', 2, 8, 20, 16, 3),
  (31, 'SecDorm', 1, 3, 6, 20, 3),
  (32, 'SecUniv', 1, 4, 12, 19, 3),
  (35, 'MScAlumni', 1, 3, 6, 22, 3),
  (36, 'Guest', 5, 20, 60, 28, 3),
  (37, 'Unlimited', 100, 200, 300, 0, 3),
  (43, 'JustEmail', 0, 0, 0, 27, 0),
  (44, 'LibraryGroup', 3, 12, 36, 29, 3);

/*!40000 ALTER TABLE `radpackages` ENABLE KEYS */;

UNLOCK TABLES;
