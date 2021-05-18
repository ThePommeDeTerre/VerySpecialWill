SET GLOBAL sql_mode='';

DROP DATABASE IF EXISTS auth_DB;

CREATE DATABASE auth_DB;

USE auth_DB;

DROP TABLE IF EXISTS user_table;

CREATE TABLE user_table (
    username VARCHAR(50) NOT NULL,
    mail VARCHAR(50) NOT NULL,
    jwt VARCHAR(250) DEFAULT '',
    fa2_token VARCHAR(128) DEFAULT '',
    pwd_salt VARCHAR(150) NOT NULL,
    pwd_hash VARCHAR(150) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (username)
);