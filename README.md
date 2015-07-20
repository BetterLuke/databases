# Tournament Database (Intro to Relational Databases)
=============

This is a project for creating a simple tournament database. The user will be able to register players for tournaments, report matches, check standings, and producess swiss pairings for future rounds of tournaments.

Contains:

- Code from lectures from Udacity Intro to Relational Databases
- Code for Project: Tournament Planner

## Table of contents

- [Changelog](#changelog)
- [Documentation](#documentation)
- [Creators](#creators)

## Changelog:

### 7/20/15 - Refactoring code and changed swissPairing to use zip()

  * Refactored code to remove more repetition by adding updateDatabase() and readDatabase() methods
  * Updated schema to include composite key for player / tournament pairs
  * Removed creating standings in view since tournament_id was added to players schema instead
  * Updated swissPairings method now uses the zip function for testing, no functionality changes

### 7/15/15 - Refactoring code
  * Refactored code to remove repetition and added format() for queries to use tuples
  * Updated tournament.sql to connect to tournament database so tables are not created in a separate database
  * Updated tournament_test.py test cases to avoid deleting after every test case and now creates a new tournament to test instead

### 7/14/15 - Added support for multiple tournaments:
  * Added a tournament table for storing tournaments
  * Updated player and matches tables to reference a tournament id 
  * Updated tournament_test.py test suite for handling tourmanets
  * Updated comments to reflect multiple tournament support

### 7/6/15 - Finished Swiss Pairing:
  * Added more comments to code
  * Finished logic for reading every other standing and pairing it to closest winner

### 6/26/15 - Updated to pass 6/8 of the test cases:
  * Created view for calculating standings using the player and matches tables
  * Completed functions for inserting data into the database tables

### 6/22/15 - Initial commit and database design:
  * Created project and initial commit for tournament files

## Documentation

### Requirements:

- [Python 2.7](https://www.python.org/downloads/) for running the tournament functions and tests
- [PostgreSQL 9.3.8 or later](http://www.postgresql.org/download/) for creating the database
- [psycopg](http://initd.org/psycopg/download/) for connecting to the PostgreSQL database
- [bleach](http://bleach.readthedocs.org/en/latest/) for protecting against database attacks
- *optional* [Vagrant](http://www.vagrantup.com/downloads.html) for using a virtual instance to optimize workflows
- *optional* [VirtualBox](https://www.virtualbox.org/) **required if using Vagrant**

### To run:

1. Download and unzip the project folder from 
[here](https://github.com/hanwenyan/databases/archive/master.zip).
2. Go to the vagrant folder and run `vagrant up` and `vagrant ssh`.
3. Run `createdb tournament` in the command line to create a tournament database.
4. Run `psql -f tournament.sql && python tournament_test.py` which will create the database tables and run the provided test suite to test the database and code.
5. Run `psql tournament` in order to perform queries against the database.

## Creators

  * Hanwen Yan
  * Udacity
