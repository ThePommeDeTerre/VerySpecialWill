DROP DATABASE IF EXISTS auth_DB;

CREATE DATABASE auth_DB;

USE auth_DB;

DROP TABLE IF EXISTS user_table;

CREATE TABLE user_table (
    username VARCHAR(50) NOT NULL,
    mail VARCHAR(50) NOT NULL,
    pwd_salt VARCHAR(150) NOT NULL,
    pwd_hash VARCHAR(150) NOT NULL,
    PRIMARY KEY (username)
);