import urllib.request, json
from datetime import datetime

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
    print(url)
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
        bdate = datetime.strptime(bdate, "%d.%m.%Y") # отдает формат '8.3.1997'
        age = int(((datetime.today() - bdate)).days/365) #количество полных лет
    except:
        #print("exeption can't get bdate")
        age = 0
    return(city_name,age)


def writingCsvPosts(handler,id,text): #пишем в файл данные по постам
    print(id)
    print(len(text.split(' ')))
    print(text)
    handler.write('\n%s\t%s' % (id, len(text.split(' '))))

def writingCsvComments(handler, id, text, author, city,  age): #пишем в файл данные пользователей
    print(id)
    print(len(text.split(' ')))
    print(text)
    print(city)
    print(age)
    handler.write('\n%s\t%s\t%s\t%s\t%s' % (id, len(text.split(' ')), author, str(city), str(age)))

def main():
    csv_posts = open('posts.csv', 'w', encoding = 'utf-8')
    csv_posts.write("post_id\tpost_length")
    csv_comments = open('comments.csv', 'w', encoding='utf-8')
    csv_comments.write("comment_id\tcomment_length\ttext\tauthor\tcity\tage")
    offset = 0
    url = postUrlCreator(offset)
    posts_count = getPostsCount( getJsonData(url))
    while offset < posts_count: #обходим все посты на стене шагом 100
        url = postUrlCreator(offset)
        posts = getContent(getJsonData(url))
        for post in posts:
            post_id = post['id']
            text = post['text'].replace('<br>',' ')
            comments_count = post['comments']['count']
            if text: # пропускаем посты без текста
                writingCsvPosts(csv_posts, post_id, text)
                if comments_count > 0: #сразу записываем комментарии, если есть
                    comm_offset = 0
                    while comm_offset < comments_count:
                        url = commentsUrlCreator(post_id, comm_offset)
                        comments = getContent(getJsonData(url))
                        for comment in comments:
                            comment_text = comment['text'].replace('<br>', ' ')
                            comment_id = comment['cid']
                            author_id = comment['uid']
                            user_url =  UserUrlCreator(author_id)
                            city,age = getUserInfo(getJsonData( user_url))
                            writingCsvComments(csv_comments, comment_id, comment_text,author_id, city, age)
                        comm_offset += 100
        offset += 100
    csv_posts.close()
    csv_comments.close()


def test():
    author_id = 46201202
    user_url = UserUrlCreator(author_id)
    city, age = getUserInfo(getJsonData(user_url))
    print(user_url)
    print(city)
    print(age)


if __name__ == '__main__':
        main()
