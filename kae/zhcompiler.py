import jieba, sys
import jieba.posseg as pseg

from kae.model import *
from kae.tinygraph import *

MAO = ":："
ENDSENT = ".。!！;；?？"
YH = '“”"'
KUOSTAR = '('
KUOEND = ')'
SHUSTAR = '《'
SHUEND = '》'
SPLIT = "、"

def prepareWordDict(g):
    '''修改词典'''
    dicts = g.getNodes("UserWord")
    for d in dicts:
        jieba.add_word(d["name"], 100, d["wordclass"])
    sdicts = g.getNodes("UserSpWord")
    for sd in sdicts:
        jieba.suggest_freq(sd["name"].split("/"), tune=True)

def cut(s):
    '''分词'''
    seg_list = pseg.cut(s)
    words = []
    for word, flag in seg_list:
        words.append(Word(name=word, wordclass=flag))
    return words

def replaceSame(gdb, words):
    # 同义词替代
    for word in words:
        sws = gdb.getNodes("SameWord", word.name)
        if len(sws)>0:
            word.name = sws[0]["sameas"] 

def delUseless(gdb, words):
    # 去除无用词
    uls = [ul["name"] for ul in gdb.getNodes("UselessWord")]
    dels = []
    for word in words:
        if word.name in uls:
            dels.append(word)
        elif word.wordclass=="y":
            dels.append(word)
    for dw in dels:
        words.remove(dw)

def parseSubSentence(gdb, words):
    # 切分子句
    maoidx = -1
    endidx = -1
    for idx, word in enumerate(words):
        if word.name in MAO:#找到冒号作为开始
            maoidx = idx
        if word.name in ENDSENT:#句子结束作为结束
            endidx = idx
            
    if maoidx != -1 and (endidx-maoidx)>2: #找到冒号
        sub = []
        for i in range(maoidx+1,endidx):
            w = words.pop(maoidx+1)
            if w.name not in SPLIT:
                sub.append(w)
        words.insert(maoidx+1, sub)


def _match(gdb, sid, o, wl, i):
    # print([di(li) for li in o.edges])
    sl = []
    for li in o["edges"]:
        edge = gdb.di(li)
        if edge["src"]==sid:
            sl.append((edge["tar"], edge["name"]))  
    # isok = 0
    if len(sl)==0:
        if i==len(wl):#寻到底了
            return True
    # print("_", sl, "->", wl[i])
    for si, st in sl:
        s = gdb.di(si)
            # _match(gdb, si, o, wl, i)
        if i>=len(wl):
            continue
        print(" +", s, "->", wl[i])
        if type(wl[i])!=list and s["name"].startswith("{") and s["name"].endswith("}") and wl[i].wordclass in s["wordclass"]:
            exec(f"o['{s['name'][1:-1]}']=wl[i].name")
        elif type(wl[i])==list and s["name"].startswith("{") and s["name"].endswith("}"):
            exec(f"o['{s['name'][1:-1]}']=wl[i]")
        elif s["name"] != wl[i].name or wl[i].wordclass not in s['wordclass'] : 
            print(" X", wl[i])
            continue
        
        # _next = s.next
        # if _next is not None:
        if _match(gdb, si, o, wl, i+1):
            # isok +=1
            return True
    return False #isok>0 or len(sl)==0
    

def match(ss, wl, gdb):
    '''匹配，找到最合适的句式'''
    for s in ss:
        # lines = s.next
        if _match(gdb, None, s, wl, 0) and s["action"] is not None:
            return s

def understand(intes, sen):
    '''从句式对应意图'''
    for inte in intes:
        if inte["target"]==sen["target"] and inte["action"]==sen["action"]:
            if type(sen["args"])!=list:
                inte["args"] = sen["args"]
            else:
                inte["args"] = [eval(w.name) for w in sen["args"]]
            return inte



def iscomment(words):
    '''判断是注释'''
    if words[0].name=="说明" and words[1].name in MAO:
        return True
    elif words[0].name=="【" and words[1].name=="注" and words[2].name=="】":
        return True
    return False



def splitSentence(paragraph):
    '''拆分句子（顺带划分整体语素：括弧，引号等）'''
    sents =[[]]
    words = cut(paragraph)
    yh = 0
    for word in words:
        if word.wordclass=="x" and word.name in YH:
            yh+=1
            if yh%2==0:
                sents[-1][-1].name = sents[-1][-1].name+'"' #收尾
                continue
            else:
                sents[-1].append(word) #开启
                sents[-1][-1].name='"'
                sents[-1][-1].wordclass="*"
                continue
        if yh%2==0:
            sents[-1].append(word)
        else:
            sents[-1][-1].name = sents[-1][-1].name+word.name #把分词后的字符串再拼一起
            continue
        if word.wordclass=="x" and word.name in ENDSENT:
            sents.append([])
    return sents[:-1]

