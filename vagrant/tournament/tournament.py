#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
# Contains all of the functions required to run the tournament database

import psycopg2
import bleach


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print ("""Database connection failed. Check to ensure the 
            tournament database is available.""")
        sys.exit()


def updateDatabase(query, bleached, db, c):
    """Update the database and close the connection."""

    c.execute(query, bleached)
    db.commit()
    db.close()


def readDatabase(query, bleached, db, c):
    """Read from the database and close the connection."""

    c.execute(query, bleached)
    result = c.fetchall()
    db.close()

    return result


def deleteMatches():
    """Remove all the match records from the database."""

    db, c = connect()

    query = "TRUNCATE TABLE matches RESTART IDENTITY CASCADE;"
    bleached = None

    updateDatabase(query, bleached, db, c)


def deletePlayers():
    """Remove all the player records from the database."""

    db, c = connect()

    query = "TRUNCATE TABLE players RESTART IDENTITY CASCADE;"
    bleached = None

    updateDatabase(query, bleached, db, c)


def deleteTournament():
    """
    Remove all the tournament records from the database.
    Requires key constraints to be removed from players and matches first.
    """

    db, c = connect()

    query = "TRUNCATE TABLE tournament RESTART IDENTITY CASCADE;"
    bleached = None

    updateDatabase(query, bleached, db, c)


def getTournamentId(tournamentName):
    """Returns a tournament id if the name is known."""

    db, c = connect()

    query = "SELECT id FROM tournament WHERE name = %s;"
    bleached = (bleach.clean(tournamentName),)

    result = readDatabase(query, bleached, db, c)
    tournament_id = int(result[0][0])

    return tournament_id


def countPlayers(tournament_id):
    """Returns the number of players currently registered for a given
    tournament id.

    Args:
      tournament_id: the tournament's id (UNIQUE)
    """

    db, c = connect()

    query = "SELECT count(id) FROM players WHERE tournament_id_fk = %s;"
    bleached = (bleach.clean(tournament_id),)

    result = readDatabase(query, bleached, db, c)
    player_count = int(result[0][0])

    return player_count


def registerPlayer(name, tournament_id):
    """Adds a player to the tournament database for a given tournament.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    INSERT INTO table_name (column1,column2,column3,...)
    VALUES (value1,value2,value3,...);

    Args:
      name: the player's full name (need not be unique).
      tournament_id: the tournament's id (UNIQUE)
    """

    db, c = connect()

    query = """INSERT INTO players (player_name, tournament_id_fk)
               VALUES (%s, %s);"""
    bleached = (bleach.clean(name), bleach.clean(tournament_id))

    updateDatabase(query, bleached, db, c)


def createTournament(tournament_name):
    """
    Adds a new tournament to the tournament database.

    The database assigns a unique serial id number for the tournament.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the tournament's name.
    """

    db, c = connect()

    query = "INSERT INTO tournament (name) VALUES (%s);"
    bleached = (bleach.clean(tournament_name),)

    updateDatabase(query, bleached, db, c)


def playerStandings(tournament_id):
    """Returns a list of the players and their win records, sorted by wins
    for a given tournament id.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Args:
      tournament_id: the tournament's id (UNIQUE)

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db, c = connect()

    query = """SELECT id, name, wins, wins+losses AS matches
               FROM standings WHERE tournament_id = %s
               ORDER BY wins DESC, losses ASC;"""
    bleached = (bleach.clean(tournament_id),)

    result = readDatabase(query, bleached, db, c)
    standings = [(int(row[0]), str(row[1]),
                  int(row[2]), int(row[3]))
                 for row in result]

    return standings


def reportMatch(winner, loser, tournament_id):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament_id: the tournament's id (UNIQUE)
    """

    db, c = connect()

    query = """INSERT INTO matches (winner, loser, tournament_id_fk)
              VALUES (%s, %s, %s);"""
    bleached = (bleach.clean(winner), bleach.clean(loser),
                bleach.clean(tournament_id))

    updateDatabase(query, bleached, db, c)


def swissPairings(tournament_id):
    """Returns a list of pairs of players for the next round of a match
    for a given tournament id.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
      tournament_id: the tournament's id (UNIQUE)

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name

    Test case:
    [(609, 'Twilight Sparkle', 1, 1), (611, 'Applejack', 1, 1),
      (610, 'Fluttershy', 0, 1), (612, 'Pinkie Pie', 0, 1)]
    """

    standings = playerStandings(tournament_id)

    pairings = []

    swiss_pairs = zip(standings[0::2], standings[1::2])

    for x in swiss_pairs:
        pairings.append((x[0][0], x[0][1], x[1][0], x[1][1]))

    # Original pairing method, replaced by using zip() function instead
    # pairings = []

    # for x in range(len(standings[::2])):
    #     pairings.append((standings[x * 2][0], standings[x * 2][1],
    #                      standings[x * 2 + 1][0], standings[x * 2 + 1][1]))

    return pairings
