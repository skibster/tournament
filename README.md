# tournament
Project 2: Udacity Swiss Tournament Results  

1. This project runs a set of tests in a preconfigured virtual machine environment to simulate a Swiss Style tournament.
2. To install the virtual machine environment, you will install Git, Virtual Box and Vagrant. Detailed installation instructions can be found here: https://www.udacity.com/wiki/ud197/install-vagrant
3. Download this tournament repository and place it in your /vagrant directory.
4. In your terminal, run the following commands:  
  * cd /path/to/vagrant (changes directories to the 'vagrant' directory).  
  * vagrant up (starts the virtual machine). 
  * vagrant ssh (creates a remote connection to your virtual machine).  
  * cd /vagrant/tournament  (changes directories to the 'tournament' directory in your virtual machine).  
  * psql (launches the PostgreSQL interactive terminal).  
  * \i tournament.sql (this command reads in the sql commands from 'tournament.sql' which will create the 'tournaments' database and the necessary tables and views needed by the application).  
  * \q (to quit the PostgreSQL interactive terminal).  
  * python tournament_test_extra.py (this runs the python tests against the tournament.py module. This is a special version of the test file to support the extra credit).  

Results:
The test results should be as show below:  
  
0. Events can be deleted.  
1. Old matches can be deleted.  
2. Player records can be deleted.  
3. After deleting, countPlayers() returns zero.  
4. After registering a player, countPlayers() returns 1.  
5. Players can be registered and deleted.  
6. Newly registered players appear in the standings with no matches.  
7. After a match, players have updated standings.  
8. After one match, players with one win are paired.  
Success!  All tests pass!
