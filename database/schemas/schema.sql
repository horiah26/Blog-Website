CREATE TABLE IF NOT EXISTS users (
    username TEXT UNIQUE NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,  
    date_created VARCHAR(40) NOT NULL,
    date_modified VARCHAR(40) NOT NULL
);


CREATE TABLE IF NOT EXISTS posts (
    post_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    text TEXT NOT NULL,
    owner VARCHAR(100) NOT NULL,
    date_created VARCHAR(40) NOT NULL,
    date_modified VARCHAR(40) NOT NULL
);

CREATE TEMPORARY TABLE users_temp (
    username TEXT UNIQUE NOT NULL PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,  
    date_created VARCHAR(40),
    date_modified VARCHAR(40)
);

INSERT INTO users_temp (username)
SELECT DISTINCT owner FROM posts WHERE owner NOT IN(SELECT username FROM users);

UPDATE users_temp
SET name = username, 
email = CONCAT(username,'@temporary.com'), 
password = username, 
date_created =  CONCAT( TO_CHAR(NOW() :: DATE, 'Mon dd yyyy - ' ),  TO_CHAR(NOW() :: TIME, 'HH24:MI' )),
date_modified =  CONCAT( TO_CHAR(NOW() :: DATE, 'Mon dd yyyy - ' ),  TO_CHAR(NOW() :: TIME, 'HH24:MI' ))
WHERE password is NULL;

INSERT INTO users SELECT * FROM users_temp;

DROP TABLE users_temp;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'posts_owner_fkey') THEN
        ALTER TABLE posts
            ADD CONSTRAINT posts_owner_fkey
            FOREIGN KEY (owner) REFERENCES users(username);
    END IF;
END;
$$;