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
DROP TABLE tournament, players, matches;

-- Create a table for multiple tournaments
CREATE TABLE tournament ( name TEXT,
						  id SERIAL PRIMARY KEY);

-- Create a table for player information
CREATE TABLE players ( player_name TEXT,
					   id SERIAL PRIMARY KEY );

-- Create a table for matches played
CREATE TABLE matches ( winner INT REFERENCES players(id),
					   loser INT REFERENCES players(id),
					   id SERIAL PRIMARY KEY );

-- Create a view for standings using the players and matches tables
CREATE OR REPLACE VIEW standings AS
	SELECT p.id AS id, 
		   p.name AS name,
		   COALESCE((SELECT count(winner)
    		 FROM matches
    		 WHERE winner = p.id
    		 GROUP BY winner), 0) AS wins,
		   COALESCE((SELECT count(loser)
    		 FROM matches
    		 WHERE loser = p.id
    		 GROUP BY loser), 0) AS losses
	 FROM players p;