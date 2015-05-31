-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- first delete the database tournament if it exists
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
  id serial,
  name text,
  PRIMARY KEY (id)
  );

CREATE TABLE matches (
  id serial,
  p1 integer references players,
  p2 integer references players,
  winner integer references players,
  PRIMARY KEY (id)
  );
