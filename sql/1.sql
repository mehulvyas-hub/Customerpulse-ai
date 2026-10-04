SELECT CURRENT_ROLE(), CURRENT_USER();

CREATE WAREHOUSE IF NOT EXISTS CUSTOMERPULSE_WH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE;

    SHOW WAREHOUSES LIKE 'CUSTOMERPULSE_WH';

    CREATE DATABASE IF NOT EXISTS CUSTOMERPULSE_DB;

    SHOW DATABASES LIKE 'CUSTOMERPULSE_DB';

    CREATE SCHEMA IF NOT EXISTS CUSTOMERPULSE_DB.APP;

    SHOW SCHEMAS IN DATABASE CUSTOMERPULSE_DB;

    USE WAREHOUSE CUSTOMERPULSE_WH;
    USE DATABASE CUSTOMERPULSE_DB;
    USE SCHEMA APP;
    SELECT
    CURRENT_ROLE(),
    CURRENT_WAREHOUSE(),
    CURRENT_DATABASE(),
    CURRENT_SCHEMA();

    SHOW TABLES IN SCHEMA CUSTOMERPULSE_DB.APP;

    TRUNCATE TABLE CUSTOMERPULSE_DB.APP.CALL_TRANSCRIPTS;
TRUNCATE TABLE CUSTOMERPULSE_DB.APP.COMPLAINTS;
TRUNCATE TABLE CUSTOMERPULSE_DB.APP.TRANSACTIONS;
TRUNCATE TABLE CUSTOMERPULSE_DB.APP.LOANS;
TRUNCATE TABLE CUSTOMERPULSE_DB.APP.CUSTOMERS;


USE DATABASE CUSTOMERPULSE_DB;
USE SCHEMA APP;

INSERT INTO CUSTOMERS VALUES
('C1001','Aarav Mehta','Jaipur','Premium','2022-04-12'),
('C1002','Diya Sharma','Delhi','Mass Affluent','2023-01-19'),
('C1003','Rohan Verma','Mumbai','Premium','2021-09-03'),
('C1004','Anaya Singh','Bengaluru','Mass Affluent','2024-02-14'),
('C1005','Kabir Jain','Pune','Premium','2020-11-28'),
('C1006','Ishita Gupta','Hyderabad','Mass','2024-06-01'),
('C1007','Arjun Malhotra','Chennai','Mass Affluent','2022-08-16'),
('C1008','Sara Khan','Ahmedabad','Premium','2021-05-22'),
('C1009','Vivaan Kapoor','Kolkata','Mass','2023-10-10'),
('C1010','Myra Joshi','Noida','Premium','2020-03-30');

INSERT INTO LOANS VALUES
('L2001','C1001','Home Loan',4200000,48500,0,'CURRENT'),
('L2002','C1002','Personal Loan',650000,15500,2,'CURRENT'),
('L2003','C1003','Home Loan',5100000,54000,18,'OVERDUE'),
('L2004','C1004','Personal Loan',400000,9800,0,'CURRENT'),
('L2005','C1005','Auto Loan',900000,21000,0,'CURRENT'),
('L2006','C1006','Personal Loan',250000,7600,0,'CURRENT'),
('L2007','C1007','Home Loan',3000000,36000,3,'CURRENT'),
('L2008','C1008','Business Loan',1800000,44000,12,'OVERDUE'),
('L2009','C1009','Auto Loan',700000,17500,0,'CURRENT'),
('L2010','C1010','Home Loan',3800000,42000,0,'CURRENT');

