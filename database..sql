-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `acme`
--
CREATE DATABASE IF NOT EXISTS `cnc_database` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `cnc_database`;

-- --------------------------------------------------------

--
-- Struttura della tabella `cnc_data`
--

CREATE TABLE `cnc_data` (
  `id` int(11) NOT NULL,
  `cnc_id` varchar(45) DEFAULT NULL,
  `part_program` varchar(45) DEFAULT NULL,
  `timestamp` int(11) DEFAULT NULL,
  `json_data` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `cnc_data`
--
ALTER TABLE `cnc_data`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `cnc_data`
--
ALTER TABLE `cnc_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
