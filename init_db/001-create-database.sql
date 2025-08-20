CREATE USER hiring_user WITH ENCRYPTED PASSWORD 'hiring_pass';
CREATE DATABASE hiring_db OWNER hiring_user;

CREATE USER exercises_user WITH ENCRYPTED PASSWORD 'exercises_pass';
CREATE DATABASE exercises_db OWNER exercises_user;

GRANT ALL PRIVILEGES ON DATABASE hiring_db TO hiring_user;
GRANT ALL PRIVILEGES ON DATABASE exercises_db TO exercises_user;
