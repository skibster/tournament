-- Table definitions for the tournament project.
--
--
-- first delete the database tournament if it exists
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

-- connect to newly created database
\c tournament;

-- create event table to differenciate multiple tournaments
-- without having to delete players from database
--   a column for an event's id (id)
--   a column for an event's name (name)
CREATE TABLE events (
  id serial,
  name text UNIQUE,
  PRIMARY KEY (id)
  );

-- create player table which consists of
--   a column for a player's id (id)
--   a column for a player's full name (name)
--   a column for an event for which the player is registering (event_id)
CREATE TABLE players (
  id serial,
  name text,
  event_id integer,
  PRIMARY KEY (id)
  );

-- create matches table which consists of
--   a column for a match's id (id)
--   a column for the player id of the first oppenent, e.g., home team (player1)
--   a column for the player id of the second oppenent, e.g., away team (player2)
--   a column for the winner of the match (winner)
--   a column for an event for which the player is registering (event_id)
CREATE TABLE matches (
  id serial,
  player1 integer references players,
  player2 integer references players,
  winner integer references players,
  event_id integer references events,
  PRIMARY KEY (id)
  );

-- the match_numbers view returns a table with columns for
-- player id, player name, and no_of_matches for each player:
CREATE VIEW match_numbers AS
  SELECT players.id, players.name, COUNT(matches.*) as no_of_matches
  FROM players LEFT JOIN matches ON
  players.event_id=matches.event_id AND
  (players.id=matches.player1 OR players.id=matches.player2)
  GROUP BY players.id ORDER BY players.id;


-- the match_wins view returns a table with column for
-- player id and no_of_wins for each player:
CREATE VIEW match_wins AS
  SELECT players.id, COUNT(matches.*) AS no_of_wins
  FROM players LEFT JOIN matches ON
  players.id=matches.winner
  GROUP BY players.id ORDER BY players.id;


-- the player_standings view returns a table with columns for
-- player id, player name, number of wins and number of matches for each player:
CREATE VIEW player_standings AS
  SELECT match_numbers.id, match_numbers.name, match_wins.no_of_wins, match_numbers.no_of_matches
  FROM match_numbers, match_wins
  WHERE match_numbers.id=match_wins.id ORDER BY match_wins.no_of_wins DESC;
