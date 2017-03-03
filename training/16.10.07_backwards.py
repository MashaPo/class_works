# Полученное на вход слово возвращаем в обратном порядке
while True:
    word = input('напишите слово или "конец"\n')
    if word == 'конец':
        print('До свидания')
        break
    else:
        count = -1
        new_word = ''
        while count  > -len(word) - 1:
            new_word = new_word + word[count]
            count -= 1
        print(new_word)


    
