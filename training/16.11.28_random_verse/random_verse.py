import random

def open_dict(filename):
    words = open(filename,'r',encoding = 'utf-8')
    words = words.read()
    words = words.split()
    r = random.choice(words)
    return r

def sentence(noun1, verb, noun2, adverb):
    sent = noun1 + ' ' + verb + ' ' + noun2 + ' ' + adverb
    return sent

def randomsent():
    subj = open_dict('noun_nom.txt')
    predicate = open_dict('verb.txt')
    obj = open_dict('noun_acc.txt')
    adv = open_dict('adverb.txt')
    sent = sentence(subj, predicate, obj, adv)
    return sent
def main():
    for s in range(random.randint(4,8)):
        sentence = randomsent()
        print(sentence)



if __name__ == '__main__':
    main()
