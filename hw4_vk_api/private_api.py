import urllib.request, json
import log_pass

def getChatUrl(offset,token):
    url = 'https://api.vk.com/method/messages.getHistory?chat_id=34&count=200&offset=' + str(offset) + '&access_token=' + token
    return url

def getChatInfoUrl(token):
    url = 'https://api.vk.com/method/messages.getChat?chat_id=34&access_token=' + token
    return url

def getJsonData(url): #читаем то, что отдает api
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    return data

def getParticipants(data):
    participants = data['response']['users']  # id участников
    return participants

def getMessagesCount(data):
    messages_count = data['response'][0]  # количество постов
    return messages_count

def writingCsvMessages(handler,message_id, len_text, author_id): #пишем в файл данные по сообщениям
    #print('message_id ' + str(message_id))
    #print('author_id ' + str(author_id))
    #print('len_text ' + str(len_text))
    handler.write('\n%s\t%s\t%s' % (str(message_id), len_text, str(author_id)))

def writingStatistics(handler, chat_statistics):  # пишем в файл статистику по количеству слов на человека
    for user_id in chat_statistics:
        #print('\nuser_id '+str(user_id))
        #print('\nword_count ' + str(chat_statistics[user_id]))
        handler.write('\n%s\t%s' % (str(user_id),str(chat_statistics[user_id])))

def main():
    csv_chat = open('chat.csv', 'w', encoding = 'utf-8')
    csv_chat.write("message_id\tmessage\tmessage_length\tauthor_id")
    csv_statistics = open('chat_statistics.csv', 'w', encoding='utf-8')
    csv_statistics.write("user_id\twords_count")
    token = log_pass.my_access_token
    url = getChatInfoUrl(token)
    participants = getParticipants(getJsonData(url))
    chat_statistics = {k:0 for k in participants} # k,v = id,count_of_words
    offset = 0
    url = getChatUrl(offset,token)
    messages_count = getMessagesCount( getJsonData(url))
    while offset < messages_count: #обходим все сообщения в чате шагом 200
        url = getChatUrl(offset,token)
        data = getJsonData(url)
        try:
            messages = data['response'][1:]
            for message in messages:
                message_id = message['mid']
                author_id = message['from_id']
                text = message['body'].replace('<br>',' ')
                len_text = len(text.split(' '))
                chat_statistics[author_id] += len_text
                if text: # пропускаем сообщения без текста
                    writingCsvMessages(csv_chat, message_id, len_text, author_id)
            offset += 200
        except:
            print('cannot get data from ' + url) #просто повторяем запрос, если не проходит с первого раза
    writingStatistics(csv_statistics,chat_statistics)
    csv_chat.close()
    csv_statistics.close()

if __name__ == '__main__':
        main()