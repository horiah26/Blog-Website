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
    owner VARCHAR(100) NOT NULL REFERENCES users (username),
    date_created VARCHAR(40) NOT NULL,
    date_modified VARCHAR(40) NOT NULL
);
