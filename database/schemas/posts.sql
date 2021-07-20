CREATE TABLE IF NOT EXISTS posts (
                                    post_id  SERIAL PRIMARY KEY,
                                    title VARCHAR(255) NOT NULL,
                                    text TEXT NOT NULL,
                                    owner VARCHAR(100) NOT NULL,
                                    date_created VARCHAR(40) NOT NULL,
                                    date_modified VARCHAR(40) NOT NULL
                                 )