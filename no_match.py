import json
import util

with open('probabilities.json', 'r') as in_f:
    probs = json.load(in_f)

with open('potentials.json', 'r') as in_f:
    pots = json.load(in_f)

boy = input("boy: ")
girl = input("girl: ")

couple = util.Couple.from_string(f'{boy}/{girl}')
probs[str(couple)] = 0.0
pots[boy] -= 1
pots[girl] -= 1

for person in pots.keys():
    if couple.boy == person:
        n_possib = pots[couple.boy]
        cur_couple = util.Couple(couple.boy, person)
        probs[str(cur_couple)] = 1 / n_possib
        cur_couple.update_probs()
    elif couple.girl == person:
        n_possib = pots[couple.girl]
        cur_couple = util.Couple(person, couple.girl)
        probs[str(cur_couple)] = 1 / n_possib
        cur_couple.update_probs()
