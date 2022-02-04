import json
from nis import match
import util

def update_matches(boy, girl):
    with open('matches.json', 'r') as in_f:
        matches = set(json.load(in_f))


    couple = f"{boy}/{girl}"
    matches.add(couple)

    with open('matches.json', 'w') as out_f:
        json.dump(list(matches), out_f)

    with open('probabilities.json', 'r') as in_f:
        probs = json.load(in_f)

    with open('potentials.json', 'r') as in_f:
        pots = json.load(in_f)

    probs[couple] = 1.0
    pots[boy] = 1
    pots[girl] = 1

    for person in pots.keys():
        if boy != person and girl != person:
            pots[person] -= 1

    for matchup in probs.keys():
        cur_boy, cur_girl = matchup.split('/')
        if cur_boy != boy and cur_girl != girl:
            probs[matchup] = 1 / min([pots[cur_boy], pots[cur_girl]])
            print(matchup, probs[matchup])
        elif cur_boy != boy or cur_girl != girl:
            probs[matchup] = 0.0
            print(matchup, probs[matchup])

    with open('potentials.json', 'w') as out_f:
        json.dump(pots, out_f)

    with open('probabilities.json', 'w') as out_f:
        json.dump(probs, out_f)

    with open("matches.json", 'w') as out_f:
        json.dump(list(matches), out_f)

def update_all():
    with open('matches.json', 'r') as in_f:
        matches = json.load(in_f)
    
    for match in matches:
        update_matches(*match.split('/'))

if __name__ == '__main__':
    boy = input("Boy: ")
    girl = input("Girl: ")

    update_matches(boy, girl)