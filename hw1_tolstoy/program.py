#загружаем текст тома для чтения, возвращаем токены
def ReadingFile (name):
    import re
    reg = "[<>\.\s,]"
    file = open(name, 'r', encoding = 'utf-8')
    text = file.read()
    words = re.split(reg, text)
    return words

#пишем в словарь пары омографов из файла
def OmographsList (name):
    file = open( name,'r', encoding = 'utf-8')
    dct = {}
    for line in file:
        try:
            dct[line[0]] = line[2]
        except:
            continue
    return dct

#является ли токен римской цифрой
def NumberXVII(word):
    import re
    if re.fullmatch('[XVICLMІХС]+', word) is not None:
        return True

#ищем ошибки и каждую исправляем
def FindingErrorsInText (words, omographsList):
    import re
    regex = '([A-Za-z][ІА-Яа-яіё]+)|([ІА-Яа-яіё]+[A-Za-z])'
    regex = re.compile(regex)
    dct_of_errors  = {}
    count =  0
    for word in words:
        count += 1
        if regex.search(word):
            if NumberXVII(word):
                replacement = ReplaceWithLatinic(word, omographsList)
                dct_of_errors[count] = [word, replacement]
            else:
                replacement = ReplaceWithCyrillic(word, omographsList)
                dct_of_errors[count] = [word, replacement]
    return dct_of_errors
    


#заменяем в ошибочном токене все, что сможем, на кириллицу
    
def ReplaceWithCyrillic (word, dct_of_omographs):
    import re
    new_word = ''
    for letter in word:
        try:
            new_word += dct_of_omographs[letter]
        except:
            new_word += letter
    return new_word

#заменяем в ошибочном токене все, что сможем, на латиницу(в 46 томе нужно только для римских цифр)
    
def ReplaceWithLatinic(word, dct_of_omographs):
    import re
    new_word = ''
    for letter in word:
        try:
            for latinic in dct_of_omographs:
                if letter == dct_of_omographs[latinic]:
                    new_word += latinic
                    break
        except:
            new_word += letter
    return new_word

#пишем ошибку и замену в файл errors.tsv
def WritingErrorsDown (name, dct_of_errors):
    file = open( name, 'w', encoding = 'utf-8')
    file.write('token_number' + '\t' + 'error' + '\t' + 'replacement' + '\n')
    for error in sorted(dct_of_errors):
        file.write(str(error) + '\t' + dct_of_errors[error][0] + '\t' +  dct_of_errors[error][1] + '\n')
    file.close()

#помещаем результат в файл -corr

def main ():
    words = ReadingFile('Том 46.xhtml')
    omographsList = OmographsList('letters.tsv')
    dct_of_errors = FindingErrorsInText(words,omographsList)
    WritingErrorsDown('errors.tsv', dct_of_errors)
    
    
    
if __name__ == '__main__':
    main()
    
