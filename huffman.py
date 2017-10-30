from collections import Counter
from math import log
text = 'Статьёй называют озаглавленный связный текст из основного пространства имён, содержание которого отражает одно значение его заголовка.'
ctr = Counter(text)
p_dic = {}
for w in ctr:
    p_dic[w] = ctr[w]/len(text)
entropy = sum(- p_dic[w] * log(p_dic[w], 2) for w in ctr)
#huffman
text = 'The main namespace, article namespace, or mainspace is the namespace of Wikipedia that contains the encyclopedia proper—that is, where "live" Wikipedia articles reside, as opposed to Sandbox pages.'
ctr = dict(Counter(text))
import operator
ctr2 = sorted(ctr.items(), key=operator.itemgetter(1))
while len(ctr2) > 1:
    ctr2[1] = ((ctr2[0][0],ctr2[1][0]), ctr2[0][1] + ctr2[1][1] )
    ctr2 = ctr2[1:]
    ctr2 = [(a,b) for (a,b) in sorted(ctr2, key = lambda x: x[1])]
ctr2 = ctr2[0][0]
encod = {}
def one_or_zero(tpl, cod):
    for i,elem in enumerate(tpl):
        if type(elem) == str:
            encod[elem] = cod + str(i)
        else: one_or_zero(elem, cod + str(i))
one_or_zero(ctr2,'')
for w,t in ctr2:
    if type(w) == str:
        encode[w] 
encoder(text)