import jieba, sys
import jieba.posseg as pseg

import os, json, yaml, re
import copy

def ka_load_urlmaps():
    '''加载路径对应文件'''
    from kae import ka_mount, ka_fext
    if os.access("kappcnf.yml", os.F_OK):
        f = open("kappcnf.yml", 'r',encoding='utf-8')
    else:
        f = open("urlmap.yml", 'r',encoding='utf-8')
    y = yaml.load(f, Loader=yaml.FullLoader)
    ka_mount.update(y)
    #把路径加入分词中
    for k, val in y.items():
        if not k.endswith("处"):
            jieba.add_word(k, 100, "ns")
            if val:
                for sk, sv in val.items():
                    jieba.add_word(sk, 100, "ns")
        else:
            #把格式加入分词（用于路径收尾）
            for sk, sv in val.items():
                jieba.add_word(sk, 100, "nfs")
                ka_fext[sk] = sv

from kae.model import *
from kae.tinygraph import *

MAO = ":："
ENDSENT = ".。!！?？"
YH = '“”"'
KUOSTAR = '('
KUOEND = ')'
SHUSTAR = '《'
SHUEND = '》'
SPLIT = "、；;"

def prepareWordDict(g):
    '''修改词典'''
    dicts = g.getNodes("UserWord")
    for d in dicts:
        jieba.add_word(d["name"], 1000, d["wordclass"])
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

def joinPath(gdb, words): #把路径连成一整个
    paths = []
    finded = False
    # rens = re.compile(r".+")
    for word in words:
        if not finded and word.wordclass=="ns":
            finded = True
            paths.append([word])
        elif finded:
            paths[-1].append(word)
        if finded and word.wordclass=="nfs":
            finded = False
    for pa in paths:     
        path = ""
        for p in pa:
            path+=p.name
        if len(pa)>0:
            pa[0].name = path
            for p in pa[1:]:
                words.remove(p)
    

def replaceSame(gdb, words):
    # 同义词替代
    for word in words:
        sws = gdb.getNodes("SameWord", name=word.name)
        # print("s   ", sws)
        if len(sws)>0:
            word.name = sws[0]["sameas"] 

def replaceSameLst(gdb, words):
    # 同义词替代 适用于lcut
    for word in words:
        sws = gdb.getNodes("SameWord", name=word.word)
        if len(sws)>0:
            word.word = sws[0].sameas 

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


# def _matchExp(gdb, sid, o, wl, i):
#     '''匹配表达式'''
#     # print([di(li) for li in o.edges])
#     sl = []
#     for li in o["edges"]:
#         edge = gdb.di(li)
#         if edge["src"]==sid:
#             sl.append((edge["tar"], edge["name"]))  
#     # isok = 0
#     if len(sl)==0:
#         if i==len(wl):#结束了
#             return True
#     # print("_", sl, "->", wl[i])
#     for si, st in sl:
#         s = gdb.di(si)
#             # _match(gdb, si, o, wl, i)
#         if i>=len(wl):
#             continue
#         nowi = si
#         print(" +", s, "->", wl[i])
        
#         if type(wl[i])!=list and s["name"].startswith("{") and s["name"].endswith("}") and wl[i].wordclass in s["wordclass"]:
#             exec(f"o['{s['name'][1:-1]}']=wl[i].name")
#         elif type(wl[i])==list and s["name"].startswith("{") and s["name"].endswith("}"):
#             exec(f"o['{s['name'][1:-1]}']=wl[i]")
#         elif s["name"] != wl[i].name or wl[i].wordclass not in s['wordclass']: 
#             print(" X", wl[i])
#             continue
#         # el
        
#         # _next = s.next
#         # if _next is not None:
#         if _matchExp(gdb, nowi, o, wl, i+1):
#             # isok +=1
#             return True
#     return False #isok>0 or len(sl)==0

