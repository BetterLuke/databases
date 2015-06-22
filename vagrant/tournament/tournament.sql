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

-- Destroy existing tables for testing
DROP TABLE tournament, players, matches;

-- Create a table for multiple tournaments
CREATE TABLE tournament ( name TEXT,
						  id SERIAL PRIMARY KEY);

-- Create a table for player information
CREATE TABLE players ( name TEXT,
					   id SERIAL PRIMARY KEY );

-- Create a table for matches played
CREATE TABLE matches ( p1 INT REFERENCES players(id),
					   p2 INT REFERENCES players(id),
					   winner INT REFERENCES players(id),
					   id SERIAL PRIMARY KEY );