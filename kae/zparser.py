import jieba, sys
import jieba.posseg as pseg

from kae.model import *
from kae.tinygraph import *

if __name__=="__main__":
    name = sys.argv[1]
    seg_list = pseg.cut(" ".join(sys.argv[2:]))
    words = []
    for word, flag in seg_list:
        words.append(Word(name=word, wordclass=flag))
    s = Sentence(name=name, parts=words)
    print("结果: ", f"{s}")  
