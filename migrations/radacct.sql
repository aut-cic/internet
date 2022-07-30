--
-- Table structure for table `radacct`
--

DROP TABLE IF EXISTS `radacct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radacct` (
  `radacctid` bigint(21) NOT NULL AUTO_INCREMENT,
  `acctsessionid` varchar(64) NOT NULL DEFAULT '',
  `acctuniqueid` varchar(32) NOT NULL DEFAULT '',
  `username` varchar(64) NOT NULL DEFAULT '',
  `groupname` varchar(64) NOT NULL DEFAULT '',
  `realm` varchar(64) DEFAULT '',
  `nasipaddress` varchar(15) NOT NULL DEFAULT '',
  `nasportid` varchar(15) DEFAULT NULL,
  `nasporttype` varchar(32) DEFAULT NULL,
  `acctstarttime` datetime DEFAULT NULL,
  `acctupdatetime` datetime DEFAULT NULL,
  `acctstoptime` datetime DEFAULT NULL,
  `acctinterval` int(12) DEFAULT NULL,
  `acctsessiontime` int(12) unsigned DEFAULT NULL,
  `acctauthentic` varchar(32) DEFAULT NULL,
  `connectinfo_start` varchar(50) DEFAULT NULL,
  `connectinfo_stop` varchar(50) DEFAULT NULL,
  `acctinputoctets` bigint(20) DEFAULT NULL,
  `acctoutputoctets` bigint(20) DEFAULT NULL,
  `calledstationid` varchar(50) NOT NULL DEFAULT '',
  `callingstationid` varchar(50) NOT NULL DEFAULT '',
  `acctterminatecause` varchar(32) NOT NULL DEFAULT '',
  `servicetype` varchar(32) DEFAULT NULL,
  `framedprotocol` varchar(32) DEFAULT NULL,
  `framedipaddress` varchar(15) NOT NULL DEFAULT '',
  PRIMARY KEY (`radacctid`),
  UNIQUE KEY `acctuniqueid` (`acctuniqueid`),
  KEY `username` (`username`),
  KEY `framedipaddress` (`framedipaddress`),
  KEY `acctsessionid` (`acctsessionid`),
  KEY `acctsessiontime` (`acctsessiontime`),
  KEY `acctstarttime` (`acctstarttime`),
  KEY `acctinterval` (`acctinterval`),
  KEY `acctstoptime` (`acctstoptime`),
  KEY `nasipaddress` (`nasipaddress`)
) ENGINE=InnoDB AUTO_INCREMENT=20698937 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

INSERT INTO `radacct` VALUES
  (18375113,'80511491','f67e9e7ad4412b4a5512e6ca19a0a894','parham.alvani','','','172.16.0.5','sfp1','Ethernet','2021-08-23 07:57:36','2021-08-23 17:03:38','2021-08-23 17:04:35',181,32819,'','','',127083354,570386619,'hotspot1','6C:3B:6B:F0:0A:17','Admin-Reset','','','172.23.1.192'),
  (18379211,'805125ee','a243797fb6968f23c2e271ea4535a3e5','parham.alvani','','','172.16.0.5','sfp1','Ethernet','2021-08-24 07:56:08','2021-08-24 17:08:07','2021-08-24 17:08:09',180,33120,'','','',49390730,311386231,'hotspot1','6C:3B:6B:F0:0A:17','Admin-Reset','','','172.23.1.192'),
  (14625389,'802103a5','bffb6f625440fe2eee2048a88cc1009f','parham.alvani','','','172.16.0.5','sfp1','Ethernet','2019-10-30 08:02:51','2019-10-30 12:08:51','2019-10-30 12:09:27',179,14796,'','','',4245718,6602549,'hotspot1','6C:3B:6B:E1:4D:40','Lost-Service','','','172.23.145.130'),
  (3176454,'80960f32','f0c9b424bf943a2cb75ef2be519eb40b','parhammlk','','','172.16.0.5','sfp1','Ethernet','2017-10-30 00:05:53','2017-10-30 02:05:55','2017-10-30 02:06:20',301,7227,'','','',46137,168166,'hotspot1','6C:3B:6B:E1:4D:40','Lost-Service','','','172.24.32.115'),
  (3179852,'80961d00','ceb190da16bacc5e92388c977e5d94c7','parham.alvani','','','172.16.0.5','sfp1','Ethernet','2017-10-30 08:39:10','2017-10-30 10:44:12','2017-10-30 10:44:22',300,7512,'','','',624929,14931430,'hotspot1','6C:3B:6B:E1:4D:40','Admin-Reset','','','172.23.145.10'),
  (3181345,'80962220','495f678477ee7cb30c241a15eba6db8b','bbakhshi','','','172.16.0.5','sfp1','Ethernet','2017-10-30 09:20:08','2017-10-30 11:20:08','2017-10-30 11:25:00',300,7493,'','','',774436,2758371,'hotspot1','6C:3B:6B:E1:4D:40','Lost-Service','','','172.23.169.173'),
  (3184695,'80962e8f','fec507c1fde03ae97884abf877d6ac7d','tabrizian','','','172.16.0.5','sfp1','Ethernet','2017-10-30 10:49:53','2017-10-30 12:59:54','2017-10-30 13:02:06',300,7933,'','','',3090808,24879709,'hotspot1','6C:3B:6B:E1:4D:40','Lost-Service','','','172.23.160.201'),
  (3182365,'809624ef','fe3205d2fda188b1a9b37bce5f110897','dastan.elahe','','','172.16.0.5','sfp1','Ethernet','2017-10-30 09:38:05','2017-10-30 11:43:04','2017-10-30 11:47:22',301,7757,'','','',3834366,15667561,'hotspot1','6C:3B:6B:E1:4D:40','Admin-Reset','','','172.23.181.148'),
  (3186418,'809635c4','bf31ec037167d85468eb48a5c3116c61','dastan.elahe','','','172.16.0.5','sfp1','Ethernet','2017-10-30 11:47:24','2017-10-30 11:52:24','2017-10-30 11:56:46',300,562,'','','',124594,657611,'hotspot1','6C:3B:6B:E1:4D:40','Admin-Reset','','','172.23.181.148');