def _expre(regx, nowre, words, wi, begend, args):
    r = regx if nowre is None else nowre
    w = words[wi]
    print(wi, words, w , r["name"], r["wordclass"])
    if (r["name"][0]=="{" and r["name"][-1]=="}" and "expid" in w) \
        or ("expid" not in w and w.name==r["name"] and w.wordclass in r["wordclass"]) \
        or ("expid" not in w and r["name"][0]=="{" and r["name"][-1]=="}" and w.wordclass in r["wordclass"]) \
        :
        # 完全匹配
        print("匹配")
        if len(begend)==0 or len(begend[-1])==2:
            begend.append([wi])
            args.append({})
        if r["name"][0]=="{" and r["name"][-1]=="}":# 把关键信息塞进args去
            if type(w)!=dict:
                args[-1][r["name"][1:-1]]=w.name 
            else:
                args[-1][r["name"][1:-1]]=r"{{subexp}}"
        if "next" not in r:
            begend[-1].append(wi) #end
            
        if wi+1<len(words):
            if "next" in r:
                _expre(regx, r["next"], words, wi+1, begend, args)
            else:
                _expre(regx, None, words, wi+1, begend, args)
    else:
        # 不匹配，复位
        print("不匹配")
        nwi = wi
        if len(begend)>0 and len(begend[-1])==1:
            lastbe = begend.pop(-1)
            nwi = lastbe[0]
            args.pop(-1)
        if nwi+1<len(words):
            _expre(regx, None, words, nwi+1, begend, args)

def expre(gdb, regx, words):
    # 匹配表达式，如果找到匹配的，返回分割后的表达式，如果没找到匹配分割表，找到的就返回空
    exudek = ["edges", "type", "nodetype"]
    sl = []
    begend = []
    args = []
    _expre(regx["next"], None, words, 0, begend, args)
    print("*"*10, begend)
    if len(begend)>0 and len(begend[-1])==1: #去除不完整的匹配
        begend.pop(-1)
    
    laste = 0
    for idx, be in enumerate(begend):
        beg, end = be
        sl.extend(words[laste:beg])
        expinf = {k:v for k,v in gdb.di(regx["name"]).items() if k not in exudek}
        subexp = {"expid": regx["name"],"subexp":words[beg:end+1]}
        subexp.update(expinf)
        print(subexp)
        subexp.update(args[idx])
        sl.append(subexp)
        laste = end+1
    sl.extend(words[laste:])
    return sl if len(begend)>0 else None

def evalExpression(gdb, words):
    # 把子句转换成表达式
    print("eee"*10, words)
    if len(words)==1 and words[0].wordclass in "*m": #单纯字符串或数字
        return str(words[0].name)
    elif len(words)==1 and words[0].wordclass=="ns": # 纯路径
        return str(words[0].name)
    
    # if len(words)==4 and words[0].name=="公式" and words[-2].name=="的" and words[-1].name=="值": #表达式的值
    #     return {"type":"foo" ,"op":"eval", "val":words[1].name}
    # if len(words)==3 and words[-2].name=="的" and words[-1].name=="值": #变量的值
    #     return {"type":"foo" ,"op":"kae.libs.sys.getobj", "val":words[0].name}
    es = []
    exps = gdb.getNodes("Expression")
    # print("eee"*5, exps)
    for exp in exps:
        es.append({"name":exp.doc_id})
        lis = []
        for li in exp["edges"]:
            edge = gdb.di(li)
            srcid = edge["src"]
            tarid = edge["tar"]
            lis.append((srcid, tarid))
        # print(lis)
        nownode = es[-1]
        for link in lis:
            wd = gdb.di(link[1])
            node = {"name":wd["name"], "wordclass":wd["wordclass"]}
            nownode["next"] = node
            nownode = node
            # _makeexpress(gdb, es[-1], lis)

    print(es)
    res = words
    while True:
        count = 0
        for exp in es:
            reword = expre(gdb, exp, res)
            # print("reword!", reword)
            if reword is not None:
                res = reword
                count+=1
                break
        if count==0:
            break
    print(res)

    intes = gdb.query(Intention)
    result = _understandexp(intes, res[0])
    
    return result

argregex = r"{{(\w+)}}"

