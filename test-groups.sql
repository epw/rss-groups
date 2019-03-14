INSERT INTO groups (name) VALUES ('Science & Science Fiction');
INSERT INTO users (name, rss) VALUES ('Ars Technica', 'http://feeds.arstechnica.com/arstechnica/index');
INSERT INTO users (name, rss) VALUES ('Tor', 'https://www.tor.com/feed/');
INSERT INTO group_users (group_id, user_id) VALUES (
       (SELECT id AS group_id FROM groups WHERE name = 'Science & Science Fiction'),
       (SELECT id AS user_id FROM users WHERE name = 'Ars Technica'));
INSERT INTO group_users (group_id, user_id) VALUES (
       (SELECT id AS group_id FROM groups WHERE name = 'Science & Science Fiction'),
       (SELECT id AS user_id FROM users WHERE name = 'Tor'));
