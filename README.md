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

1. Download and unzip the project folder from [here](https://github.com/hanwenyan/databases/archive/master.zip).
2. Go to the vagrant folder and run `vagrant up` and `vagrant ssh`.
3. Run `psql tournament -f tournament.sql` script which will set up the database.
4. Run `tournament_test.py` which will run the provided test suite to test the database and code.
5. Run `psql tournament` in order to perform queries against the database.

## Creators

  * Hanwen Yan
  * Udacity