def _understandexp(intes, expm):
    res = {"type":"expression" ,"foo":""}
    print(intes, expm)
    intefs = [i for i in intes if i["action"]==expm["action"]]
    if len(intefs)>0:
        intef = intefs[0] #意图
        # print("i"*30, intef)
        
        res["foo"] = intef['foo'] 
        matches = re.findall(argregex, res["foo"])
        # print(matches)
        if len(matches)>0:
            for ma in matches:
                m2 = re.match(argregex, expm[ma])
                if m2 is not None: #需要嵌入下一级
                    res["foo"] = re.sub(r"{{("+ma+r")}}", lambda m: _understandexp(intes, expm["subexp"][0])["foo"], res["foo"])
                else:
                    # print("now", ma, res["foo"])
                    res["foo"] = intef["model"]+"."+re.sub(argregex, lambda m: expm[m.group()[2:-2]], res["foo"])
        print(res)
        return res
    

# def _makeexpress(gdb, es, sid):
#     # exps = gdb.getNodes("Expression", src=sid)
#     s = gdb.di(si)
        
#     _makeexpress(gdb, es, edge["tar"])
        # if edge["src"]==sid:
        #     es.append(edge)  

def parseSubSentence(gdb, words):
    # 切分子句
    maoidx = -1
    endidx = -1
    for idx, word in enumerate(words):
        if word.name in MAO:#找到冒号作为开始
            maoidx = idx
        if word.name in ENDSENT:#句子结束作为结束
            endidx = idx
            
    if maoidx != -1 : #找到冒号
        subs = []
        subi = maoidx+1
        sub = []
        for i in range(subi,endidx):
            w = words.pop(subi)
            if w.name not in SPLIT:
                sub.append(w)
            else:
                subs.append(sub)
                sub = []
        subs.append(sub)
        words.insert(subi, subs)


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
        else: #说明是逗号，还要继续解析下去
            o["__next"] = i
            print(","*40)
            return True
    # print("_", sl, "->", wl[i])
    for si, st in sl:
        s = gdb.di(si)
            # _match(gdb, si, o, wl, i)
        if i>=len(wl):
            continue
        nowi = si
        print(" +", s, "->", wl[i])
        if s["name"]==r"{args}":
            if type(wl[i])==list:
                # 如果已经是列表
                o["args"] = []
                for part in wl[i]:
                    o["args"].append(part)
            else:
                # 复杂内容延续直至结束。
                o["args"] = [[]]
                while i<len(wl):
                    if wl[i].name in ENDSENT+"，,":
                        # args 结束了。
                        if  wl[i].name in "，,":
                            o["__next"] = i+1
                        return True
                    elif wl[i].name in SPLIT:
                        o["args"].append([])
                    else:
                        # args 开启
                        o['args'][-1].append(wl[i])
                    i+=1
        if type(wl[i])!=list and s["name"].startswith("{") and s["name"].endswith("}") and wl[i].wordclass in s["wordclass"]:
            exec(f"o['{s['name'][1:-1]}']=wl[i].name")
        elif type(wl[i])==list and s["name"].startswith("{") and s["name"].endswith("}"):
            exec(f"o['{s['name'][1:-1]}']=wl[i]")
        elif wl[i].name in ENDSENT+"，,":
            # 结束了。
            if wl[i].name in "，,":
                o["__next"] = i+1
            return True
        elif s["name"] != wl[i].name or wl[i].wordclass not in s['wordclass']: 
            print(" X", wl[i])
            continue
        # el
        
        # _next = s.next
        # if _next is not None:
        if _match(gdb, nowi, o, wl, i+1):
            # isok +=1
            return True
    return False #isok>0 or len(sl)==0
    

def match(wl, gdb):
    '''匹配，找到最合适的句式'''
    session = []
    hasnext = True
    beg = 0
    while hasnext:
        ss = gdb.query(Sentence)
        if not hasnext:
            beg = 0
        hasnext = False
        for s in ss:
            # lines = s.next
            if _match(gdb, None, s, wl, beg) and s["action"] is not None: #找到匹配的语法了
                if "__next" in s: #还没结束
                    hasnext = True
                    beg = s["__next"]
                    del s["__next"]
                # print("U"*50, session)
                session.append(copy.deepcopy(s))
                break
    print("M"*50, session)
    return session

