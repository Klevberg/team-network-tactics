from rich import print
from rich.prompt import Prompt
from rich.table import Table

from core import Champion, Match, Shape, Team

from socket import socket, AF_INET, SOCK_DGRAM
import pickle
from jsonpickle import unpickler


# Connect to socket
client = socket(AF_INET, SOCK_DGRAM)
server_address = ("localhost", 5555)
client.connect(server_address)


def print_available_champs(champions: dict[Champion]) -> None:

    # Create a table containing available champions
    available_champs = Table(title='Available champions')

    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    # Populate the table
    for champion in champions.values():
        available_champs.add_row(*champion.str_tuple)

    print(available_champs)


def input_champion(prompt: str,
                   color: str,
                   champions: dict[Champion],
                   selected_champs: list[str]) -> None:

    # Prompt the player to choose a champion and provide the reason why
    # certain champion cannot be selected
    while True:
        match Prompt.ask(f'[{color}]{prompt}'):
            case name if name not in champions:
                print(f'The champion {name} is not available. Try again.')
            case name if name in selected_champs:
                print(f'{name} is already in your team. Try again.')
            #case name if name in player2:
            #    print(f'{name} is in the enemy team. Try again.')
            case _:
                selected_champs.append(name)
                break


def print_match_summary(match: Match) -> None:

    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }

    # For each round print a table with the results
    for index, round in enumerate(match.rounds):

        # Create a table containing the results of the round
        round_summary = Table(title=f'Round {index+1}')

        # Add columns for each team
        round_summary.add_column("Red", style="red", no_wrap=True)
        round_summary.add_column("Blue", style="blue", no_wrap=True)

        # Populate the table
        for key in round:
            red, blue = key.split(', ')
            round_summary.add_row(f'{red} {EMOJI[round[key].red]}',
                                  f'{blue} {EMOJI[round[key].blue]}')
        print(round_summary)
        print('\n')

    # Print the score
    red_score, blue_score = match.score
    print(f'Red: {red_score}\n'
          f'Blue: {blue_score}')

    # Print the winner
    if red_score > blue_score:
        print('\n[red]Red victory! :grin:')
    elif red_score < blue_score:
        print('\n[blue]Blue victory! :grin:')
    else:
        print('\nDraw :expressionless:')



def play_game():

    color = client.recv(1024).decode()

    print("Waiting for both players to get ready ...")

    data = client.recv(4096)
    champions = pickle.loads(data)

    print(f'\nYou are team [{color}]{color.title()}[/{color}]')
    print('Pick your champions.\n')
    print_available_champs(champions)
    print('\n')

    selected_champs = []

    # Champion selection
    for _ in range(2):
        input_champion('Input', color, champions, selected_champs)
    
    selected_champs = ' '.join(selected_champs)
    
    print('\n')

    client.sendall(selected_champs.encode())

    data = client.recv(4096)
    match = pickle.loads(data)

    # Print a summary
    print_match_summary(match)


def view_history():

    history = client.recv(4096)
    history = pickle.loads(history)
    print(history)

    for match in history:
        match = unpickler.decode(match)
        print(match)

        #match = pickle.loads(match)    # Leads to error
        #print(match)
    
    main()


def create_champion():

    print('Input the champion name, then the probability for each result (int, from 0 - 100).\n')
    name = input('Name: ')
    rock_p = int(input('Rock probability: '))
    paper_p = int(input('Paper probability: '))
    scissors_p = 100 - (rock_p + paper_p)

    if rock_p + paper_p > 100:
        print('Probability total must not exceed 100')
        create_champion()
    
    print('New character created:\n')
    print(f'Name: {name}\nRock probability: {rock_p}\nPaper probability: {paper_p}\nScissors probability: {scissors_p}\n')

    client.sendall(f'{name} {rock_p} {paper_p} {scissors_p}'.encode())

    main()


def main():
    print('Please choose one of the following:\n'
          '1. PLAY GAME\n'
          '2. CREATE CHAMPION\n'
          '3. VIEW HISTORY\n')
    
    choice = input('Input: ')
    if choice == '1':
        client.sendall('1'.encode())
        play_game()
    elif choice == '2':
        client.sendall('2'.encode())
        create_champion()
    elif choice == '3':
        client.sendall('3'.encode())
        view_history()
    else:
        main()


if __name__ == '__main__':
    print('Welcome to [bold yellow]Team Network Tactics[/bold yellow]!\n')
    main()