remakeLine = lambda words: "".join([word.name for word in words])

ARGS = lambda args: args if type(args)!=list else str(args)[1:-1]

def compile(paragraph=" ".join(sys.argv[1:])):
    import kae, os
    dbf = os.path.join(os.path.split(os.path.split(kae.__file__)[0])[0], "kae.db")
    # print(kae.__file__) #需要考虑在某个特别目录下放db文件
    g = Graph(dbf)
    prepareWordDict(g)
    # name = " ".join(sys.argv[1:])
    # words = cut(name)
    sents = splitSentence(paragraph)
    
    ss = g.query(Sentence)
    ress = []
    mods = []
    for sent in sents:
        # print(sent)
        res = {"input":remakeLine(sent)}
        if iscomment(sent): #判断是否是注释
            res["errno"] = 0
            res["exec"] = "# "
            ress.append(res)
            continue

        replaceSame(g, sent) #替换同义词
        delUseless(g, sent) #去除无用词

        parseSubSentence(g, sent)

        s = match(ss, sent, g)
        
        # print(s)
        if s is not None:
            intes = g.query(Intention)
            inte = understand(intes, s)
            if inte is not None:
                # s = Sentence(name=name, parts=sent)
                res["errno"] = 0
                res["exec"] = f"{inte['model']}.{inte['foo']}({'' if 'args' not in inte else ARGS(inte['args'])})"
                if inte['model'] not in mods:
                    mods.append(inte['model'])
                print("运行语句: ", res["exec"])
            else:
                res["errno"] = 2
                print("我懂，但我不懂怎么做：", remakeLine(sent))
        else:
            res["errno"] = 1
            print("看看你在说什么:", remakeLine(sent))
        ress.append(res)
    for mod in mods:
        ress.insert(0, {"input":"", "errno": 0, "exec": f"import {mod}"})
    return ress

if __name__=="__main__":
    # ba = Word(name="把", wordclass="p")
    # jiang = Word(name="将", wordclass="p")
    # tar = Word(name=r"{target}", wordclass="n")
    # act = Word(name=r"{action}", wordclass="v")
    # juz = Word(name=r"。", wordclass="x")
    # ju = Word(name=r".", wordclass="x")
    # gantanz = Word(name=r"！", wordclass="x")
    # gantan = Word(name=r"!", wordclass="x")

    # batar = NextRef(name="", src=id(ba), tar=id(tar))
    # jiangtar = NextRef(name="", src=id(jiang), tar=id(tar))
    # taract = NextRef(name="", src=id(tar), tar=id(act))
    # actjuz = NextRef(name="", src=id(act), tar=id(juz))
    # actju = NextRef(name="", src=id(act), tar=id(ju))
    # actgantanz = NextRef(name="", src=id(act), tar=id(gantanz))
    # actgantan = NextRef(name="", src=id(act), tar=id(gantan))
    # _ba = NextRef(name="", tar=id(ba))
    # _jiang = NextRef(name="", tar=id(jiang))
    # lins=[id(batar),id(jiangtar),id(taract), id(actjuz), id(actju), id(actgantanz), id(actgantan), id(_ba), id(_jiang)]

    
    # _act = NextRef(name="", tar=id(act))
    # acttar = NextRef(name="", src=id(act), tar=id(tar))
    # tarjuz = NextRef(name="", src=id(tar), tar=id(juz))
    # tarju = NextRef(name="", src=id(tar), tar=id(ju))
    # lins2 = [id(_act), id(acttar), id(tarjuz), id(tarju)]

    # ss = []
    # ss.append(Sentence(name="把(tar)(act)", edges=lins))
    # ss.append(Sentence(name="(act)(tar)", edges=lins2))

    # for ref in lins:
    #     if ref.src is not None:
    #         w = di(ref.src)
        # if type(w)==list:
        #     w.

    # intes = []
    # intes.append(Intention(name="打开空调", foo="openf", model="devs", target="空调", action="打开"))
    # intes.append(Intention(name="打开图像", foo="open", model="img", target="图像", action="打开"))
    # intes.append(Intention(name="旋转图像", foo="ra", model="img", target="图像", action="旋转"))

    # print(s1)

    compile()
