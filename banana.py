#проверяем, что слово CVCVCV и все гласные одинаковые
word = input('give me a word\n')
word_list = list(word)
list1 = word_list[1::2]
list2 = word_list[::2]
still_banana = False
for c in list2:
    if c in 'aouei':
        print("1 you're not speaking banana language!")
        break
if list1[0] in 'aouei':
    for vocal in list1[1:]:
        if vocal == list1[0]:
            still_banana = True
        else:
            print("2 you're not speaking banana language!")
            break
else:
    print("3 you're not speaking banana language!")

if still_banana == True:
    print('This is banana')
        
