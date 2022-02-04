import json
import match
import no_match

with open('probabilities.json', 'r') as in_f:
    probs = json.load(in_f)

if len(probs.keys()) == 0:
    with open('week1.json', 'r') as in_f:
        probs = {x: 0 for x in json.load(in_f)['couples']}
print(probs)
pots = {}

boys = {x.split('/')[0] for x in probs.keys()}
girls = {x.split('/')[1] for x in probs.keys()}


for boy in boys:
    pots[boy] = len(girls)
    for girl in girls:
        pots[girl] = len(boys)
        probs[f"{boy}/{girl}"] = 1 / len(boys)

with open('probabilities.json', 'w') as out_f:
    json.dump(probs, out_f)

with open('potentials.json', 'w') as out_f:
    json.dump(pots, out_f)

match.update_all()
no_match.update_all()
