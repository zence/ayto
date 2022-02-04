import json
import util

def update_no_match(boy, girl):
    with open('probabilities.json', 'r') as in_f:
        probs = json.load(in_f)

    with open('potentials.json', 'r') as in_f:
        pots = json.load(in_f)

    with open('matches.json', 'r') as in_f:
        matches = set(json.load(in_f))

    with open('no_matches.json', 'r') as in_f:
        no_matches = set(json.load(in_f))


    couple = f'{boy}/{girl}'
    no_matches.add(couple)
    probs[couple] = 0.0
    if pots[boy] > 1:
        pots[boy] -= 1
    if pots[girl] > 1:
        pots[girl] -= 1

    matched_boys = {x.split('/')[0] for x in matches}
    matched_girls = {x.split('/')[1] for x in matches}

    boys = {x.split('/')[0] for x in probs.keys()} - matched_boys
    girls = {x.split('/')[1] for x in probs.keys()} - matched_girls

    if girl not in matched_girls:
        for cur_boy in boys:
            if cur_boy != boy:
                n_possib = pots[girl]
                probs[f"{cur_boy}/{girl}"] = 1 / n_possib
                print(f"{cur_boy}/{girl}", probs[f"{cur_boy}/{girl}"])
    
    if boy not in matched_boys:
        for cur_girl in girls:
            if cur_girl != girl:
                n_possib = pots[boy]
                probs[f"{boy}/{cur_girl}"] = 1 / n_possib

    # for person in pots.keys():
    #     if boy != person:
    #         n_possib = pots[boy]
    #         cur_couple = f"{boy}/{person}"
    #         probs[str(cur_couple)] = 1 / n_possib
    #     elif girl == person:
    #         n_possib = pots[girl]
    #         cur_couple = f"{person}/{girl}"
    #         probs[str(cur_couple)] = 1 / n_possib

    with open('potentials.json', 'w') as out_f:
        json.dump(pots, out_f)

    with open('probabilities.json', 'w') as out_f:
        json.dump(probs, out_f)

    with open('no_matches.json', 'w') as out_f:
        json.dump(list(no_matches), out_f)

def update_all():
    with open('no_matches.json', 'r') as in_f:
        no_matches = json.load(in_f)

    for no_match in no_matches:
        update_no_match(*no_match.split('/'))

if __name__ == '__main__':
    boy = input("boy: ")
    girl = input("girl: ")
