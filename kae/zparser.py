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

def _match(sid, o, wl, i):
    sl = [li.tar for li in o.edges if li.src==sid]
    # isok = 0
    if len(sl)==0:
        if i==len(wl):#寻到底了
            return True
    # print("_", sl, "->", wl[i])
    for si in sl:
        s = di(si)
            # _match(si, o, wl, i)
        if i>=len(wl):
            continue
        print(" +", s, "->", wl[i])
        if s.name.startswith("{") and s.name.endswith("}") and s.wordclass==wl[i].wordclass:
            exec(f"o.{s.name[1:-1]}=wl[i].name")
        elif s.name != wl[i].name or s.wordclass!=wl[i].wordclass:
            print(" X", wl[i])
            continue
        
        # _next = s.next
        # if _next is not None:
        if _match(si, o, wl, i+1):
            # isok +=1
            return True
    return False #isok>0 or len(sl)==0
    

def match(ss, wl):
    '''匹配，找到最合适的句式'''
    for s in ss:
        # lines = s.next
        if _match(None, s, wl, 0) and s.action is not None:
            return s

def understand(intes, sen):
    '''从句式对应意图'''
    for inte in intes:
        if inte.target==sen.target and inte.action==sen.action:
            return inte

if __name__=="__main__":
    ba = Word(name="把", wordclass="p")
    jiang = Word(name="将", wordclass="p")
    tar = Word(name=r"{target}", wordclass="n")
    act = Word(name=r"{action}", wordclass="v")
    juz = Word(name=r"。", wordclass="x")
    ju = Word(name=r".", wordclass="x")
    gantanz = Word(name=r"！", wordclass="x")
    gantan = Word(name=r"!", wordclass="x")
    lins = []
    lins.append(NextRef(name="", src=id(ba), tar=id(tar)))
    lins.append(NextRef(name="", src=id(jiang), tar=id(tar)))
    lins.append(NextRef(name="", src=id(tar), tar=id(act)))
    lins.append(NextRef(name="", src=id(act), tar=id(juz)))
    lins.append(NextRef(name="", src=id(act), tar=id(ju)))
    lins.append(NextRef(name="", src=id(act), tar=id(gantanz)))
    lins.append(NextRef(name="", src=id(act), tar=id(gantan)))
    parts=[NextRef(name="", tar=id(ba)), NextRef(name="", tar=id(jiang))]
    lins.extend(parts)

    lins2 = []
    lins2.append(NextRef(name="", tar=id(act)))
    lins2.append(NextRef(name="", src=id(act), tar=id(tar)))
    lins2.append(NextRef(name="", src=id(tar), tar=id(juz)))
    lins2.append(NextRef(name="", src=id(tar), tar=id(ju)))

    ss = []
    ss.append(Sentence(name="把(tar)(act)", edges=lins))
    ss.append(Sentence(name="(act)(tar)", edges=lins2))

    # for ref in lins:
    #     if ref.src is not None:
    #         w = di(ref.src)
        # if type(w)==list:
        #     w.

    intes = []
    intes.append(Intention(name="打开空调", foo="openf", model="devs", target="空调", action="打开"))
    intes.append(Intention(name="打开图像", foo="open", model="img", target="图像", action="打开"))
    intes.append(Intention(name="旋转图像", foo="ra", model="img", target="图像", action="旋转"))

    # print(s1)

    name = " ".join(sys.argv[1:])
    words = cut(name)

    s = match(ss, words)
    # print(s)
    if s is not None:
        inte = understand(intes, s)
        if inte is not None:
            # s = Sentence(name=name, parts=words)
            print("结果: ", f"{inte.model}.{inte.foo}()")
        else:
            print("无法理解的语句：", name)
    else:
        print("无法解析的句式:", name)
