CREATE DATABASE `anime_storage` CHARACTER SET utf8 COLLATE utf8_general_ci;

DROP TABLE IF EXISTS `animelist`;
DROP TABLE IF EXISTS `anime`;

CREATE TABLE animelist
(
    id INT(11) NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL, 
    url TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE anime
(
    id INT(11) NOT NULL AUTO_INCREMENT,
    category INT(11) NOT NULL,
    name TEXT NOT NULL, 
    dl_url TEXT NOT NULL, 
    update_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);