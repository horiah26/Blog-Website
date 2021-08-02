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

ALTER TABLE users ALTER COLUMN name DROP NOT NULL;
ALTER TABLE users ALTER COLUMN email DROP NOT NULL;
ALTER TABLE users ALTER COLUMN password DROP NOT NULL;
ALTER TABLE users ALTER COLUMN date_created DROP NOT NULL;
ALTER TABLE users ALTER COLUMN date_modified DROP NOT NULL;

INSERT INTO users (username)
SELECT DISTINCT owner FROM posts WHERE owner NOT IN(SELECT username FROM users);

INSERT INTO users VALUES('admin', 
                        'admin', 
                        'admin@temporary.com', 
                        'admin',  
                        CONCAT( TO_CHAR(NOW() :: DATE, 'Mon dd yyyy - ' ),  TO_CHAR(NOW() :: TIME, 'HH24:MI' )),
                        CONCAT( TO_CHAR(NOW() :: DATE, 'Mon dd yyyy - ' ),  TO_CHAR(NOW() :: TIME, 'HH24:MI' )))
                        ON CONFLICT DO NOTHING;

UPDATE users
SET name = username, 
email = CONCAT(username,'@temporary.com'), 
password = username, 
date_created =  CONCAT( TO_CHAR(NOW() :: DATE, 'Mon dd yyyy - ' ),  TO_CHAR(NOW() :: TIME, 'HH24:MI' )),
date_modified =  CONCAT( TO_CHAR(NOW() :: DATE, 'Mon dd yyyy - ' ),  TO_CHAR(NOW() :: TIME, 'HH24:MI' ))
WHERE password is NULL;

ALTER TABLE users ALTER COLUMN name SET NOT NULL;
ALTER TABLE users ALTER COLUMN email SET NOT NULL;
ALTER TABLE users ALTER COLUMN password SET NOT NULL;
ALTER TABLE users ALTER COLUMN date_created SET NOT NULL;
ALTER TABLE users ALTER COLUMN date_modified SET NOT NULL;


DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'posts_owner_fkey') THEN
        ALTER TABLE posts
            ADD CONSTRAINT posts_owner_fkey
            FOREIGN KEY (owner) REFERENCES users(username);
    END IF;
END;
$$;