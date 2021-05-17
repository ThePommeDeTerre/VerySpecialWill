DROP DATABASE IF EXISTS auth_DB;

CREATE DATABASE auth_DB;

USE auth_DB;

DROP TABLE IF EXISTS user_table;

CREATE TABLE user_table (
    username VARCHAR(50) NOT NULL,
    mail VARCHAR(50) NOT NULL,
    fa2_token VARCHAR(32),
    pwd_salt VARCHAR(150) NOT NULL,
    pwd_hash VARCHAR(150) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (username)
);