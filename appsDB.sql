-- This file contains the database schema for the application system

-- User table
DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts(
    UID INT(10) NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(50) NOT NULL,
    role VARCHAR(50),
    -- 0 System administrator
    -- 1 Grad Secretary
    -- 2 Faculty Reviewers
    -- 3 CAC/Chair
    -- 4 Applicants
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    birthday VARCHAR(50) NOT NULL,
    ssn VARCHAR(50) NOT NULL,
    addr VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    zipcode VARCHAR(100) NOT NULL,
    PRIMARY KEY(UID)
);

DROP TABLE IF EXISTS academic_info;
CREATE TABLE academic_info(
    UID INT(10) NOT NULL,
    admin_date VARCHAR(50) NOT NULL,
    degree_app VARCHAR(50) NOT NULL,
    bachelor VARCHAR(50) NOT NULL,
    bach_school VARCHAR(100) NOT NULL,
    bach_gpa FLOAT(3, 2) NOT NULL,
    GRE_verbal VARCHAR(50) NOT NULL,
    GRE_quant VARCHAR(50) NOT NULL,
    FOREIGN KEY(UID) REFERENCES accounts(UID) ON DELETE CASCADE,
    PRIMARY KEY(UID)
);

DROP TABLE IF EXISTS letters;
CREATE TABLE letters(
    UID INT(10) NOT NULL,
    fullname1 VARCHAR(100),
    rec_email1 VARCHAR(255),
    title1 VARCHAR(100),
    affiliation1 VARCHAR(100),
    fullname2 VARCHAR(100),
    rec_email2 VARCHAR(255),
    title2 VARCHAR(100),
    affiliation2 VARCHAR(100),
    fullname3 VARCHAR(100),
    rec_email3 VARCHAR(255),
    title3 VARCHAR(100),
    affiliation3 VARCHAR(100),
    FOREIGN KEY(UID) REFERENCES accounts(UID) ON DELETE CASCADE,
    PRIMARY KEY(UID)
);

DROP TABLE IF EXISTS review;
CREATE TABLE review(
    UID INT(10) NOT NULL,
    review_rating INT(1),
    reason VARCHAR(50),
    comments VARCHAR(100),
    rating INT(1),
    -- 1 to 5 letter rating (5 being best)
    FOREIGN KEY(UID) REFERENCES accounts(UID) ON DELETE CASCADE,
    PRIMARY KEY(UID)
)

DROP TABLE IF EXISTS appstatus;
CREATE TABLE appstatus(
    UID INT(10) NOT NULL,
    decision INT(1),
    -- 0 means denied
    -- 1 means accepted
    -- 2 means accepted with aid
    FOREIGN KEY(UID) REFERENCES accounts(UID) ON DELETE CASCADE,
    PRIMARY KEY(UID)
)

INSERT INTO accounts (username, password, email, role, fname, lname, birthday, ssn, addr, city, state, country, zipcode) VALUES ('adnanshilleh', 'test', 'adnanshilleh@gwu.edu', 1, 'Adnan', 'Shilleh', '02/23/1998', '000110000', '10 North St', 'Shelton', 'CT', 'USA', '06484');