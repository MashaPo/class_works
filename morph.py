#распознаем существительные
vocF = 'ая'
vocN = 'ое'
while True:
    inpt = input('введите слово или напишите "конец"\n')    
    if inpt == 'конец':
        print('конец - noun masc')
        break
    elif inpt.endswith('ость') or inpt.endswith('шь'):
        print('noun fem')
    else:
        for v in vocF:
            if inpt.endswith(v):
                print('noun fem')
                break
            else:
                for v in vocN:
                    if inpt.endswith(v):
                        print('noun N')
                        break
                    else:
                        print('noun M')
        continue
   
