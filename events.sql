-- phpMyAdmin SQL Dump
-- version 4.8.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 30, 2019 at 03:51 AM
-- Server version: 10.1.34-MariaDB
-- PHP Version: 7.2.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `events`
--

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `eventID` int(11) NOT NULL,
  `Title` varchar(500) NOT NULL,
  `startdate` date NOT NULL,
  `enddate` date NOT NULL,
  `starttime` time NOT NULL,
  `endtime` time NOT NULL,
  `Ticketprice` int(10) NOT NULL,
  `poster` varchar(1000) NOT NULL,
  `place` varchar(1000) NOT NULL,
  `Description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `event`
--

INSERT INTO `event` (`eventID`, `Title`, `startdate`, `enddate`, `starttime`, `endtime`, `Ticketprice`, `poster`, `place`, `Description`) VALUES
(1, 'فریلند', '2019-01-04', '2019-01-12', '12:59:00', '00:00:00', 60000, '/uploads/freeland-blog-768x329.jpg', 'سالن همایش منطقه آزاد بندر انزلی', 'این رویداد به شما کمک می‌کند کسب و کار خود را با اطمینان شروع کنید. اگر شما مهارت یا تخصصی دارید، این رویداد به شما کمک می‌کند تا یاد بگیرید از کجا شروع کنید، چطور مشتریان زیادی پیدا کنید، چطور خود را مطرح کنید، و چطور بدون آنکه جایی استخدام شوید درآمد بالایی داشته باشید. برای شروع کار به عنوان یک فریلنسر، به سرمایه زیادی نیاز ندارید. مهمترین سرمایه شما، وقت و تخصص شماست. نیاز نیست فردی را استخدام کنید چون همه کارها را خودتان انجام خواهید داد، و هر وقت نیاز بود با فریلنسرهای دیگر پروژه‌ای کار می‌کنید.'),
(2, 'تست', '2019-01-10', '2019-12-31', '00:58:00', '13:59:00', 50000, '/uploads/58531d7356ce728d0ed6059f_Gallery-Image-1.png', 'رشت', 'تست تست تست'),
(3, 'تست2', '2019-01-24', '2019-01-04', '13:59:00', '13:59:00', 50000, '/uploads/8b6d073aafc111a71421e4929282d312.jpg', 'انزلی', 'تسسسسسسسسسسست'),
(4, 'تست2', '2019-01-18', '2019-01-19', '12:59:00', '13:59:00', 50000, '/uploads/grand-conference.png', 'انزلی', 'تسسست تسست ');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `ticketID` int(11) NOT NULL,
  `eventID` int(11) NOT NULL,
  `username` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticketID`, `eventID`, `username`) VALUES
(1, 1, 'yalda'),
(2, 2, 'yalda'),
(3, 2, 'yalda'),
(4, 2, 'yalda'),
(5, 4, 'fatem'),
(6, 4, 'fatem'),
(7, 2, 'fatem'),
(8, 1, 'fatem');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `ID` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `lastname` varchar(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `password` varchar(20) NOT NULL,
  `image` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`ID`, `name`, `lastname`, `username`, `email`, `password`, `image`) VALUES
(1, 'عارفه', 'حمیدی', 'ar_efe', 'arefehamidi.guilan@gmail.com', '2585', '/uploads/photo_--_--.jpg'),
(2, 'یلدا', 'پروری مقدم', 'Yalda', 'ghuyesepid.guailan@gmail.com', '3352', '/uploads/SAM_5987.jpg'),
(3, 'راحله', 'دیانتی', 'Rahele', 'baran.guailan@gmail.com', '94012', ''),
(4, 'فاطمه', 'قربانعلی زاده محسنی', 'fatem', 'f.ghaf', '1376210', '/uploads/photo_2019-01-30_06-17-52.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`eventID`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ticketID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `eventID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `ticket`
--
ALTER TABLE `ticket`
  MODIFY `ticketID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
