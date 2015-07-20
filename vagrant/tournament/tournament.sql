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

-- Destroy the existing tournament database to start fresh
DROP DATABASE IF EXISTS tournament;

-- Create the tournament database for all of the tournament information
CREATE DATABASE tournament;

-- Connect to the tournament database to create the tables
\c tournament;

-- Destroy existing tables for testing purposes
DROP TABLE IF EXISTS tournament, players, matches CASCADE;

-- Create a table for multiple tournaments with minimum fields
CREATE TABLE tournament ( name TEXT UNIQUE,
						  id SERIAL PRIMARY KEY );

-- Create a table for player information with minimum fields
CREATE TABLE players ( player_name TEXT,
					   tournament_id_fk INT REFERENCES tournament(id),
					   id SERIAL, 
					   PRIMARY KEY (id, tournament_id_fk) );

-- Create a table for matches played with minimum fields
CREATE TABLE matches ( winner INT,
					   loser INT,
					   tournament_id_fk INT REFERENCES tournament(id),
					   FOREIGN KEY (winner, tournament_id_fk) REFERENCES players (id, tournament_id_fk),
					   FOREIGN KEY (loser, tournament_id_fk) REFERENCES players (id, tournament_id_fk),
					   id SERIAL PRIMARY KEY );

-- Create a view for standings using the players and matches tables
CREATE OR REPLACE VIEW standings AS
	SELECT p.id AS id, 
		   p.player_name AS name,
		   p.tournament_id_fk AS tournament_id,
		   COALESCE((SELECT count(winner)
    		 FROM matches
    		 WHERE winner = p.id
    		 GROUP BY winner, tournament_id_fk), 0) AS wins,
		   COALESCE((SELECT count(loser)
    		 FROM matches
    		 WHERE loser = p.id
    		 GROUP BY loser, tournament_id_fk), 0) AS losses
	FROM players p;