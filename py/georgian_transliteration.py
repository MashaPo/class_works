
#import os
#def main():
#    for root, dirs, files in os.walk('C:/Program Files'):
#        print(files)

#if __name__ == '__main__':


def reading_alpha(file):
    alpha = open(file,'r', encoding = "utf-8")
    ge_alpha = {}
    for pair in alpha:
        try:
            pair = pair.split(';')
            ge_alpha[pair[0]] = pair[1]
        except: continue
    alpha.close()
    return ge_alpha

def transliteration(source, target, alpha):
    ge_file =  open(source,'r', encoding = "utf-8")
    trans_file = open(target, 'w', encoding = "utf-8")   
    for line in ge_file:
        for word in line:
            chars = list(word)
            for char in chars:
                if char in alpha:
                    trans_file.write(alpha[char])
                else:
                    trans_file.write(char)
    trans_file.close()


def main():
    ge_alpha = reading_alpha('alpha.txt')
    transliteration('wiki.txt','trans.txt', ge_alpha)


if __name__ == '__main__':
    main()
