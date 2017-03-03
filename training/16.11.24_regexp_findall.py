import re
regexp = '[аяиеэоуыё]'
f = open('1.txt','r',encoding = 'utf-8')
w = open('2.txt','w',encoding = 'utf-8')
w2 = open('3.txt','w',encoding = 'utf-8')
s = f.read()
words = s.split()
a = re.findall(regexp,s)
print(len(a))
print(len(words)) 

for word in words:
    s1 = re.sub('[аяиеэоуыё]','o', word)
    w.write(s1)
w.close()

for word in words:
    s2 = re.sub(([a-z]+) ([a-z]+)), r'\2 \1',s)
    w1.write(s2)
w1.close()


patt = re.compile('[а-яёА-ЯЁ]')
if patt.search(word):
    i += 1

print(i)
