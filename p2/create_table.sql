
CREATE DATABASE testDB;
USE testDB;

DROP TABLE IF EXISTS users;
CREATE TABLE users
(
	user_id INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(255) CHARACTER SET utf8,
	email VARCHAR(50),
	pwd VARCHAR(50),
	admin TINYINT(1) DEFAULT 1,
	PRIMARY KEY(user_id),
	UNIQUE KEY(username)
);

DROP TABLE IF EXISTS posts;
CREATE TABLE posts
(
	post_id INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(255) CHARACTER SET utf8,
	content TEXT,
	create_time DATETIME DEFAULT NULL,
	modify_time DATETIME DEFAULT NULL,
	PRIMARY KEY(post_id),
	FOREIGN KEY (username) REFERENCES users (username)
);

SET FOREIGN_KEY_CHECKS = 0;

LOAD DATA
    LOCAL INFILE "/data/users.txt"
    REPLACE INTO TABLE users
    FIELDS TERMINATED BY '|'
    LINES TERMINATED BY '\n'
(username,email,pwd,admin);

LOAD DATA
    LOCAL INFILE "/data/posts.txt"
    REPLACE INTO TABLE posts
    FIELDS TERMINATED BY '|'
    LINES TERMINATED BY '\n'
(username,content);

SET FOREIGN_KEY_CHECKS = 1;