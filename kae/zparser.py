import jieba, sys
import jieba.posseg as pseg

if __name__=="__main__":
    seg_list = pseg.cut(" ".join(sys.argv[1:]))
    print("结果: ", [f"{word} {flag}" for word, flag in seg_list])  