def understand(gdb, intes, session):
    '''从句式对应意图'''
    DEFARG = ["type", "nodetype", "name", "edges", "args"]
    runers = []
    for sen in session:
        print(sen)
        for inte in intes:
            # print(inte["action"], sen["action"], inte["target"]==sen["target"] if "target" in sen else True)
            if inte["action"]==sen["action"] and (inte["target"]==sen["target"] if "target" in sen else True):#带目标对象的最好目标对象也一致
                for key in sen.keys():
                    if key not in DEFARG:
                        inte[key] = sen[key]
                if "args" in sen and sen["args"] is not None:
                    if type(sen["args"])!=list:
                        # print("a"*10, sen["args"])
                        inte["args"] = sen["args"]
                    elif len(sen["args"])==1:
                        # print("b"*10, sen["args"])
                        inte["args"] = [evalExpression(gdb, sen["args"][0])]
                    else:
                        # print("c"*10, sen["args"])
                        inte["args"] = [evalExpression(gdb, w) for w in sen["args"]]
                runers.append(inte)
                break
    return runers




def iscomment(words):
    '''判断是注释'''
    if (words[0].name=="说明" or words[0].name=="声明") and words[1].name in MAO:
        return True
    elif words[0].name=="【" and words[1].name=="注" and words[2].name=="】":
        return True
    return False



def splitSentence(paragraph):
    '''拆分句子（顺带划分整体语素：括弧，引号等）'''
    sents =[[]]
    words = cut(paragraph)
    print("w"*100, words)
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
    print("!"*100, sents)
    return sents[:-1] if len(sents)>1 else sents

remakeLine = lambda words: "".join([word.name for word in words])

ARGS = lambda args: args if type(args)!=list else str(args)[1:-1]

def STR (args):
    if type(args)==list:
        if len(args)>1:
            return "*["+",".join([STR(a) for a in args])+"]"
        else:
            return STR(args[0])
    elif type(args)==dict:
        if "type" in args.keys() and args["type"]=="expression":#表达式
            return f"{args['foo']}"
        else:
            kvs = []
            for k in args.keys():
                kvs.append(fr"\'{k}\'={STR(args[k])}")
            return "{"+",".join([STR(a) for a in args])+"}"
    return  str(args)

def compile(paragraph=" ".join(sys.argv[1:])):
    import kae, os, re
    # initDict()
    ka_load_urlmaps()
    dbf = os.path.join(os.path.split(os.path.split(kae.__file__)[0])[0], "kae.db")
    # print(kae.__file__) #需要考虑在某个特别目录下放db文件
    g = Graph(dbf)
    prepareWordDict(g)
    # name = " ".join(sys.argv[1:])
    # words = cut(name)
    sents = splitSentence(paragraph)
    
    ress = []
    mods = ["kae.libs.sys"]
    for sent in sents:
        # print(sent)
        res = {"input":remakeLine(sent)}
        if iscomment(sent): #判断是否是注释
            res["errno"] = 0
            res["exec"] = "# "
            ress.append(res)
            continue

        joinPath(g, sent)
        replaceSame(g, sent) #替换同义词
        delUseless(g, sent) #去除无用词

        parseSubSentence(g, sent)

        s = match(sent, g)
        
        print("sessions:",":"*50 ,s)
        if s is not None and len(s)>0:
            intes = g.query(Intention)
            uintes = understand(g, intes, s)
            
            if len(uintes)>0:
                # s = Sentence(name=name, parts=sent)
                res["errno"] = 0
                regex = r"{{(\w+)}}"
                execs = []
                for inte in uintes:
                    foo = inte['foo'] #({'' if 'args' not in inte else ARGS(inte['args'])})
                    matches = re.findall(regex, foo)
                    if len(matches)>0:
                        fooexec = re.sub(regex, lambda m: STR(inte[m.group()[2:-2]]), foo)
                    else:
                        fooexec = foo
                    execs.append(f"{inte['model']}.{fooexec}")
                    if inte['model'] not in mods and inte['model']!="":
                        mods.append(inte['model'])
                res["exec"] = "".join(execs)
                print("运行语句: ", res["exec"])
            else:
                res["errno"] = 2
                print("我懂，但我不懂怎么做：", res["input"])
        else:
            res["errno"] = 1
            print("看看你在说什么:", res["input"])
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
