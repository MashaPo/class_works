#распознаем существительные в начальной форме (грубо). Для F и N задаем концы строк, M по остаточному признаку
F_endings = ['а', 'я', 'сть', 'шь']
N_endings = ['о', 'е']
while True:
    inpt = input('введите слово или напишите "конец"\n')    
    if inpt == 'конец':
        break

    else:
        found_it = False
        while found_it == False:
            for f in F_endings:
                if inpt.endswith(f):
                    print('noun F')
                    found_it = True
            for n in N_endings:
                if inpt.endswith(n):
                    print('noun N')
                    found_it = True
            if found_it == False:
                print('noun M')
                found_it = True
