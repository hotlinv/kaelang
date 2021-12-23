
import jieba
 
def replaceSynonymWords(string1):
    # 1读取同义词表，并生成一个字典。
    combine_dict = {}
    # synonymWords.txt是同义词表，每行是一系列同义词，用tab分割
    for line in open("dict/同义词.txt", "r", encoding='utf-8'):
        seperate_word = line.strip().split()
        for i, word in enumerate(seperate_word):
            if i!=0:
                combine_dict[word] = seperate_word[0]
 
            # 2提升某些词的词频，使其能够被jieba识别出来
            if len(word)>1:
                jieba.suggest_freq(word, tune=True)
 
    # 3将语句切分成单词
    seg_list = list(jieba.cut(string1, cut_all=False))
    #print(seg_list)
 
    # 4返回同义词替换后的句子
    return "".join([combine_dict[word] if word in combine_dict else word for word in seg_list])
 
 
string1 = '创建一个图片，然后说：“开始运行命令了！”'
print(string1, "=>", replaceSynonymWords(string1))

