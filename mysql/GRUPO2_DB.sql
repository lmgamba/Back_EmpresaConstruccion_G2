CREATE DATABASE  IF NOT EXISTS "InnoDB" /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `InnoDB`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: empresadeconstruccion-empresaconstruccion.e.aivencloud.com    Database: InnoDB
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '0f7f4781-07f0-11f1-9134-862ccfb02e7b:1-21,
756f6781-08c0-11f1-9e4d-862ccfb02dc7:1-136,
efca51a5-06ad-11f1-a574-862ccfb06f70:1-61';

--
-- Table structure for table `assignments`
--

DROP TABLE IF EXISTS `assignments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assignments` (
  `id_assignments` int NOT NULL AUTO_INCREMENT,
  `date_start` date NOT NULL,
  `date_finish` date DEFAULT NULL,
  `status` tinyint DEFAULT '1',
  `users_id` int NOT NULL,
  `constructionsSites_id` int NOT NULL,
  PRIMARY KEY (`id_assignments`),
  UNIQUE KEY `id_assignments_UNIQUE` (`id_assignments`),
  KEY `fk_assignments_users_idx` (`users_id`),
  KEY `fk_assignments_constructionsSites1_idx` (`constructionsSites_id`),
  CONSTRAINT `fk_assignments_constructionsSites1` FOREIGN KEY (`constructionsSites_id`) REFERENCES `constructionsSites` (`id_constructions`),
  CONSTRAINT `fk_assignments_users` FOREIGN KEY (`users_id`) REFERENCES `users` (`id_users`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignments`
--

LOCK TABLES `assignments` WRITE;
/*!40000 ALTER TABLE `assignments` DISABLE KEYS */;
INSERT INTO `assignments` VALUES (1,'2025-10-01',NULL,1,13,5),(2,'2025-11-01',NULL,1,13,6),(3,'2025-12-01',NULL,1,13,7),(4,'2025-12-15',NULL,1,13,11),(5,'2026-01-10',NULL,1,40,18),(6,'2025-08-01','2025-12-01',0,14,8),(7,'2026-01-05',NULL,1,14,11),(8,'2026-03-01','2026-08-01',1,14,22),(9,'2025-09-01','2025-12-15',0,23,5),(10,'2026-01-15',NULL,1,24,5),(11,'2025-10-10','2025-12-20',0,25,6),(12,'2026-01-20',NULL,1,27,6),(13,'2025-11-05','2026-01-30',0,28,7),(14,'2026-01-25',NULL,0,29,11),(15,'2026-01-18',NULL,1,30,18),(16,'2025-09-10','2025-11-30',0,32,13),(17,'2025-10-15','2025-12-31',0,33,14),(18,'2026-01-12',NULL,1,34,15),(19,'2025-11-20',NULL,1,36,19),(20,'2026-01-08',NULL,1,37,6),(25,'2026-02-17','2026-02-28',1,23,5);
/*!40000 ALTER TABLE `assignments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `constructionsSites`
--

DROP TABLE IF EXISTS `constructionsSites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `constructionsSites` (
  `id_constructions` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `description` text,
  `address` varchar(255) NOT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_constructions`),
  UNIQUE KEY `id_constructions_UNIQUE` (`id_constructions`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `constructionsSites`
--

LOCK TABLES `constructionsSites` WRITE;
/*!40000 ALTER TABLE `constructionsSites` DISABLE KEYS */;
INSERT INTO `constructionsSites` VALUES (5,'Residencial Nuevo Norte','Promoción residencial 80 viviendas','Calle Agustin de Foxa 24, Madrid',40.47220000,-3.68270000,'IN_PROGRESS'),(6,'Torre Levante Valencia Nuevo','Edificio oficinas 15 plantas','Av Cortes Valencianas, Valencia',39.49630000,-0.40360000,'IN_PROGRESS'),(7,'Hotel Mirador del Puerto','Hotel 4 estrellas','Muelle Uno, Malaga',36.71960000,-4.41500000,'PLANNING'),(8,'Centro Logistico Zaragoza PLAZA','Nave 10.000m2','Plataforma PLAZA, Zaragoza',41.63300000,-0.97400000,'FINISHED'),(9,'Residencial Sevilla Este','120 viviendas','Av de las Ciencias, Sevilla',37.40450000,-5.92300000,'IN_PROGRESS'),(10,'Campus Empresarial Las Tablas','Complejo oficinas','Calle Maria Tubau, Madrid',40.50350000,-3.66970000,'PLANNING'),(11,'Hospital Privado Barcelona Mar','Centro hospitalario','Carrer de la Marina, Barcelona',41.40360000,2.17440000,'IN_PROGRESS'),(13,'Edificio Corporativo Bilbao','Oficinas corporativas','Gran Via 45, Bilbao',43.26300000,-2.93500000,'IN_PROGRESS'),(14,'Puerto Deportivo Alicante','Ampliacion portuaria','Muelle 12, Alicante',38.34430000,-0.48100000,'FINISHED'),(15,'Residencial Costa del Sol','Urbanizacion chalets','Estepona, Malaga',36.42500000,-5.14500000,'IN_PROGRESS'),(16,'Centro Comercial Atlantico','Centro comercial','Vecindario, Gran Canaria',27.84200000,-15.44600000,'IN_PROGRESS'),(17,'Parque Empresarial Valencia Sur','Oficinas y coworking','Paterna, Valencia',39.50200000,-0.44000000,'PLANNING'),(18,'Residencial Montecarmelo','Viviendas lujo','Montecarmelo, Madrid',40.50520000,-3.69500000,'IN_PROGRESS'),(19,'Ampliacion Aeropuerto Malaga','Nueva terminal','Aeropuerto Malaga',36.67490000,-4.49910000,'IN_PROGRESS'),(20,'Reforma Estadio Valladolid','Reforma graderio','Valladolid Centro',41.65230000,-4.72450000,'IN_PROGRESS'),(22,'Edificio Tecnologico 22@','Oficinas tech','Distrito 22@ Barcelona',41.40330000,2.20400000,'IN_PROGRESS'),(23,'Residencial Playa Editado','Apartamentos turisticos','Motril, Granada',36.72800000,-3.51700000,'IN_PROGRESS'),(24,'Centro Salud Amara','Centro sanitario','Amara, San Sebastian',43.31280000,-1.97400000,'IN_PROGRESS'),(26,'Hospital Virgen del Rocio','\nNueva planta de urgencias\n','Avenida Manuel Siurot, Sevilla',37.36200000,-5.98030000,'active');
/*!40000 ALTER TABLE `constructionsSites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `id_logs` int NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  `type` varchar(50) NOT NULL,
  `date_register` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `users_id` int NOT NULL,
  `constructionsSites_id` int NOT NULL,
  PRIMARY KEY (`id_logs`),
  UNIQUE KEY `id_logs_UNIQUE` (`id_logs`),
  KEY `fk_logs_users1_idx` (`users_id`),
  KEY `fk_logs_constructionsSites1_idx` (`constructionsSites_id`),
  CONSTRAINT `fk_logs_constructionsSites1` FOREIGN KEY (`constructionsSites_id`) REFERENCES `constructionsSites` (`id_constructions`),
  CONSTRAINT `fk_logs_users1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id_users`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (1,'Avance semanal de la estructura','UPDATE','2025-11-10 09:30:00',30,5),(2,'Revision de seguridad en la obra','INFO','2025-12-15 11:00:00',30,6),(3,'Actualizacion del progreso de cimentacion','UPDATE','2026-01-20 10:15:00',32,7),(4,'Incidencia menor con suministros','ALERT','2026-01-28 16:40:00',32,11),(5,'Control de calidad de materiales','INFO','2026-02-12 12:20:00',28,18),(6,'Inspeccion de maquinaria en obra','INFO','2025-09-12 08:45:00',14,8),(7,'Retraso por condiciones climaticas','ALERT','2025-11-22 14:10:00',14,8),(8,'Inicio de tareas de cimentacion','UPDATE','2026-01-06 09:05:00',14,9),(9,'Incidencia menor en materiales','ALERT','2026-01-18 13:25:00',14,9),(10,'Progreso semanal registrado','UPDATE','2026-02-05 17:40:00',14,9),(11,'Revision de seguridad diaria','INFO','2026-02-14 10:10:00',14,9),(12,'Montaje de estructura principal','UPDATE','2025-10-18 11:00:00',23,13),(13,'Finalizacion de fase inicial','UPDATE','2025-11-25 15:30:00',24,14),(14,'Inicio de nueva fase de construccion','INFO','2026-01-12 09:50:00',24,15),(15,'Entrega de materiales completada','INFO','2025-08-12 08:45:00',25,16),(16,'Avance en ampliacion de terminal','UPDATE','2026-01-22 16:10:00',25,19),(17,'Control de calidad semanal','INFO','2025-10-07 12:00:00',27,20),(18,'Instalacion de sistemas electricos','UPDATE','2025-12-15 14:20:00',28,22),(19,'Cierre de movimiento de tierras','UPDATE','2025-09-18 18:00:00',29,23),(20,'Planificacion de siguientes tareas','INFO','2026-01-22 10:30:00',29,24),(23,'Nuevo avance','UPDATE','2026-02-19 20:01:46',14,8),(24,'Avance nuevo','UPDATE','2026-02-19 20:02:16',14,22),(25,'ALERT Retraso en la entrega ','ALERT','2026-02-19 20:35:13',14,11);
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id_users` int NOT NULL AUTO_INCREMENT,
  `name` varchar(65) NOT NULL,
  `surname` varchar(65) NOT NULL,
  `mail` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','user') NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_users`),
  UNIQUE KEY `id_users_UNIQUE` (`id_users`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (13,'Admin Jefe','Empresa','jefe.empresa.construccion@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$z5nTWqvVOicEAMA4B+D8Hw$fMdPsJ+KqwdaZYJ4UqmV4U8T989jZQLs1KBIHq3o0iM','admin','2021-02-19 13:31:34',0),(14,'Operario Supervisor','Empresa','operario.empresa.construccion@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0),(23,'Antonio','Gomez','antonio.gomez@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0),(24,'Manuel','Lopez','manuel.lopez@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0),(25,'Francisco','Diaz','francisco.diaz@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',1),(26,'Jose','Perez','jose.perez@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0),(27,'Juan','Martin','juan.martin@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0),(28,'Pedro','Serrano','pedro.serrano@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',1),(29,'Sergio','Navarro','sergio.navarro@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0),(30,'Raul','Ortega','raul.ortega@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0),(31,'Diego','Morales','diego.morales@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0),(32,'Ruben','Vargas','ruben.vargas@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',1),(33,'Fernando','Molina','fernando.molina@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',1),(34,'Oscar','Iglesias','oscar.iglesias@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0),(35,'Hector','Suarez','hector.suarez@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0),(36,'Adrian','Cano','adrian.cano@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0),(37,'Ivan','Gil','ivan.gil@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0),(38,'Mario','Santos','mario.santos@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',1),(39,'Victor','Leon','victor.leon@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0),(40,'Alejandro','Reyes','alejandro.reyes@demoapp.com','$argon2id$v=19$m=65536,t=3,p=4$bu3du7eW8t57T0lpjZFyzg$gPUKUbI0fQGVx6UAuzDNDjhrSZPjbghSgvV+TSuWEwE','user','2021-02-19 13:31:34',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-20 17:39:02
