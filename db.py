import json
import jsonpickle

from core import Champion


def add_champion(name, rock_p, paper_p, scissors_p):

    with open('db.json') as data:
        data = json.loads(data.read())
        character_dict = data['champions']

    character_dict.update({name: [rock_p, paper_p, scissors_p]})
    data['champions'] = character_dict

    with open('db.json', 'w') as outfile:
        json.dump(data, outfile)


def _parse_champ(name, stats) -> Champion:

    rock, paper, scissors = stats
    return Champion(name, float(rock), float(paper), float(scissors))


def get_champions() -> dict[str, Champion]:

    champions = {}

    with open('db.json') as data:
        champions = json.loads(data.read())['champions']
        for name, stats in champions.items():
            champ = _parse_champ(name, stats)
            champions[champ.name] = champ

    return champions


def add_to_history(match):

    with open('db.json') as data:
        data = json.loads(data.read())
        history = data['history']
    
    json_pickle = jsonpickle.encode(match, unpicklable=True)
    json_data = json.dumps(json_pickle, indent = 4)

    history.append(json_data)
    data['history'] = history
    
    with open('db.json', 'w') as outfile:
        json.dump(data, outfile)


def get_history():

    with open('db.json') as data:
        history = json.loads(data.read())['history']

    return history