-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Apr 30, 2025 at 04:12 PM
-- Server version: 8.0.34
-- PHP Version: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jamparke_IA637_Project`
--

-- --------------------------------------------------------

--
-- Table structure for table `debt`
--

CREATE TABLE `debt` (
  `debt_id` int NOT NULL,
  `debt_amount` decimal(15,2) NOT NULL,
  `debt_rate` decimal(5,2) NOT NULL,
  `debt_date` date NOT NULL,
  `debt_terms` int NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `debt`
--

INSERT INTO `debt` (`debt_id`, `debt_amount`, `debt_rate`, `debt_date`, `debt_terms`, `user_id`) VALUES
(13, 5000.00, 5.00, '2025-04-03', 60, 6),
(14, 25000.00, 4.50, '2025-02-28', 120, 7),
(15, 60000.00, 7.00, '2023-07-30', 60, 7),
(16, 80000.00, 9.50, '2021-03-30', 180, 7),
(17, 150000.00, 3.00, '2019-06-06', 360, 6);

-- --------------------------------------------------------

--
-- Table structure for table `investments`
--

CREATE TABLE `investments` (
  `inv_id` int NOT NULL,
  `inv_date` date NOT NULL,
  `uid` int NOT NULL,
  `stock_shares` decimal(10,2) DEFAULT NULL,
  `stock_purchase_price` decimal(10,2) DEFAULT NULL,
  `stock_tic` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `investments`
--

INSERT INTO `investments` (`inv_id`, `inv_date`, `uid`, `stock_shares`, `stock_purchase_price`, `stock_tic`) VALUES
(10, '2024-12-05', 6, 25.00, 28.60, 'SCHG'),
(11, '2024-12-05', 6, 7.00, 132.98, 'VYM'),
(12, '2024-12-05', 6, 1.00, 251.89, 'SMH'),
(13, '2024-12-05', 6, 30.00, 28.96, 'SCHD'),
(14, '2024-12-05', 6, 2.00, 302.40, 'VTI'),
(15, '2024-12-05', 6, 2.00, 558.46, 'VOO'),
(16, '2024-12-05', 6, 7.00, 215.16, 'QQQM'),
(17, '2025-04-01', 6, 5.00, 200.00, 'AAPL'),
(21, '2010-06-16', 7, 500.00, 104.04, 'VOO'),
(22, '2010-11-30', 6, 5.00, 100.00, 'VOO');

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `tid` int NOT NULL,
  `trans_category` varchar(100) NOT NULL,
  `trans_amount` decimal(15,2) NOT NULL,
  `trans_date` date NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`tid`, `trans_category`, `trans_amount`, `trans_date`, `user_id`) VALUES
(4, 'Income', 1000.00, '2025-04-22', 6),
(5, 'Gas', 40.00, '2025-04-08', 6),
(6, 'Housing', 1000.00, '2025-04-17', 6),
(7, 'Entertainment', 15.00, '2025-04-17', 6),
(8, 'Loan Payment', 250.00, '2025-04-02', 6),
(9, 'Entertainment', 30.00, '2025-04-05', 6),
(10, 'Income', 1000.00, '2025-04-08', 6),
(11, 'Food', 200.00, '2025-04-13', 6),
(12, 'Income', 2000.00, '2025-03-05', 6),
(13, 'Housing', 1000.00, '2025-03-13', 6),
(14, 'Income', 2000.00, '2025-02-28', 7),
(15, 'Income', 2000.00, '2025-03-31', 7),
(16, 'Income', 2000.00, '2025-04-30', 7),
(17, 'Housing', 1200.00, '2025-04-01', 7),
(18, 'Housing', 1200.00, '2025-03-01', 7),
(19, 'Housing', 1200.00, '2025-02-01', 7),
(20, 'Food', 300.00, '2025-04-16', 7),
(21, 'Food', 300.00, '2025-03-14', 7),
(22, 'Food', 300.00, '2025-02-12', 7),
(23, 'Gas', 50.00, '2025-04-18', 7),
(24, 'Gas', 80.00, '2025-03-19', 7),
(25, 'Gas', 60.00, '2025-02-14', 7),
(26, 'Entertainment', 250.00, '2025-04-11', 7),
(27, 'Loan Payment', 400.00, '2025-03-29', 7),
(28, 'Loan Payment', 400.00, '2025-02-28', 7),
(29, 'Loan Payment', 400.00, '2025-04-29', 7),
(30, 'Entertainment', 400.00, '2025-04-03', 6);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `uid` int NOT NULL,
  `fname` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` varchar(20) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`uid`, `fname`, `email`, `role`, `password`) VALUES
(3, 'Jacob', 'a@a.com', 'admin', '5ae6de412f4a8d6eb59926302d4afe01'),
(6, 'Tyler', 'b@b.com', 'customer', '3c7a71e1b859a94a35be988b0e7a633c'),
(7, 'Jacob', 'c@c.com', 'customer', 'c2e378e5060a5f590daf9ba5238203be');

-- --------------------------------------------------------

--
-- Table structure for table `value`
--

CREATE TABLE `value` (
  `debt_id` int NOT NULL,
  `inv_id` int NOT NULL,
  `date` date NOT NULL,
  `current_value` decimal(15,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `debt`
--
ALTER TABLE `debt`
  ADD PRIMARY KEY (`debt_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `investments`
--
ALTER TABLE `investments`
  ADD PRIMARY KEY (`inv_id`),
  ADD KEY `user_id` (`uid`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`tid`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`uid`);

--
-- Indexes for table `value`
--
ALTER TABLE `value`
  ADD PRIMARY KEY (`debt_id`,`inv_id`,`date`),
  ADD KEY `inv_id` (`inv_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `debt`
--
ALTER TABLE `debt`
  MODIFY `debt_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `investments`
--
ALTER TABLE `investments`
  MODIFY `inv_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `tid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `uid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `debt`
--
ALTER TABLE `debt`
  ADD CONSTRAINT `debt_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`uid`);

--
-- Constraints for table `investments`
--
ALTER TABLE `investments`
  ADD CONSTRAINT `investments_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`);

--
-- Constraints for table `transaction`
--
ALTER TABLE `transaction`
  ADD CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`uid`);

--
-- Constraints for table `value`
--
ALTER TABLE `value`
  ADD CONSTRAINT `value_ibfk_1` FOREIGN KEY (`debt_id`) REFERENCES `debt` (`debt_id`),
  ADD CONSTRAINT `value_ibfk_2` FOREIGN KEY (`inv_id`) REFERENCES `investments` (`inv_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
