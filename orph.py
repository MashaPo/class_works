#заменяем все четные на Б. абракадабра -> БбБаБаБаБрБ
inpt = input('введите слово\n')    
word = ''
for number,letter in enumerate(inpt):
    if number%2 == 0:
        word += 'Б'
    else:
        word += letter
print(word)
