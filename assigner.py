import pandas as pd
import numpy as np
import json
import os
from datetime import datetime as dt
from itertools import permutations
from progressbar import ProgressBar

current_year = dt.now().year

if os.path.isfile("probabilities.json"):
    with open('probabilities.json', 'r') as in_f:
        probabilities = json.load()

start_time = dt.now()
# TODO: create algorithm for selecting optimal assignments for this year
penalties = {
    "PAST_YEAR": np.inf,
    "COUPLE": np.inf,
    "SELF": np.inf,
    "GIFT_EXCHANGE": 10,
    "GIVE_BACK": 5,
}

discounts = {
    "SPECIAL_2020": -10
}

all_siblings = [
    "Zac",
    "Lyd",
    "Nic",
    "TC",
    "Em",
    "Crystal",
    "Jon",
    "Jake",
    "Steph",
    "Katherine"
]



couples = {
    "Zac": "Lyd",
    "Lyd": "Zac",
    "TC": "Em",
    "Em": "TC",
    "Nic": "Katherine",
    "Katherine": "Nic",
    "Crystal": "Jon",
    "Jon": "Crystal",
    "Steph": "Jake",
    "Jake": "Steph"
}

possible_assignments = {
    giver: [recipient for recipient in all_siblings \
        if giver != recipient and recipient not in past_ass[giver].values] \
    for giver in all_siblings
}


score_matrix = pd.DataFrame({
    giver: [0 for _ in all_siblings] \
        for giver in all_siblings
})

score_matrix.index = all_siblings

for giver in all_siblings:
    for recipient in all_siblings:
        score = 0
        if recipient in past_ass[giver].values:
            score += penalties['PAST_YEAR']
        if recipient == couples.get(giver):
            score += penalties['COUPLE']
        if giver == recipient:
            score += penalties['SELF']
        if giver == past_ass[recipient].values[-1]:
            score += penalties['GIVE_BACK']
        # if recipient == special_2020.get(giver):
        #     score += discounts['SPECIAL_2020']
        score_matrix.loc[recipient, giver] = score


all_combos = list(permutations(all_siblings))
best_combo_ixs = []
best_score = np.inf

with ProgressBar(max_value=len(all_combos)) as bar:
    for ix, perm in enumerate(all_combos):
        score = 0
        for i, giver in enumerate(all_siblings):
            recipient = perm[i]
            score += score_matrix.loc[recipient, giver]
            rec_as_give_ix = all_siblings.index(recipient)
            if giver == perm[rec_as_give_ix]:
                score += penalties['GIFT_EXCHANGE']
        if score < best_score:
            best_combo_ixs = [ix]
            best_score = score
        elif score == best_score:
            best_combo_ixs.append(ix)
        bar.update(ix)

print(f"Algo finished! Elapsed time: {dt.now() - start_time}")
print(f"Best score: {best_score}")

if len(best_combo_ixs) > 1:
    print(f"Found {len(best_combo_ixs)} optimal combos! Selecting one at random...")
    cur_ass = pd.DataFrame({'giver': all_siblings,
                            'recipient': all_combos[np.random.choice(best_combo_ixs)]})
    print(cur_ass)
else:
    print(f"Optimal combo found!")
    cur_ass = pd.DataFrame({'giver': all_siblings,
                            'recipient': all_combos[best_combo_ixs[0]]})
    print(cur_ass)

cur_ass.to_excel(f"christmas_assignments_{current_year}.xlsx")

this_year_ass = pd.Series(cur_ass['recipient'].values, index=cur_ass['giver'].values)
past_ass = past_ass.append(this_year_ass, ignore_index=True)

past_ass.to_pickle("past_ass.pkl")
