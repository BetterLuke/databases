# Intro to Relational Databases
=============

These are the files for the Introduction to Relational Databases class. The goal here is to provide a introduction to designing a database through the use of PostgreSQL.

Contains:

- Code from lectures from Udacity Intro to Relational Databases
- Code for Project: Tournament Planner

## Table of contents

- [Changelog](#changelog)
- [Documentation](#documentation)
- [Creators](#creators)

## Changelog:

### 7/17/15 - Changed pairing method to use zip function

  * swissPairings method now uses the zip function for testing, no functionality changes

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

- Python 2.7
- Vagrant

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
