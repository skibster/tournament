#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteEvents():
    deleteEvents()
    print "0. Events can be deleted."


def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDeletePlayers():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCreateEvent(name):
    createEvent(name)

def testGetEvent(name):
    return getEvent(name)

def testCount(event_id):
    deleteMatches()
    deletePlayers()
    c = countPlayers(event_id)
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister(event_id):
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar", event_id)
    c = countPlayers(event_id)
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete(event_id):
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney", event_id)
    registerPlayer("Joe Malik", event_id)
    registerPlayer("Mao Tsu-hsi", event_id)
    registerPlayer("Atlanta Hope", event_id)
    c = countPlayers(event_id)
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers(event_id)
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches(event_id):
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray", event_id)
    registerPlayer("Randy Schwartz", event_id)
    standings = playerStandings(event_id)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches(event_id):
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton", event_id)
    registerPlayer("Boots O'Neal", event_id)
    registerPlayer("Cathy Burton", event_id)
    registerPlayer("Diane Grant", event_id)
    standings = playerStandings(event_id)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings(event_id)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings(event_id):
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle", event_id)
    registerPlayer("Fluttershy", event_id)
    registerPlayer("Applejack", event_id)
    registerPlayer("Pinkie Pie", event_id )
    standings = playerStandings(event_id)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings(event_id)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


if __name__ == '__main__':
    testDeleteEvents()
    testDeleteMatches()
    testDeletePlayers()
    event_name = "My Cool Event!"
    testCreateEvent(event_name)
    event = testGetEvent(event_name)
    testCount(event)
    testRegister(event)
    testRegisterCountDelete(event)
    testStandingsBeforeMatches(event)
    testReportMatches(event)
    testPairings(event)
    print "Success!  All tests pass!"


