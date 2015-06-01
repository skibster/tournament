-- Table definitions for the tournament project.
--
--
-- first delete the database tournament if it exists
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

-- connect to newly created database
\c tournament;

-- create player table which consists of
--   a column for a player's id (id)
--   a column for a player's full name (name)
CREATE TABLE players (
  id serial,
  name text,
  PRIMARY KEY (id)
  );

-- create matches table which consists of
--   a column for a match's id (id)
--   a column for the player id of the first oppenent, e.g., home team (player1)
--   a column for the player id of the second oppenent, e.g., away team (player2)
--   a column for the winner of the match (winner)
CREATE TABLE matches (
  id serial,
  player1 integer references players,
  player2 integer references players,
  winner integer references players,
  PRIMARY KEY (id)
  );

-- The player_standings view returns a table that contains a row for each player
-- sorted by wins where the first row is the player with the most wins or is tied with the most wins.
-- The table contains columns for each player's [id], [name], number of [wins] and number of [matches]-- played.
CREATE VIEW player_standings AS
  SELECT players.id,
         players.name,
         (SELECT COUNT(*) FROM matches WHERE players.id = matches.winner) AS wins,
         (SELECT COUNT(*) FROM matches WHERE players.id = matches.player1 OR players.id = matches.player2) AS matches
         FROM players ORDER BY wins DESC;
