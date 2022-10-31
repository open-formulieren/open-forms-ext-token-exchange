CREATE USER openforms;
CREATE DATABASE openforms;
GRANT ALL PRIVILEGES ON DATABASE openforms TO openforms;
ALTER ROLE openforms CREATEDB; --Needed to create the test database
