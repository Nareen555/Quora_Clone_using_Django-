A website smiliar to Quora where you can ask question and answer the question which questioned by others.
You can only see or like if you follow the particular user and You can add like for the evey question in you feed page.
Username is uique name it not have duplicate user name.

Login page :
localhost url
http://127.0.0.1:8000/quora_clone/log_in/

![image alt](https://github.com/Nareen555/Quora_Clone_using_Django-/blob/39c275c9340a6f350bdea630e930c1a8d7482b7b/image/Screenshot%20from%202025-04-09%2013-45-02.png)

Feed page:
http://127.0.0.1:8000/quora_clone/log_in/home/?username=john&password=password

![image alt](https://github.com/Nareen555/Quora_Clone_using_Django-/blob/39c275c9340a6f350bdea630e930c1a8d7482b7b/image/Screenshot%20from%202025-04-09%2013-45-51.png)

Follower and Following Page:
http://127.0.0.1:8000/quora_clone/log_in/home/followers/?username=john&password=password

![image alt](https://github.com/Nareen555/Quora_Clone_using_Django-/blob/39c275c9340a6f350bdea630e930c1a8d7482b7b/image/Screenshot%20from%202025-04-09%2013-47-27.png)

Technologies Used

    Python
    jinja code
    Postgresql Database


Query to create tables

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
