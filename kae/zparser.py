import jieba, sys
import jieba.posseg as pseg

from kae.model import *
from kae.tinygraph import *

def cut(s):
    '''分词'''
    seg_list = pseg.cut(" ".join(sys.argv[2:]))
    words = []
    for word, flag in seg_list:
        words.append(Word(name=word, wordclass=flag))
    return words

def _match(sid, o, wl, i):
    sl = [li.tar for li in o.next if li.src==sid]
    for si in sl:
        s = di(si)
        # print("_", s, "->", wl[i])
            # _match(si, o, wl, i)
        if s.name.startswith("{") and s.name.endswith("}"):
            exec(f"o.{s.name[1:-1]}=wl[i].name")
        elif s.name != wl[i].name and s.wordclass!=wl[i].wordclass:
            return
        # _next = s.next
        # if _next is not None:
        _match(si, o, wl, i+1)
    

def match(ss, wl):
    '''匹配，找到最合适的句式'''
    for s in ss:
        # lines = s.next
        _match(None, s, wl, 0)
        if s.action is not None:
            return s

def understand(intes, sen):
    '''从句式对应意图'''
    for inte in intes:
        if inte.target==sen.target and inte.action==sen.action:
            return inte

if __name__=="__main__":
    ba = Word(name="把", wordclass="p")
    jiang = Word(name="将", wordclass="v")
    yu = Word(name="于", wordclass="v")
    tar = Word(name=r"{target}", wordclass="n")
    act = Word(name=r"{action}", wordclass="v")
    juz = Word(name=r"。", wordclass="x")
    ju = Word(name=r".", wordclass="x")
    gantanz = Word(name=r"！", wordclass="x")
    gantan = Word(name=r"!", wordclass="x")
    lins = []
    lins.append(NextRef(name="", src=id(ba), tar=id(tar)))
    lins.append(NextRef(name="", src=id(jiang), tar=id(tar)))
    lins.append(NextRef(name="", src=id(yu), tar=id(tar)))
    lins.append(NextRef(name="", src=id(tar), tar=id(act)))
    lins.append(NextRef(name="", src=id(act), tar=id(juz)))
    lins.append(NextRef(name="", src=id(act), tar=id(ju)))
    lins.append(NextRef(name="", src=id(act), tar=id(gantanz)))
    lins.append(NextRef(name="", src=id(act), tar=id(gantan)))
    parts=[NextRef(name="", tar=id(ba)), NextRef(name="", tar=id(jiang)), NextRef(name="", tar=id(yu))]
    lins.extend(parts)
    s1 = Sentence(name="把(tar)(act)", next=lins)

    # for ref in lins:
    #     if ref.src is not None:
    #         w = di(ref.src)
        # if type(w)==list:
        #     w.

    i1 = Intention(name="打开空调", foo="openf", model="devs", target="空调", action="打开")

    # print(s1)

    name = sys.argv[1]
    words = cut(name)

    s = match([s1], words)
    # print(s)
    if s is not None:
        inte = understand([i1], s)
        # s = Sentence(name=name, parts=words)
        print("结果: ", f"{inte.model}.{inte.foo}()")
