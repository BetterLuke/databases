#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""

    db = psycopg2.connect("dbname={}".format(database_name))
    cursor = db.cursor()
    return db, cursor


def deleteMatches():
    """Remove all the match records from the database."""

    db, c = connect()

    c.execute("TRUNCATE TABLE matches RESTART IDENTITY CASCADE;")

    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""

    db, c = connect()

    c.execute("TRUNCATE TABLE players RESTART IDENTITY CASCADE;")

    db.commit()
    db.close()


def deleteTournament():
    """
    Remove all the tournament records from the database.
    Requires key constraints to be removed from players and matches first.
    """

    db, c = connect()

    c.execute("TRUNCATE TABLE tournament RESTART IDENTITY CASCADE;")

    db.commit()
    db.close()


def countPlayers(tournament_id):
    """Returns the number of players currently registered for a given
    tournament id.

    Args:
      tournament_id: the tournament's id (UNIQUE)
    """

    db, c = connect()

    query = "SELECT count(id) FROM players WHERE tournament_id_fk = %s ;"
    c.execute(query, (bleach.clean(tournament_id)))  # Sanitize the value
    player_count = int(c.fetchall()[0][0])

    db.close()
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
    c.execute(query,
              (bleach.clean(name),
               bleach.clean(tournament_id)))  # Sanitize the values

    db.commit()
    db.close()


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

    c.execute(query, (bleach.clean(tournament_name),))  # Sanitize the value

    db.commit()
    db.close()


def createStandingsView(tournament_id):
    """
    Creates a view in the database for standings for a given
    tournament id.

    Args:
      tournament_id: the tournament's id (UNIQUE)
    """

    db, c = connect()

    query = """CREATE OR REPLACE VIEW standings AS
              SELECT p.id AS id,
              p.player_name AS name,
              COALESCE((SELECT count(winner)
              FROM matches m
              WHERE winner = p.id AND tournament_id_fk = {0}
              GROUP BY winner, tournament_id_fk), 0) AS wins,
              COALESCE((SELECT count(loser)
              FROM matches m
              WHERE loser = p.id AND tournament_id_fk = {0}
              GROUP BY loser, tournament_id_fk), 0) AS losses
              FROM players p
              WHERE tournament_id_fk = {0};"""

    parameters = (bleach.clean(tournament_id))

    c.execute(query.format(*parameters))

    db.commit()
    db.close()


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

    createStandingsView(tournament_id)

    db, c = connect()

    query = """SELECT id, name, wins, wins+losses AS matches
               FROM standings ORDER BY wins DESC, losses ASC;"""

    c.execute(query)
    standings = [(int(row[0]), str(row[1]),
                  int(row[2]), int(row[3]))
                 for row in c.fetchall()]
    db.close()
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
              VALUES ({0}, {1}, {2});"""

    parameters = (bleach.clean(winner), bleach.clean(loser),
                  bleach.clean(tournament_id))

    c.execute(query.format(*parameters))  # Sanitize the values

    db.commit()
    db.close()


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
    """
    standings = playerStandings(tournament_id)

    """
    Test case:
    [(609, 'Twilight Sparkle', 1, 1), (611, 'Applejack', 1, 1),
      (610, 'Fluttershy', 0, 1), (612, 'Pinkie Pie', 0, 1)]
    """

    pairings = []

    for x in range(len(standings[::2])):
        pairings.append((standings[x * 2][0], standings[x * 2][1],
                         standings[x * 2 + 1][0], standings[x * 2 + 1][1]))

    return pairings
