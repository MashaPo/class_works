import os
from subprocess import call
#возвращает тройки вида директория-список папок-список файлов
dirs = os.walk('corpus')
for dir in dirs:
    #дублируем структуру в каталог morph_corpus
    new_dir = 'morph_' + dir[0] + '/'
    os.makedirs(os.path.dirname(new_dir), exist_ok=True)
    files = dir[2]
    for file in files:
        input_file = dir[0] + '/' + file
        output_file = new_dir + file
        #команду передаем на консоль (указываем относительный путь, бинарник должен лежать в папке проекта)
        mystem_call = 'mystem.exe -id %s %s' % (input_file,output_file)
        call(mystem_call)
