# Team Network Tactics

- A game for the mandatory assignment in INF142


## About

Welcome to TNT! Let me tell you a bit about how this game works.

The game consists of three major components: the server (`server.py`), the client (`client.py`), and the database (`db.json`).

The database is a JSON file, which has the following structure:

```json
{
    "champions": {
        "Vain": [50,25,25],
        "Dr. Yi": [10,10,80],
        "Twist": [10,25,65],
        "Guan": [30,35,35],
        "Siva": [60,20,20],
        "Katina": [20,50,30],
        "Asir": [5,5,90],
        "Cactus": [5,90,5],
        "Luanne": [90,5,5]
    },
    "history": []
}
```

The 'champions' section stores the playable champions, while the 'history' section stores the previously played matches.


## Guide

Now, I will provide a simple guide that you can follow to play the game.

### Step 1:

Run the python script `server.py` in one terminal
>python server.py

### Step 2:

Run the python script `client.py` in two different terminals
>python client.py


The clients will show three options:

```
1. PLAY GAME
2. CREATE CHAMPION
3. VIEW HISTORY
```

#### PLAY GAME

When this option is selected, the first client will connect to the server and wait for the second client to connect. Once both clients have selected this option, the players will get to select their champions. After the first player has picked their champions, the client will again wait for the other player. Once both players have picked their characters, the game will begin, and the same result will show up on both clients. The server will save the match to the database.

#### CREATE CHAMPION

When create champion is picked, the client will connect to the server and let it know that the second option was selected. The player will then be prompted for the name and stats of the new champion. The server is listening, so when the player is finished, the server calls on the necessary functions in `db.py` to add the champion to the database.
The player will again see the option screen, and can choose to start the game (where they will now be able to play using their new custom champion), or add more champions first.

#### VIEW HISTORY

When the client lets the server know that the player selected option 3, the server will use the database tooling (`db.py`) to fetch the history stored in the database. This feature is still a work in progress, as the client has a hard time decoding the match data. The socket communication, however, between the client and the server works as it should. The client will print out what it was able to retrieve, which is the match encoded by jsonpickle, and the player will again see the option screen.


## Thanks for playing!

I hope you enjoyed! Please let me know if you have any questions!