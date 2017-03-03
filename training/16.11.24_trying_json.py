
#как прочитать json:
#read = open('date.json')
#json = json.load(read)
import re
import os
import json

final_json ={}
#здесь будут все слова a|b|c|d
#final_json['common'] = []
#здесь будет список текстов и их уникальных слов
texts = {}

regexp = '[А-ЯЁа-яё]+'

files = os.listdir('C:/Users/student/Desktop/py/texts')
for file in files:
    f = open('texts/' + file, 'r', encoding = 'utf-8')
    s = f.read()
    cyr_words = re.findall(regexp,s)
    cyr_words = set(cyr_words)
    texts[file] = list(cyr_words)
    print(len(texts))

f = open('1.json', 'w',  encoding = 'utf-8')
#записываем json на диск. в файл f
json.dump(texts, f, indent = 2, ensure_ascii = False)


#import json
#f = open(1.json, 'w',  encoding = 'utf-8')
#записываем json на диск. в файл f
#json.dump(d, f, indent = 2, ensure.ascii = False)
#f.close()

