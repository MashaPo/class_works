import sqlite3
import urllib.request, json
#from datetime import datetime

'''posts:
pid = post id (key)
text = post text
ccount = comments count
from_id = community id

comments:
cid = comment id(key),
text = comment text
pid = post id,
from_id = author id,
reply_to_cid = id of the comment our comment replies to

authors:
uid = user id (key),
bdate = date of birth,
city = city name
'''

def tablesCreation(cur):
    cur.execute('create table posts(pid INTEGER not null primary key, text VARCHAR(100), ccount INTEGER, from_id INTEGER)')
    cur.execute('create table comments(cid INTEGER not null primary key, text VARCHAR(100), pid INTEGER, from_id INTEGER, reply_to_cid INTEGER)')
    cur.execute('create table authors(uid INTEGER not null primary key, bdate VARCHAR(100), city VARCHAR(100))')

# выкачиваем все посты и комменты сообщества Образовач
def postUrlCreator(offset): #запрос для получения постов
    url = 'https://api.vk.com/method/wall.get?owner_id=-74404187&count=100&offset=' + str(offset)
    return url

def commentsUrlCreator(post_id, offset): #запрос для получения комментариев
    url = 'https://api.vk.com/method/wall.getComments?owner_id=-74404187&post_id='\
          + str(post_id) + '&count=100&offset=' + str(offset)
    return url

def UserUrlCreator(user_id): #запрос для получения информации о пользователе
    url = 'https://api.vk.com/method/users.get?fields=city,bdate&user_ids='+str(user_id)
    return url

def cityUrlGenerator(city_id): #запрос для получения названия города
    url = 'https://api.vk.com/method/database.getCitiesById?city_ids='+str(city_id)
    #print(url)
    return url

def getJsonData(url): #читаем то, что отдает api
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    return data

def getContent(data):
    content = data['response'][1:] # список постов или список комментариев
    return content

def getPostsCount(data):
    posts_count = data['response'][0]  # количество постов
    return posts_count

def getCityName(data):
    city_name = data['response'][0]['name']  # название города
    return city_name

def getUserInfo(data):
    try:
        city = data['response'][0]["city"]
        city_data=getJsonData(cityUrlGenerator(city))
        city_name = getCityName(city_data)
    except:
        #print("exception can't get city")
        city_name = 0
    try:
        bdate = data['response'][0]["bdate"]
        #bdate = datetime.strptime(bdate, "%d.%m.%Y") # отдает формат '8.3.1997'
        #age = int(((datetime.today() - bdate)).days/365) #количество полных лет
    except:
        #print("exeption can't get bdate")
        bdate = 0
    return(city_name,bdate)


def debugPosts(id,text):
    print(id)
    print(text)


def debugComments(id, text, author, city, bdate):
    print(id)
    print(text)
    print(author)
    print(city)
    print(bdate)


def main():
    con = sqlite3.connect('vk_db.db')
    cur = con.cursor()
    tablesCreation(cur)
    offset = 0
    url = postUrlCreator(offset)
    posts_count = getPostsCount( getJsonData(url))
    while offset < posts_count: #обходим все посты на стене шагом 100
        url = postUrlCreator(offset)
        posts = getContent(getJsonData(url))
        for post in posts:
            post_id = post['id']
            text = post['text'].replace('<br>',' ').replace('"', '""')
            comments_count = post['comments']['count']
            from_id = post['from_id']
            if text: # пропускаем посты без текста
                debugPosts( post_id, text)
                #заносим в таблицу инфу по посту
                req = 'insert into posts(pid, text, ccount, from_id) values(' \
                        + str(post_id) +', "' + text +'", ' + str(comments_count) + ', ' + str(from_id) + ')'
                #print(req)
                cur.execute(req)
                con.commit()
                if comments_count > 0: #сразу записываем комментарии, если есть
                    comm_offset = 0
                    while comm_offset < comments_count:
                        url = commentsUrlCreator(post_id, comm_offset)
                        comments = getContent(getJsonData(url))
                        for comment in comments:
                            comment_text = comment['text'].replace('<br>', ' ').replace('"', '""')
                            comment_id = comment['cid']
                            author_id = comment['uid']
                            try:
                                reply_to_cid = comment['reply_to_cid']
                            except:
                                reply_to_cid = 0
                            user_url =  UserUrlCreator(author_id)
                            city,bdate = getUserInfo(getJsonData( user_url))
                            #debugComments(comment_id, comment_text,author_id, city, bdate)
                            req = 'insert into comments(cid, text, pid, from_id, reply_to_cid) values (' + \
                                    str(comment_id) + ', "' + comment_text + '", ' + str(post_id) + \
                                    ', ' + str(author_id) +  ', ' + str(reply_to_cid) + ')'
                            cur.execute(req)
                            #print(req)
                            con.commit()
                            #авторы могут повторяться, проверяем, есть ли они уже
                            req = 'select uid from authors where uid=' + str(author_id)
                            #print(req)
                            cur.execute(req)
                            allready_author = cur.fetchall()
                            if not allready_author:
                                req = 'insert into authors(uid, bdate, city)values (' + \
                                        str(author_id) + ', "' + str(bdate) +  '", "' + str(city) + '")'
                                #print(req)
                                cur.execute(req)
                                con.commit()
                        comm_offset += 100
        offset += 100

    cur.execute('select * from posts limit 100')
    print(cur.fetchall())
    cur.execute('select * from comments limit 100')
    print(cur.fetchall())
    cur.execute('select * from authors limit 100')
    print(cur.fetchall())


if __name__ == '__main__':
        main()
