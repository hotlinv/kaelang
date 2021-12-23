
from ka import initDict, cutWords, replaceSynonymWords
 
 
string1 = '定义一个空列表名为“一行”。'
# initDict()
print(string1, "=>", " ".join(replaceSynonymWords(cutWords(string1))))

