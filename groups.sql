CREATE TABLE groups (
       name VARCHAR(64),

       id SERIAL,
       PRIMARY KEY(id)
       );

CREATE TABLE users (
       name VARCHAR(64),
       rss VARCHAR(128),       

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
