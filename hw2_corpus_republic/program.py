"""
https://republic.ru/posts/53486 - 1 июля
https://republic.ru/posts/78149 - 31 декабря
"""

import urllib.request
from bs4 import BeautifulSoup
import lxml.html
import os

#создаем url
def urlGenerator(postId):
    url = 'https://republic.ru/posts/' + str(postId)
    return(url)

#получаем html дерево, если статья не реклама и не оформление подписки(https://republic.ru/posts/53592)
def treeFromUrl(url):
    try:
        req = urllib.request.urlopen(url)
        html = req.read().decode('utf-8')
        if "content=\"article\"" not in html:
            tree = 'SPECIAL'
        else:
             tree = lxml.html.fromstring(html)
             label = tree.xpath('..//div[@class="post-label"]/text()')[0]
             if "На правах рекламы" in label:
                 tree = 'SPECIAL(ADVERTISEMENT)'
    except:
        tree = '404'
        html = ''
    return (html,tree)

#достаем заголовок и дату
def Meta(tree):
    title = tree.xpath('..//meta[@property="og:title"]')[0].get('content')
    try:
        label = tree.xpath('..//div[@class="post-label"]/a/text()')[0]
    except:
        label = ''
    try:
        author = tree.xpath('..//meta[@name="mediator_author"]')[0].get('content')
    except:
        author = ''
    # для даты отличаются теги, если это новости, и если это мнения
    if label == 'Новость':
        date = tree.xpath('.//div[@class="post-published"]/text()')[0]
    else:
        date = tree.xpath('.//div[@class="post-authors__published"]/text()')[-1]
    date = date.strip('\t\n').replace('/ха0', ' ').replace('&nbsp;', ' ')
        #print("\n%s,%s,%s,%s" % (author,date,label,title))
    return(author,date,label,title)

#пишем мета-информацию в таблицу
def writingToTable(table,filename,author,date,label,title,url,wordcount):
    table.write("\n%s\t%s\t%s\t%s\tRepublic\t%s\t%s\t%s" % (filename,author,date,label,title,url,wordcount))

#достаем текст BeautifulSoup'ом
def getText(html):
    soup = BeautifulSoup(html, 'lxml')
    textbranch = soup.find(name='div', attrs={"post-content js-mediator-article"})
    text = textbranch.text.strip('\n')
    wordcount = text.count(' ')
    return(text,wordcount)

#парсим дату для распределения по директориям
def filenameGenerator(date,id):
    date = date.split(' ')
    months = 'января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split(' ')
    if not date[1].endswith(','):
        month, year = date[1], date[2][:4]
    else:
        month = date[1][:-1]
        year = '2017'
    month = months.index(month) + 1
    filename = 'corpus/%s/%s/%s.txt' % (year, month, id)
    return(filename)

#пишем файлы
def addToCorpus(text,filename):
    #создает директории, если таких еще нет
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w",encoding = 'utf-8') as f:
        f.write(text)

def main():
    table = open('meta.csv', 'w', encoding='utf-8')
    table.write("path\tauthor\tdate\tlabel\tsource\ttitle\turl\twordcount")
    for id in range(53486,78150):
        url = urlGenerator(id)
        html,tree = treeFromUrl(url)
        if tree not in ('404','SPECIAL','SPECIAL(ADVERTISEMENT)'):
            author,date,label,title = Meta(tree)
            text,wordcount = getText(html)
            filename = filenameGenerator(date,id)
            addToCorpus(text, filename)
            writingToTable(table,filename,author,date,label,title,url,wordcount)

    table.close()
    
if __name__ == '__main__':
    main()
