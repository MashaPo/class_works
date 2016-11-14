import os
files = os.listdir('C:/Users/student/Desktop/py/texts')
f = open('words.csv', 'w', encoding = 'utf-8')
dl = '\t'
#пишем шапку
f.write('слово' + dl + 'частота' + dl  + 'сколько файлов' + '\n')
#создаем список и словари
#словарь k,v k - слово v - частота
dct_freq = {}
#словарь k,v k - слово v - имена файлов, где оно есть, списком
dct_files = {}

lst = []
#идем по файлам
for file in files:
    h = open('texts/' + file, 'r', encoding = 'utf-8')
    for line in h:
        line = line.split()
        for word in line:
            word = word.lower().strip('.!,?;:()-12334567890"|][«»\'')
#считаем слова и складываем в словарь
            if word not in dct_freq:
                dct_freq[word] = 1
            else:
                dct_freq[word] += 1
            if word not in dct_files:
                dct_files[word] = [file]
            else:
                if file not in dct_files[word]:
                    dct_files[word] = [file]
                else:
                    dct_files[word].append(file)
for word in sorted(dct_freq):
    f.write(word + dl + str(dct_freq[word]) + dl + str(len(dct_files[word])) + '\n')
