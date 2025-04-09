
create table query

CREATE TABLE user_details (
    username TEXT PRIMARY KEY,
    password TEXT,
    following TEXT[]  -- Using an array of text
);

CREATE TABLE posts (
    uuid TEXT PRIMARY KEY,
    username TEXT,
    post TEXT,
    vote JSON,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE cmd (
    request_id TEXT PRIMARY KEY,
    username TEXT,
    post TEXT,
    vote JSON,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    post_request_id TEXT
);
