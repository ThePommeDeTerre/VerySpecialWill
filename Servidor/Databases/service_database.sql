SET GLOBAL sql_mode='';

DROP DATABASE IF EXISTS service_DB;

CREATE DATABASE service_DB;
USE service_DB;


/* ---  USER TABLE ---*/

DROP TABLE IF EXISTS service_user;

CREATE TABLE service_user (
    service_username VARCHAR(50) PRIMARY KEY,
    user_pk VARCHAR (150) DEFAULT ''
);


/* ---  KEY TABLE ---*/

DROP TABLE IF EXISTS share_key;

CREATE TABLE share_key(
    key_id INT(10) NOT NULL AUTO_INCREMENT,
    value_of_key VARCHAR(150) NOT NULL,
    PRIMARY KEY (key_id)
);

/* ---  WILL TABLE ---*/

DROP TABLE IF EXISTS will;

CREATE TABLE will (
    will_id INT(10) NOT NULL AUTO_INCREMENT,
    will_message LONGTEXT NOT NULL,
    will_hmac VARCHAR(256) NOT NULL,
    will_sign VARCHAR(256) NOT NULL,
    will_pub TEXT NOT NULL,
    will_nonce VARCHAR(256),
    user_owner VARCHAR(50) NOT NULL,
    n_min_shares INT(10) NOT NULL,
    PRIMARY KEY (will_id),
    FOREIGN KEY (user_owner)
        REFERENCES service_user (service_username)
);


/* ---  SHARE TABLE ---*/

DROP TABLE IF EXISTS user_share;

CREATE TABLE user_share (
    username_share VARCHAR(50) NOT NULL,
    key_id_share INT(10) NOT NULL,
    will_id_share INT(10) NOT NULL,
    PRIMARY KEY (username_share, key_id_share),
    FOREIGN KEY (username_share)
        REFERENCES service_user (service_username),
    FOREIGN KEY (key_id_share)
        REFERENCES share_key (key_id),
    FOREIGN KEY (will_id_share)
        REFERENCES will (will_id)
);