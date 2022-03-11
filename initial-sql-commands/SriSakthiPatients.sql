DROP DATABASE IF EXISTS SrisakthiPatients;
CREATE DATABASE SrisakthiPatients;
USE SrisakthiPatients;

CREATE TABLE `patients` (
  `Sno` int NOT NULL AUTO_INCREMENT,
  `patientID` varchar(10) NOT NULL,
  `name` varchar(225) NOT NULL,
  `dob` date NOT NULL,
  `gender` char(1) NOT NULL,
  `phone` varchar(17) NOT NULL,
  `address` varchar(255) NOT NULL,
  PRIMARY KEY (`patientID`),
  UNIQUE KEY `Sno` (`Sno`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO patients (patientID, name, dob, gender, phone, address)
VALUES ("ABC1234", "MUTHU", '2000-03-28', "M", "+919000000000", "Cecilia Chapman\n711-2880 Nulla St.\nMankato Mississippi 96522");




CREATE TABLE `Appointments` (
  `Sno` int NOT NULL AUTO_INCREMENT,
  `date` DATE,
  `time` TIME,
  `patientID` varchar(10) NOT NULL REFERENCES patients(patientID),
  `treatmentID` VARCHAR(10),
  PRIMARY KEY (`treatmentID`),
  UNIQUE KEY `Sno` (`Sno`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO Appointments (date, time, patientID, treatmentID)
VALUES ('2022-07-12', '10:00', "ABC1234", "A24DS67");




CREATE TABLE `treatments` (
    `Sno` int NOT NULL AUTO_INCREMENT,
    `treatmentID` VARCHAR(10) NOT NULL REFERENCES Appointments(treatmentID),
    `date` DATE,
    `time` TIME,
    `treatment` TEXT,
    `status` TEXT,
    `fee` REAL(16,2),
    `paid` BOOLEAN,
    UNIQUE KEY `Sno` (`Sno`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO treatments (patientID, treatmentID, date, time, treatment, status, fee, paid)
VALUES ("ABC1234", "A24DS67", '2022-07-12', '10:07', "Root Canal", "Completed", 7000.00, True);
