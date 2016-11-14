
f = open('queries.txt', 'w', encoding = 'utf-8')
while True:
    inpt = input('Ваше слово: \n')
    if inpt == 'хватит':
        break
    else: f.write(inpt + '\n')
f.close()


