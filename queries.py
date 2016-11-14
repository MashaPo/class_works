f = open('queries.csv', 'w', encoding = 'utf-8')
#шапка
f.write('input' + '\t' + 'length' + '\t' + 'palindrom' + '\t' + 'verb' + '\n')

while True:
    inpt = input('Ваше слово: \n')
    if inpt == 'хватит':
        break
    else:
        lngth = len(inpt)
        count = 0
        backwards = ''
        palindr = 'no'
        verb = 'no'
        V_endings = ['ть', 'л', 'ла', 'ли', 'ло', 'ем', 'ю', 'шь', 'т', 'у', 'чь']
#проверяем, является ли палиндромом
        while count < lngth:
            backwards = inpt[count] + backwards
            count += 1
        if backwards == inpt:
            palindr = 'yes'
        for end in V_endings:
            if inpt.endswith(end):
                    verb = 'yes'
                    break
        f.write(inpt + '\t' + str(len(inpt))+ '\t' + palindr + '\t' + verb + '\n')
f.close()
