#!/usr/bin/env python
#
"""Tournament.py is a Python implementation of a Swiss-system tournament"""

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("ERROR: Unable to connect to database.")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    cursor.execute("TRUNCATE matches;")
    db.commit()
    db.close


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    query = "DELETE FROM players;"
    cursor.execute(query)
    db.commit()
    db.close()


def createEvent(name):
    """Adds an event to the tournament database.

    The database assigns a unique serial id number for the event.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the event's name (must be unique).
    """
    db, cursor = connect()
    query = "INSERT INTO events (name) VALUES (%s);"
    param = (name,)
    cursor.execute(query, param)
    db.commit()
    db.close()


def getEvent(name):
    """Get an event's id from the tournament database.

    Args:
      name: the event's name.

    Returns:
      The event id.

    """
    db, cursor = connect()
    query = "SELECT id FROM events WHERE name = %s;"
    param = (name,)
    cursor.execute(query, param)
    event_id = cursor.fetchall()
    db.close()
    return event_id[0][0]


def countPlayers(event_id):
    """Returns the number of players currently registered."""
    db, cursor = connect()
    query = "SELECT COUNT(*) FROM players WHERE players.event_id = %s;"
    param = (event_id,)
    cursor.execute(query, param)
    number_of_players = cursor.fetchall()
    db.close()
    return number_of_players[0][0]


def registerPlayer(name, event_id):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name:     the player's full name (need not be unique).
      event_id: the id of the event for which the player is registering
    """
    db, cursor = connect()
    query = "INSERT INTO players (name, event_id) VALUES (%s, %s);"
    param = (name, event_id)
    cursor.execute(query, param)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Args:
      event_id: the id of the event

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()
    # player_standings is a PostgreSQL View
    # see tournament.sql for details
    query = "SELECT * FROM player_standings"
    cursor.execute(query)
    standings = cursor.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser, event_id):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    query = "INSERT INTO matches (player1, player2, winner, event_id) \
              VALUES (%s, %s, %s, %s);"
    param = (winner, loser, winner, event_id)
    cursor.execute(query, param)
    db.commit()
    db.close()


def swissPairings(event_id):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
      event_id: the id of the event

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    player_list = playerStandings()

    # the for loop increments by 2 so that it can
    # build pairs of oppenents for a round.
    # the pairs are appended to the empty list pairings
    pairings = []
    for i in xrange(0, len(player_list), 2):
        z = zip(player_list[i], player_list[i + 1])
        pairings.append((z[0][0], z[1][0], z[0][1], z[1][1]))
    return pairings
