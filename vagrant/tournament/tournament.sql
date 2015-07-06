-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Example:
-- CREATE TABLE posts ( content TEXT,
--                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--                     id SERIAL );

-- Create the tournament database for all of the tournament information
CREATE DATABASE tournament;

-- Destroy existing tables for testing purposes
DROP TABLE tournament, players, matches CASCADE;

-- Create a table for multiple tournaments with minimum fields
CREATE TABLE tournament ( name TEXT,
						  id SERIAL PRIMARY KEY );

-- Create a table for player information with minimum fields
CREATE TABLE players ( player_name TEXT,
					   id SERIAL PRIMARY KEY );

-- Create a table for matches played with minimum fields
CREATE TABLE matches ( winner INT REFERENCES players(id),
					   loser INT REFERENCES players(id),
					   tournament_id_fk INT REFERENCES tournament(id),
					   id SERIAL PRIMARY KEY );

-- Create a view for standings using the players and matches tables
CREATE OR REPLACE VIEW standings AS
	SELECT p.id AS id, 
		   p.player_name AS name,
		   COALESCE((SELECT count(winner)
    		 FROM matches
    		 WHERE winner = p.id
    		 GROUP BY winner, tournament_id_fk), 0) AS wins,
		   COALESCE((SELECT count(loser)
    		 FROM matches
    		 WHERE loser = p.id
    		 GROUP BY loser, tournament_id_fk), 0) AS losses
	FROM players p;

CREATE OR REPLACE VIEW testing AS
	SELECT p.id AS id, 
		   p.player_name AS name,
		   count(wins.winner),
		   count(losses.loser)
	FROM players p, 
		(SELECT winner, tournament_id_fk
		 FROM matches
		 GROUP BY winner, tournament_id_fk) as wins,
	   	(SELECT loser, tournament_id_fk
		 FROM matches
		 GROUP BY loser, tournament_id_fk) as losses
   	GROUP BY p.id;