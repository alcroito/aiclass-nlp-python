__author__ = 'Placinta'

from Models import Models

encrypted_string = "Esp qtcde nzyqpcpynp zy esp ezatn zq Lcetqtntlw Tyepwwtrpynp hld spwo le Olcexzfes Nzwwprp ty estd jplc".upper()
new_string = ''
count = len(encrypted_string)
possibilities = []
corp = Models()
corp.createWordUniGramModel()
for i in range(1,37):
    character_list = []
    new_string = ""
    for j in range(0, count):
        if encrypted_string[j] == ' ':
            character_list.append(' ')
        else:
            character_list.append(chr((ord(encrypted_string[j])-0x41 + i)%26+0x41))
    new_string = "".join(character_list).lower()
    possibilities.append(new_string)
    #print "{0}:".format(i)

max_prob = -10000
max_string = ''
for string in possibilities:
    probability = corp.getWordProbability(string)
    if probability > max_prob:
        max_prob = probability
        max_string = string
print max_string


# question is the first conference on the topic of artificial intelligence was held at dartmouth college in this year
# result is 1955