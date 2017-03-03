"""https://republic.ru 07.15 - 12.16
папки -  года,папки - месяца. метатаблица по файлам:заглавие дата автор,
количество слов,    5 млн токенов за год
a - сбор текстов, б - извлечение мета инфы, в  -разметка майстемом
https://republic.ru/posts/53486 - 1 июля
https://republic.ru/posts/78149 - 31 декабря


meta property="og:url"
meta property="og:title"
"""


import urllib.request
from bs4 import BeautifulSoup
import lxml.html
import os

def urlGenerator(postId):
    url = 'https://republic.ru/posts/' + str(postId)
    return(url)


#получаем html дерево
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
    # https://republic.ru/posts/53592 - подписка
    '''subscription = tree.xpath('.//div[@class="subscription"]/text()')
    if len(subscription) > 0:
        author, date, label, title = "SUBSCRIPTION", "", "", ""
    # https://republic.ru/posts/53625 спецпроект
    elif tree.xpath('..//meta[@property="og:url"]')[0].get('content') != url:
        author, date, label, title = "SPECIAL", "", "", ""
    else:'''
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

def getText(html):
    soup = BeautifulSoup(html, 'lxml')
    textbranch = soup.find(name='div', attrs={"post-content js-mediator-article"})
    text = textbranch.text.strip('\n')
    wordcount = text.count(' ')
    return(text,wordcount)

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

def addToCorpus(text,filename):
    #print(text)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w",encoding = 'utf-8') as f:
        f.write(text)

def main():
    table = open('meta.csv', 'a', encoding='utf-8')
    #table.write("path\tauthor\tdate\tlabel\tsource\ttitle\turl\twordcount")
    for id in range(78150,78151):
        url = urlGenerator(id)
        html,tree = treeFromUrl(url)
        if tree not in ('404','SPECIAL','SPECIAL(ADVERTISEMENT)'):
            author,date,label,title = Meta(tree)
            text,wordcount = getText(html)
            filename = filenameGenerator(date,id)
            addToCorpus(text, filename)
        #else:
         #   author,date,label,title = tree, '', '', ''
            writingToTable(table,filename,author,date,label,title,url,wordcount)

    table.close()

    #for element in root.iter():
    #   print('tag: %s - yield: %s - text: %s' % (element.tag, element.text))
    
if __name__ == '__main__':
    main()
    
