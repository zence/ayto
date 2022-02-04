import pandas as pd
import numpy as np
import json
import os
from datetime import datetime as dt
from itertools import permutations, product
from progressbar import ProgressBar

with open('probabilities.json', 'r') as in_f:
    probs = json.load(in_f)

with open('matches.json', 'r') as in_f:
    matches = json.load(in_f)

matched_boys = {x.split('/')[0] for x in matches}
matched_girls = {x.split('/')[1] for x in matches}

boys = list({x.split('/')[0] for x in probs.keys()} - matched_boys)
girls = list({x.split('/')[1] for x in probs.keys()} - matched_girls)

best_matches = {}

score_matrix = pd.DataFrame({
    boy: [0 for _ in boys] \
        for boy in boys
})

score_matrix.index = girls
all_combos = []

for boy in boys:
    for girl in girls:
        score_matrix.loc[girl, boy] = probs[f"{boy}/{girl}"]


all_combos = list(permutations(boys, len(girls)))
best_combo_ixs = []
best_score = np.inf

with ProgressBar(max_value=len(all_combos)) as bar:
    for ix, perm in enumerate(all_combos):
        zipped = zip(perm, girls)
        score = 0
        for boy, girl in zipped:
            score += score_matrix.loc[girl, boy]

        if score < best_score:
            best_combo_ixs = [ix]
            best_score = score
        elif score == best_score:
            best_combo_ixs.append(ix)
        bar.update(ix)

if len(best_combo_ixs) > 1:
    print(f"Found {len(best_combo_ixs)} optimal combos! Selecting one at random...")
    cur_ass = pd.DataFrame({'boy': boys,
                            'girl': all_combos[np.random.choice(best_combo_ixs)]})
    print(cur_ass)
else:
    print(f"Optimal combo found!")
    cur_ass = pd.DataFrame({'boy': boys,
                            'girl': all_combos[best_combo_ixs[0]]})
    print(cur_ass)