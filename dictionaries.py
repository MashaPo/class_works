#частотный словарь
f = open('C:/Users/student/Desktop/2.txt', 'r', encoding = 'utf-8')
dct = {}
lst = []
for line in f:
    line = line.split()
    for word in line:
        word = word.lower().strip('.!,?;:()-')
        if word not in dct:
            dct[word] = 1
        else:
            dct[word] += 1
for word in sorted(dct):
    print(word, dct[word])



'''
for k in dct:
    lst.append((dct[k],k))

lst.sort()
for pair in lst:
    print(pair)
'''
