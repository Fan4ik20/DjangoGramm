CREATE DATABASE DjangoGramm;

CREATE USER tester with PASSWORD 'tester';
ALTER USER tester CREATEDB;

GRANT ALL PRIVILEGES ON DATABASE DjangoGramm to tester;
