import glob
import json

class Couple:

    def __init__(self, boy, girl):
        self.boy = boy
        self.girl = girl

    def __str__(self):
        return str(self.boy) + '/' + str(self.girl)

    def from_string(self, couple_str):
        return Couple(*couple_str.split('/'))

    def contains(self, person):
        return self.boy == person or self.girl == person

def bayes_update(previous, matches, possible):
    # p(b|a) = p(b) * p(a) / p(a)
    # p(is match|data) = ((p(data|is match) * p(is match)) / p(data))
    # p(data) = 1 / possible
    # p(is match) = previous
    # p(data|is match) = 1 / matches
    # [1 0 0 0 0] p(data) = 1/5
    # [1 1 1 0 0] p(is match) = 3/5
    # p(data|is match) = 1/3
    # ((1/3) * (3/5)) / (1/5)
    # a = matches # n correct
    # b = possible - a # n incorrect
    # # domain θ
    # theta_range = np.linspace(0, 1, 1000)
    # # prior distribution P(θ)
    # prior = stats.beta.pdf(x = theta_range, a=a, b=b)

    # theta_range_e = theta_range + 0.001 
    # prior = stats.beta.cdf(x=theta_range_e, a=a, b=b) - stats.beta.cdf(x=theta_range, a=a, b=b) 
    # # prior = stats.beta.pdf(x = theta_range, a=a, b=b)
    # likelihood = stats.binom.pmf(k=matches, n=possible, p=theta_range) 
    # posterior = likelihood * prior # element-wise multiplication
    # normalized_posterior = posterior / np.sum(posterior)

    # return normalized_posterior
    likelihood = 1 / 9 # I'm saying that this was always set to be the outcome since this will be a constant

    posterior = (likelihood * previous) / (matches / possible)
    return posterior

def update_probs():
    with open('probabilities.json', 'r') as in_f:
        probs = json.load(in_f)

    with open('no_matches.json', 'r') as in_f:
        no_matches = set(json.load(in_f))

    with open('potentials.json', 'r') as in_f:
        pots = json.load(in_f)
    
    for couple in probs.keys():
        boy, girl = couple.split('/')
        probs[couple] = 1 / min([pots[boy], pots[girl]])

    weeks = glob.iglob('week*.json')
    for week in weeks:
        with open(week, 'r') as in_f:
            matchups = json.load(in_f)

        couples = [x for x in matchups['couples'] if x not in no_matches]
        matches = matchups['matches']

        for couple in couples:
            probs[couple] = bayes_update(probs[couple], matches, len(couples))

    with open('probabilities.json', 'w') as out_f:
        json.dump(probs, out_f)

if __name__ == '__main__':
    update_probs()
