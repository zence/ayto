import json

with open('probabilities.json', 'r') as in_f:
    probs = json.load(in_f)

with open('potentials.json', 'r') as in_f:
    contestants = json.load(in_f)
with open('matches.json', 'r') as in_f:
    matches = json.load(in_f)

matched_boys = {x.split('/')[0] for x in matches}
matched_girls = {x.split('/')[1] for x in matches}
matched_individuals = {*matched_boys, *matched_girls}

boys = {x.split('/')[0] for x in probs.keys()}
girls = {x.split('/')[1] for x in probs.keys()}

contestants = {x for x in contestants.keys() if x not in matched_individuals}

week = input("Week: ")

week_data = {'couples': []}

answer = None
while answer != "Done":
    print("Remaining contestants:", ', '.join(contestants))
    boy = input("Boy: ")
    if boy not in boys:
        if boy in girls:
            girl = boy
            boy = input("That was a girl! Give me a boy next: ")
        else:
            print(f"{boy} not found in contestants list!!!")
            continue
    else:
        girl = input("Girl: ")
        if girl not in girls:
            print(f"{girl} not found in contestants list!!!")
            continue
    week_data['couples'].append(f'{boy}/{girl}')
    contestants.remove(boy)
    contestants.remove(girl)
    if not contestants:
        break

n_matches = input("Matches: ")
week_data['matches'] = int(n_matches)


with open(f'week{week}.json', 'w') as out_f:
    json.dump(week_data, out_f)