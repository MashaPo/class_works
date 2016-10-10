'''f = open('C:/Users/student/Desktop/2.txt','r', encoding = 'utf-8')
line_number = 0

for line in f:
    print(len(line))
    line_number += 1
    if line_number%3 == 0:
        print(line)
f.close()'''
#для каждой строки кол-во символов, выводим каждую третью на экран
f = open('C:/Users/student/Desktop/2.txt','r', encoding = 'utf-8')

a = f.readlines()
f.close()
b = a[::3]
for line in a:
    print(len(line))
for line in b:
    print(line)
