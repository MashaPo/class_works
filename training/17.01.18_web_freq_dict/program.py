


import urllib.request
import re

#находим подстраницы,создаем список концов строк типа /posts/78441 
def FindingUrls(home):
    html = OpenUrl(home)
    urls = []
    reg = '<a href="(/posts/[0-9]*)" target="_self"'
    urls = re.findall(reg, html)
    urls = UrlMaker(home, urls)
    print(urls)
    print(len(urls))
    return(urls)
    
#клеим концы к началу  
def UrlMaker(home, substr):
    urls = []
    for s in substr:
        s = home + s
        urls.append(s)
    return urls

#находим текст страницы
def OpenUrl(url):
    resp = urllib.request.urlopen(url)
    html = resp.read()
    html = html.decode("utf-8")
    return html

#coздаем файл для частотного словаря
def FreqFile(name, dct_freq):
    f = open(name, 'w', encoding = 'utf-8')
    dl = '\t'
    #пишем шапку
    f.write('слово' + dl + 'частота' + dl)
    for word in sorted(dct_freq):
        f.write(word + dl + str(dct_freq[word]) + dl + '\n')
    
#словарь k,v k - слово v - частота
def Dct_Freq(r_texts):
    dct_freq = {}
    for text in r_texts: 
        for line in text:
                line = line.split()
                for word in line:
                    word = word.lower().strip('.!,?;:()-12334567890"|][«»\'')
        #считаем слова и складываем в словарь
                    if word not in dct_freq:
                        dct_freq[word] = 1
                    else:
                        dct_freq[word] += 1
    return dct_freq
                    
    
def main():
    urls = FindingUrls('https://republic.ru')
    texts = []
    for url in urls:
        texts.append(OpenUrl(url))
    FreqFile('republic_words.tsv', Dct_Freq(texts))


 

    
if __name__ == '__main__':
    main()
