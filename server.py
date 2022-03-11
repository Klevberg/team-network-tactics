from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from core import *
import pickle
import db


# Connect to socket
sock = socket(AF_INET, SOCK_DGRAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.bind(("localhost", 5555))


def wait_until_recv_from_address(target_address, bufsize):

    while True:
        message, address = sock.recvfrom(bufsize)
        if address == target_address:
            return message


def get_history():
    return db.get_history()


def new_champion(address):

    character = wait_until_recv_from_address(address, 1024)
    name, rock_p, paper_p, scissors_p = character.decode().split()

    db.add_champion(name, int(rock_p), int(paper_p), int(scissors_p))


def connect_player(first_player_address = ''):

    while True:
        message, address = sock.recvfrom(1024)
        if message.decode() == "1":
            if not first_player_address:
                sock.sendto("red".encode(), address)
            else:
                sock.sendto("blue".encode(), address)
            break
        elif message.decode() == "2":
            new_champion(address)
        elif message.decode() == "3":
            history = pickle.dumps(get_history())
            sock.sendto(history, address)
    
    return address


player1_address = connect_player()   # Connect player 1
player2_address = connect_player(player1_address)   # Connect player 2


champions = db.get_champions()
champions_pickle = pickle.dumps(champions)

sock.sendto(champions_pickle, player1_address)
sock.sendto(champions_pickle, player2_address)


for _ in range(2):
    champs, address = sock.recvfrom(1024)
    if address == player1_address:
        player1_champs = champs.decode().split()
    elif address == player2_address:
        player2_champs = champs.decode().split()


champions = db.get_champions()

match = Match(
    Team([champions[name] for name in player1_champs]),
    Team([champions[name] for name in player2_champs]),
    4
)

match.play()

match_string = pickle.dumps(match)
db.add_to_history(match_string)
sock.sendto(match_string, player1_address)
sock.sendto(match_string, player2_address)
