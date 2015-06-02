#!/usr/bin/env python
#
"""Tournament.py is a Python implementation of a Swiss-system tournament"""

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteEvents():
    """Remove all the event records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM events;")
    conn.commit()
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    conn.commit()
    conn.close()


def createEvent(name):
    """Adds an event to the tournament database.

    The database assigns a unique serial id number for the event.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the event's name (must be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO events (name) VALUES (%s);", (name,))
    conn.commit()
    conn.close()


def getEvent(name):
    """Get an event's id from the tournament database.

    Args:
      name: the event's name.
      
    Returns:
      The event id.
      
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id FROM events WHERE name = %s;", (name,))
    event_id = c.fetchall()
    conn.close()
    return event_id[0][0]


def countPlayers(event_id):
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM players WHERE players.event_id = %s;", (event_id,))
    number_of_players = c.fetchall()
    conn.close()
    return number_of_players[0][0]


def registerPlayer(name, event_id):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name:     the player's full name (need not be unique).
      event_id: the id of the event for which the player is registering
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name, event_id) VALUES (%s, %s);", (name, event_id))
    conn.commit()
    conn.close()


def playerStandings(event_id):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
      event_id: the id of the event

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    # player_standings is a PostgreSQL View
    # see tournament.sql for details
    c.execute("SELECT * FROM player_standings")
    standings = c.fetchall()
    conn.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches (player1, player2, winner) \
              VALUES (%s, %s, %s);", (winner, loser, winner))
    conn.commit()
    conn.close()


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
    player_list = playerStandings(event_id)

    # the for loop increments by 2 so that it can build pairs of oppenents for a round.
    # players [0] and player[1] are paired for a match,
    # player [2] and player[3] are paired for a match, etc.
    # the pairs are appended to the empty list pairings
    pairings = []
    for i in xrange(0, len(player_list), 2):
        player_id1 = player_list[i][0]
        player_name1 = player_list[i][1]
        player_id2 = player_list[i+1][0]
        player_name2 = player_list[i+1][1]

        pairings.append((player_id1, player_name1, player_id2, player_name2))
    return pairings
