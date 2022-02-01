import util
import json

contestants = {
    'boy': [],
    'girl': []
}
answer = ''

# while answer != 'Done':
#     while answer == '':
#         answer = input("Name: ")
#         if answer == 'Done':
#             break

#     name = answer
#     while answer != 'boy' and answer != 'girl':
#         answer = input("Gender[boy/girl]: ")
#         if answer == 'Done':
#             break
    
#     gender = answer

#     contestants[gender].append(name)

#     print(name, "added!")
#     print("Number of boys:", len(contestants['boy']))
#     print("Number of girls:", len(contestants['girl']))
#     print("boys:", ', '.join(contestants['boy']))
#     print("girls:", ', '.join(contestants['girl']))
#     print("*\n" * 5)

#     answer = ''
contestants['boy'] = [
    'Zak',
    'Tevin',
    'Kwasi',
    'Brett',
    'Tomas',
    'Cam',
    'Andrew',
    'Moe',
    'Daniel',
    'Lewis',
    'Shamoy'
]
contestants['girl'] = [
    'Kenya',
    'Bria',
    'Jasmine',
    'Asia',
    'Cali',
    'Kayla',
    'Lauren',
    'Morgan',
    'Maria',
    'Nutsa',
    'Samantha'
]

if len(contestants['boy']) != len(contestants['girl']):
    print("Oopsies! There are", len(contestants['boy']), "guys and", len(contestants['girl']), "gals. Try again!")
    raise ValueError()

probabilities = {}

for boy in contestants['boy']:
    for girl in contestants['girl']:
        couple = util.Couple(boy, girl)
        probabilities[str(couple)] = 1 / len(contestants['boy'])

with open('probabilities.json', 'w') as out_f:
    json.dump(probabilities, out_f)

potentials = {}
for boy in contestants['boy']:
    potentials[boy] = len(contestants['girl'])
for girl in contestants['girl']:
    potentials[girl] = len(contestants['boy'])

with open('potentials.json', 'w') as out_f:
    json.dump(potentials, out_f)
# Zak, Tevin, Kwasi, Brett, Tomas, Cam, Andrew, Moe, Daniel, Lewis, Shamoy
# Kenya, Bria, Jasmine, Asia, Cali, Kayla, Lauren, Morgan, Maria, Nutsa, Samantha