INSERT INTO TRANSACTIONS VALUES
('T3001','C1001','2026-09-25',85000,'CARD','SUCCESS'),
('T3002','C1001','2026-09-18',42000,'UPI','SUCCESS'),
('T3003','C1001','2026-08-26',63000,'CARD','SUCCESS'),
('T3004','C1002','2026-09-20',18000,'UPI','SUCCESS'),
('T3005','C1002','2026-08-29',22000,'CARD','SUCCESS'),
('T3006','C1003','2026-09-27',12000,'UPI','SUCCESS'),
('T3007','C1003','2026-08-10',95000,'CARD','SUCCESS'),
('T3008','C1003','2026-07-02',88000,'CARD','SUCCESS'),
('T3009','C1004','2026-09-26',34000,'UPI','SUCCESS'),
('T3010','C1004','2026-09-15',29000,'CARD','SUCCESS'),
('T3011','C1005','2026-09-28',76000,'CARD','SUCCESS'),
('T3012','C1005','2026-09-12',55000,'UPI','SUCCESS'),
('T3013','C1006','2026-09-23',7000,'UPI','SUCCESS'),
('T3014','C1006','2026-09-04',8500,'CARD','SUCCESS'),
('T3015','C1007','2026-09-21',31000,'UPI','SUCCESS'),
('T3016','C1007','2026-08-22',44000,'CARD','SUCCESS'),
('T3017','C1008','2026-09-05',9000,'UPI','SUCCESS'),
('T3018','C1008','2026-07-12',110000,'CARD','SUCCESS'),
('T3019','C1009','2026-09-24',12000,'UPI','SUCCESS'),
('T3020','C1009','2026-09-10',15000,'CARD','SUCCESS'),
('T3021','C1010','2026-09-29',68000,'CARD','SUCCESS'),
('T3022','C1010','2026-09-11',51000,'UPI','SUCCESS');

INSERT INTO COMPLAINTS VALUES
('CP4001','C1001','2026-08-15','CARD','Card payment reversed unexpectedly','CLOSED'),
('CP4002','C1002','2026-09-01','APP','Mobile app login delay','CLOSED'),
('CP4003','C1003','2026-08-30','LOAN','EMI debit issue not resolved','OPEN'),
('CP4004','C1003','2026-09-11','LOAN','Requested loan statement multiple times','OPEN'),
('CP4005','C1004','2026-09-08','APP','Unable to update nominee details','CLOSED'),
('CP4006','C1005','2026-08-02','CARD','Card limit request','CLOSED'),
('CP4007','C1006','2026-09-05','UPI','UPI transfer failed twice','CLOSED'),
('CP4008','C1007','2026-09-12','CARD','Merchant dispute raised','OPEN'),
('CP4009','C1008','2026-08-18','LOAN','Payment schedule mismatch','OPEN'),
('CP4010','C1008','2026-09-06','SERVICE','Relationship manager did not call back','OPEN'),
('CP4011','C1010','2026-08-20','APP','Biometric login issue','CLOSED'),
('CP4012','C1010','2026-09-02','INVESTMENT','Need portfolio statement','CLOSED');

INSERT INTO CALL_TRANSCRIPTS VALUES
('CL5001','C1001','2026-09-26','Neha','Customer asked about card benefits and was satisfied after explanation.'),
('CL5002','C1002','2026-09-18','Ravi','Customer reported a minor login delay but confirmed the issue was resolved.'),
('CL5003','C1003','2026-09-28','Neha','Customer is frustrated that the EMI debit issue remains unresolved. Customer says multiple follow ups have not helped and wants a senior person to call back.'),
('CL5004','C1004','2026-09-20','Ravi','Customer was satisfied after the nominee update process was explained.'),
('CL5005','C1005','2026-09-22','Neha','Customer asked for a higher card limit and was positive about the service.'),
('CL5006','C1006','2026-09-24','Ravi','Customer confirmed the UPI problem is fixed and was satisfied.'),
('CL5007','C1007','2026-09-23','Neha','Customer is mildly unhappy about an unresolved merchant dispute and asked for a status update.'),
('CL5008','C1008','2026-09-27','Ravi','Customer is very unhappy about the payment schedule mismatch and missing relationship manager callback. Customer says they may move their banking relationship elsewhere.'),
('CL5009','C1009','2026-09-25','Neha','Customer had a normal service interaction and no major issue was reported.'),
('CL5010','C1010','2026-09-29','Ravi','Customer was satisfied after receiving the requested portfolio statement.');

SELECT COUNT(*) AS CUSTOMERS
FROM CUSTOMERPULSE_DB.APP.CUSTOMERS;

SELECT COUNT(*) AS LOANS
FROM CUSTOMERPULSE_DB.APP.LOANS;

SELECT COUNT(*) AS TRANSACTIONS
FROM CUSTOMERPULSE_DB.APP.TRANSACTIONS;

SELECT COUNT(*) AS CALLS
FROM CUSTOMERPULSE_DB.APP.CALL_TRANSCRIPTS;

SELECT *
FROM CUSTOMERPULSE_DB.APP.CUSTOMERS
WHERE CUSTOMER_ID = 'C1003';
