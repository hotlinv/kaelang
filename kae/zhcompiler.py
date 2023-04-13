import jieba, sys
import jieba.posseg as pseg

from kae.model import *
from kae.tinygraph import *

def cut(s):
    '''分词'''
    seg_list = pseg.cut(s)
    words = []
    for word, flag in seg_list:
        words.append(Word(name=word, wordclass=flag))
    return words

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
        if s["name"].startswith("{") and s["name"].endswith("}") and wl[i].wordclass in s["wordclass"]:
            exec(f"o['{s['name'][1:-1]}']=wl[i].name")
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
            inte["args"] = sen["args"]
            return inte

def iscomment(words):
    if words[0].name=="说明" and words[1].name=="：" or words[1].name==":":
        return True
    return False

def compile(name=" ".join(sys.argv[1:])):
    # name = " ".join(sys.argv[1:])
    words = cut(name)
    res = {"input":name}
    if iscomment(words):
        res["errno"] = 0
        res["exec"] = f"# {name}"
        return res

    g = Graph("kae.db")
    ss = g.query(Sentence)

    s = match(ss, words, g)
    
    # print(s)
    if s is not None:
        intes = g.query(Intention)
        inte = understand(intes, s)
        if inte is not None:
            # s = Sentence(name=name, parts=words)
            res["errno"] = 0
            res["exec"] = f"{inte['model']}.{inte['foo']}({'' if 'args' not in inte else inte['args']})"
            print("运行语句: ", res["exec"])
        else:
            res["errno"] = 2
            print("我懂，但我不懂怎么做：", name)
    else:
        res["errno"] = 1
        print("看看你在说什么:", name)
    return res

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
