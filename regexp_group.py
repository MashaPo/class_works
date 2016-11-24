import re
regexp = '(б[аяиеэоуыё])'
f = open('1.txt','r',encoding = 'utf-8')
s = f.read()
words = s.split()
for word in words:
    if re.search(regexp,word):
        res = re.search(regexp,word)
        print(res.group(1))
