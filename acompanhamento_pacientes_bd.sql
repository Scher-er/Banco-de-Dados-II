CREATE DATABASE  IF NOT EXISTS `acompanhamento_pacientes_bd` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `acompanhamento_pacientes_bd`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: acompanhamento_pacientes_bd
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

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

--
-- Table structure for table `alertas`
--

DROP TABLE IF EXISTS `alertas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alertas` (
  `idAlertas` int(11) NOT NULL AUTO_INCREMENT,
  `geracao` datetime NOT NULL,
  `nivel_critico` varchar(45) NOT NULL,
  `status` char(1) NOT NULL,
  `Pacientes_idPacientes` int(11) NOT NULL,
  PRIMARY KEY (`idAlertas`),
  KEY `fk_Alertas_Pacientes1_idx` (`Pacientes_idPacientes`),
  CONSTRAINT `fk_Alertas_Pacientes1` FOREIGN KEY (`Pacientes_idPacientes`) REFERENCES `pacientes` (`idPacientes`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alertas`
--

LOCK TABLES `alertas` WRITE;
/*!40000 ALTER TABLE `alertas` DISABLE KEYS */;
/*!40000 ALTER TABLE `alertas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bairros`
--

DROP TABLE IF EXISTS `bairros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bairros` (
  `idBairros` int(11) NOT NULL AUTO_INCREMENT,
  `Nome_do_Bairro` varchar(200) NOT NULL,
  `Cidades_idCidades` int(11) NOT NULL,
  PRIMARY KEY (`idBairros`),
  KEY `fk_Bairros_Cidades1_idx` (`Cidades_idCidades`),
  CONSTRAINT `fk_Bairros_Cidades1` FOREIGN KEY (`Cidades_idCidades`) REFERENCES `cidades` (`idCidades`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bairros`
--

LOCK TABLES `bairros` WRITE;
/*!40000 ALTER TABLE `bairros` DISABLE KEYS */;
/*!40000 ALTER TABLE `bairros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cidades`
--

DROP TABLE IF EXISTS `cidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cidades` (
  `idCidades` int(11) NOT NULL AUTO_INCREMENT,
  `Nome_da_Cidade` varchar(200) NOT NULL,
  `Estados_idEstados` int(11) NOT NULL,
  PRIMARY KEY (`idCidades`),
  KEY `fk_Cidades_Estados1_idx` (`Estados_idEstados`),
  CONSTRAINT `fk_Cidades_Estados1` FOREIGN KEY (`Estados_idEstados`) REFERENCES `estados` (`idEstados`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cidades`
--

LOCK TABLES `cidades` WRITE;
/*!40000 ALTER TABLE `cidades` DISABLE KEYS */;
/*!40000 ALTER TABLE `cidades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `convenios`
--

DROP TABLE IF EXISTS `convenios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `convenios` (
  `idconvenios` int(11) NOT NULL AUTO_INCREMENT,
  `nome_convenio` varchar(200) NOT NULL,
  `cnpj` varchar(20) NOT NULL,
  `registro_ans` varchar(20) NOT NULL,
  `Pacientes_idPacientes` int(11) NOT NULL,
  PRIMARY KEY (`idconvenios`),
  UNIQUE KEY `cnpj_UNIQUE` (`cnpj`),
  KEY `fk_convenios_Pacientes1_idx` (`Pacientes_idPacientes`),
  CONSTRAINT `fk_convenios_Pacientes1` FOREIGN KEY (`Pacientes_idPacientes`) REFERENCES `pacientes` (`idPacientes`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `convenios`
--

LOCK TABLES `convenios` WRITE;
/*!40000 ALTER TABLE `convenios` DISABLE KEYS */;
/*!40000 ALTER TABLE `convenios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estados`
--

DROP TABLE IF EXISTS `estados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estados` (
  `idEstados` int(11) NOT NULL AUTO_INCREMENT,
  `Nome_do_Estado` varchar(45) NOT NULL,
  `Sigla` varchar(45) NOT NULL,
  `Países_idPaises` int(11) NOT NULL,
  PRIMARY KEY (`idEstados`),
  KEY `fk_Estados_Países_idx` (`Países_idPaises`),
  CONSTRAINT `fk_Estados_Países` FOREIGN KEY (`Países_idPaises`) REFERENCES `paises` (`idPaises`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados`
--

LOCK TABLES `estados` WRITE;
/*!40000 ALTER TABLE `estados` DISABLE KEYS */;
/*!40000 ALTER TABLE `estados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historico_medico`
--

DROP TABLE IF EXISTS `historico_medico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historico_medico` (
  `idhistorico_medico` int(11) NOT NULL AUTO_INCREMENT,
  `data_evento` date NOT NULL,
  `tipo_evento` varchar(50) NOT NULL,
  `descrição_detalhada` varchar(500) NOT NULL,
  `Pacientes_idPacientes` int(11) NOT NULL,
  PRIMARY KEY (`idhistorico_medico`),
  KEY `fk_historico_medico_Pacientes1_idx` (`Pacientes_idPacientes`),
  CONSTRAINT `fk_historico_medico_Pacientes1` FOREIGN KEY (`Pacientes_idPacientes`) REFERENCES `pacientes` (`idPacientes`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_medico`
--

LOCK TABLES `historico_medico` WRITE;
/*!40000 ALTER TABLE `historico_medico` DISABLE KEYS */;
/*!40000 ALTER TABLE `historico_medico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `limites_alerta`
--

DROP TABLE IF EXISTS `limites_alerta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `limites_alerta` (
  `idLimites_alerta` int(11) NOT NULL AUTO_INCREMENT,
  `Valor_minimo` decimal(10,2) NOT NULL,
  `Valor_Maximo` decimal(10,2) NOT NULL,
  `Pacientes_idPacientes` int(11) NOT NULL,
  PRIMARY KEY (`idLimites_alerta`),
  KEY `fk_Limites_alerta_Pacientes1_idx` (`Pacientes_idPacientes`),
  CONSTRAINT `fk_Limites_alerta_Pacientes1` FOREIGN KEY (`Pacientes_idPacientes`) REFERENCES `pacientes` (`idPacientes`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `limites_alerta`
--

LOCK TABLES `limites_alerta` WRITE;
/*!40000 ALTER TABLE `limites_alerta` DISABLE KEYS */;
/*!40000 ALTER TABLE `limites_alerta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicao`
--

DROP TABLE IF EXISTS `medicao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicao` (
  `idMedicao` int(11) NOT NULL AUTO_INCREMENT,
  `medicao` datetime NOT NULL,
  `tipo_medicao` varchar(50) NOT NULL,
  `valor` decimal(10,2) NOT NULL,
  `unidade_medida` varchar(20) NOT NULL,
  `Pacientes_idPacientes` int(11) NOT NULL,
  PRIMARY KEY (`idMedicao`),
  KEY `fk_Medicao_Pacientes1_idx` (`Pacientes_idPacientes`),
  CONSTRAINT `fk_Medicao_Pacientes1` FOREIGN KEY (`Pacientes_idPacientes`) REFERENCES `pacientes` (`idPacientes`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicao`
--

LOCK TABLES `medicao` WRITE;
/*!40000 ALTER TABLE `medicao` DISABLE KEYS */;
/*!40000 ALTER TABLE `medicao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pacientes`
--

DROP TABLE IF EXISTS `pacientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pacientes` (
  `idPacientes` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(200) NOT NULL,
  `idade` int(11) NOT NULL,
  `Data_de_Nascimento` date NOT NULL,
  `CPF` char(14) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Telefone` varchar(20) NOT NULL,
  `Numero_da_casa` int(11) NOT NULL,
  `Genero` char(1) DEFAULT NULL,
  `Contato_Emergencial_Nome` varchar(200) NOT NULL,
  `Contato_Emergencial_Telefone` varchar(45) NOT NULL,
  `Status` char(1) NOT NULL,
  `Data_Cadastro` date NOT NULL,
  `Bairros_idBairros` int(11) NOT NULL,
  PRIMARY KEY (`idPacientes`),
  UNIQUE KEY `Email_UNIQUE` (`Email`),
  UNIQUE KEY `CPF_UNIQUE` (`CPF`),
  KEY `fk_Pacientes_Bairros1_idx` (`Bairros_idBairros`),
  CONSTRAINT `fk_Pacientes_Bairros1` FOREIGN KEY (`Bairros_idBairros`) REFERENCES `bairros` (`idBairros`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacientes`
--

LOCK TABLES `pacientes` WRITE;
/*!40000 ALTER TABLE `pacientes` DISABLE KEYS */;
/*!40000 ALTER TABLE `pacientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pacientes_has_profissionais`
--

DROP TABLE IF EXISTS `pacientes_has_profissionais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pacientes_has_profissionais` (
  `Pacientes_idPacientes` int(11) NOT NULL,
  `Profissionais_idProfissionais` int(11) NOT NULL,
  PRIMARY KEY (`Pacientes_idPacientes`,`Profissionais_idProfissionais`),
  KEY `fk_Pacientes_has_Profissionais_Profissionais1_idx` (`Profissionais_idProfissionais`),
  KEY `fk_Pacientes_has_Profissionais_Pacientes1_idx` (`Pacientes_idPacientes`),
  CONSTRAINT `fk_Pacientes_has_Profissionais_Pacientes1` FOREIGN KEY (`Pacientes_idPacientes`) REFERENCES `pacientes` (`idPacientes`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pacientes_has_Profissionais_Profissionais1` FOREIGN KEY (`Profissionais_idProfissionais`) REFERENCES `profissionais` (`idProfissionais`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacientes_has_profissionais`
--

LOCK TABLES `pacientes_has_profissionais` WRITE;
/*!40000 ALTER TABLE `pacientes_has_profissionais` DISABLE KEYS */;
/*!40000 ALTER TABLE `pacientes_has_profissionais` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paises`
--

DROP TABLE IF EXISTS `paises`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paises` (
  `idPaises` int(11) NOT NULL AUTO_INCREMENT,
  `Nome_do_País` varchar(200) NOT NULL,
  `Sigla` varchar(10) NOT NULL,
  PRIMARY KEY (`idPaises`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paises`
--

LOCK TABLES `paises` WRITE;
/*!40000 ALTER TABLE `paises` DISABLE KEYS */;
/*!40000 ALTER TABLE `paises` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profissionais`
--

DROP TABLE IF EXISTS `profissionais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profissionais` (
  `idProfissionais` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(200) NOT NULL,
  `idade` int(11) NOT NULL,
  `Data_de_Nascimento` date NOT NULL,
  `CPF` char(14) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Telefone` varchar(20) NOT NULL,
  `Numero_da_casa` int(11) NOT NULL,
  `Genero` char(1) DEFAULT NULL,
  `Status` char(1) NOT NULL,
  PRIMARY KEY (`idProfissionais`),
  UNIQUE KEY `Email_UNIQUE` (`Email`),
  UNIQUE KEY `CPF_UNIQUE` (`CPF`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profissionais`
--

LOCK TABLES `profissionais` WRITE;
/*!40000 ALTER TABLE `profissionais` DISABLE KEYS */;
/*!40000 ALTER TABLE `profissionais` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'acompanhamento_pacientes_bd'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-10 21:51:04
