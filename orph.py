
inpt = input('введите слово\n')    
count = 0
word = ''
for letter in inpt:
    if count%2 == 0:
        word = word + 'Б'
        count += 1
    else:
        word += letter
        count += 1
print(word)
            
