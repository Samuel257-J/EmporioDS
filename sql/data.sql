-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: lanchonete_db
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Dumping data for table `funcionarios`
--

LOCK TABLES `funcionarios` WRITE;
/*!40000 ALTER TABLE `funcionarios` DISABLE KEYS */;
INSERT INTO `funcionarios` VALUES (1,'Samuel','70522216404','Gerente','samuel177j','samuel177j'),(2,'João Vitor de Souza Silva','70812034422','Atendente','joaovitor321','joaovitor321'),(3,'Davi Bittencourt Nogueira','01941095267','Cozinheiro','davibit123','davibit123'),(4,'Luiz Felipe Gomes da Costa','70042710480','Garçom','luizfelipe321','luizfelipe321');
/*!40000 ALTER TABLE `funcionarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
INSERT INTO `produtos` VALUES (1,'Pastel de Carne','Pastel',12.00,500,1),(2,'Pastel de Coalho','Pastel',12.00,500,1),(3,'Pastel de Cheddar','Pastel',12.00,500,1),(4,'Pastel de Frango','Pastel',12.00,500,1),(5,'Pastel de Presunto','Pastel',12.00,500,1),(6,'Pastel de Calabresa','Pastel',12.00,500,1),(7,'Pastel de Catupiry','Pastel',12.00,500,1),(8,'Pastel de Queijo','Pastel',12.00,500,1),(9,'Pastel de Frango c/ Catupiry','Pastel',13.00,400,1),(10,'Pastel de Frango c/ Cheddar','Pastel',13.00,400,1),(11,'Pastel de Frango c/ Milho','Pastel',13.00,400,1),(12,'Pastel de Carne c/ Bacon','Pastel',13.00,400,1),(13,'Pastel de Atum','Pastel',13.00,400,1),(14,'Pastel de Mussarela','Pastel',13.00,400,1),(15,'Pastel de Mussarela, Tomate e Manjericão','Pastel',14.00,300,1),(16,'Pastel de Frango, Cebola e Azeitonas','Pastel',14.00,300,1),(17,'Pastel de Camarão, Queijo, Cebola e Azeitonas','Pastel',14.00,300,1),(18,'X-Frango','Hambúrguer',16.00,300,1),(19,'X-Calabresa','Hambúrguer',17.00,300,1),(20,'X-Bacon','Hambúrguer',18.00,300,1),(21,'X-Tudo','Hambúrguer',22.00,300,1),(22,'X-Picanha','Hambúrguer',25.00,250,1),(23,'Coxinha Tradicional','Coxinha',8.00,500,1),(24,'Coxinha de Queijo','Coxinha',8.00,500,1),(25,'Coxinha de Frango c/ Catupiry','Coxinha',9.00,400,1),(26,'Coxinha de Carne Seca','Coxinha',10.00,350,1),(27,'Coxinha de Camarão','Coxinha',12.00,250,1),(28,'Batata Frita Simples','Porção',15.00,450,1),(29,'Batata Frita c/ Bacon','Porção',20.00,350,1),(30,'Anéis de Cebola','Porção',16.00,300,1),(31,'Nuggets de Frango','Porção',18.00,300,1),(32,'Bolinho de Queijo','Porção',16.00,400,1),(33,'Mandioca Frita','Porção',14.00,300,1),(34,'Lasanha de Carne','Massa',40.00,250,1),(35,'Lasanha de Frango','Massa',40.00,250,1),(36,'Lasanha de Presunto','Massa',40.00,250,1),(37,'Lasanha Quatro Queijos','Massa',50.00,250,1),(38,'Pudim de Leite','Sobremesa',12.00,150,1),(39,'Brigadeiro Gourmet','Sobremesa',10.00,100,1),(40,'Torta de Chocolate','Sobremesa',15.00,100,1),(41,'Mousse de Maracujá','Sobremesa',12.00,150,1),(42,'Beijinho de Côco','Sobremesa',8.00,200,1),(43,'Sorvete (2 bolas)','Sobremesa',10.00,150,1),(44,'Coca-Cola Lata (300ml)','Bebida',7.00,500,1),(45,'Guaraná Lata (300ml)','Bebida',7.00,500,1),(46,'Fanta-Uva Lata (300ml)','Bebida',7.00,500,1),(47,'Fanta-Laranja Lata (300ml)','Bebida',7.00,500,1),(48,'Pepsi Lata (300ml)','Bebida',7.00,500,1),(49,'Sprite Lata (300ml)','Bebida',7.00,500,1),(50,'Suco de Laranja - Copo (300ml)','Bebida',8.00,200,1),(51,'Suco de Uva - Copo (300ml)','Bebida',8.00,200,1),(52,'Suco de Manga - Copo (300ml)','Bebida',8.00,200,1),(53,'Suco de Maracujá - Copo (300ml)','Bebida',8.00,200,1),(54,'Suco de Limão - Copo (300ml)','Bebida',8.00,200,1),(55,'Suco de Caju - Copo (300ml)','Bebida',8.00,200,1),(56,'Suco de Cajá - Copo (300ml)','Bebida',8.00,200,1),(57,'Suco de Goiaba - Copo (300ml)','Bebida',8.00,200,1),(58,'Suco de Abacaxi - Copo (300ml)','Bebida',8.00,200,1),(59,'Suco de Graviola - Copo (300ml)','Bebida',8.00,200,1),(60,'Jarra de Goiaba (600ml)','Bebida',16.00,100,1),(61,'Jarra de Cajá (600ml)','Bebida',16.00,100,1),(62,'Jarra de Caju (600ml)','Bebida',16.00,100,1),(63,'Jarra de Limão (600ml)','Bebida',16.00,100,1),(64,'Jarra de Maracujá (600ml)','Bebida',16.00,100,1),(65,'Jarra de Abacaxi (600ml)','Bebida',16.00,100,1),(66,'Jarra de Manga (600ml)','Bebida',16.00,100,1),(67,'Jarra de Laranja (600ml)','Bebida',16.00,100,1),(68,'Jarra de Uva (600ml)','Bebida',16.00,100,1),(69,'Jarra de Graviola (600ml)','Bebida',16.00,100,1),(70,'Água Mineral (500ml)','Bebida',3.50,500,1),(71,'Cerveja - Lata (350ml)','Bebida',6.00,150,1),(72,'Cerveja Long Neck (600ml)','Bebida',12.00,100,1),(73,'Heineken - Cerveja Premium','Bebida',10.00,150,1),(74,'Stella Artois - Cerveja Premium','Bebida',10.00,150,1),(75,'Cerveja Artesanal','Bebida',15.00,150,1),(76,'Malzbier','Bebida',8.00,100,1);
/*!40000 ALTER TABLE `produtos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-08 21:19:14
