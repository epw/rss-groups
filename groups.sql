CREATE TYPE blog_type AS ENUM
       ('rss',
	'blogger',
        'wordpress');

CREATE TABLE groups (
       name VARCHAR(64),

       public BOOLEAN NOT NULL DEFAULT FALSE,

       id SERIAL,
       PRIMARY KEY(id)
       );

CREATE TABLE users (
       name VARCHAR(64),
       email VARCHAR(128),
       rss VARCHAR(128),       
       type blog_type,
       username VARCHAR(128),
       password TEXT,
       state TEXT,
       credentials TEXT,
       id SERIAL,
       PRIMARY KEY(id)
       );
       
CREATE TABLE group_users (
       group_id INT NOT NULL,
       user_id INT NOT NULL,

       FOREIGN KEY (group_id)
              REFERENCES groups(id)
       	      ON DELETE CASCADE
	      ON UPDATE CASCADE,
       FOREIGN KEY (user_id)
              REFERENCES users(id)
       	      ON DELETE CASCADE
	      ON UPDATE CASCADE
       );

CREATE TABLE posts (
       user_id INT NOT NULL,

       type blog_type,
       url VARCHAR(255),
       xml TEXT,

       id SERIAL,
       PRIMARY KEY(id),

       FOREIGN KEY (user_id)
              REFERENCES users(id)
       	      ON DELETE CASCADE
	      ON UPDATE CASCADE
       );
