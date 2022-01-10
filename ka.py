import glob
import inspect as ins
from pprint import pprint
import sys, re
import logging
import jieba
import functools

# 配置logging
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d - %(message)s',
    handlers=[
        #logging.FileHandler("ke.log", mode="a"),  # for logs write in file（mode：a为追加log，设置为w则表示每次清空，重新记录log）
        logging.StreamHandler()  # for print at console
    ]
)
jieba.setLogLevel(logging.INFO)

def catch2cn(fn):
    @functools.wraps(fn) #要加这句，不然inspect的get方法认不到函数，只能认到inner
    def inner(*args):
        try:
            return fn(*args)
        except Exception as e:
            fndoc = ins.getdoc(fn)
            err = u"{} 出错了：{}".format(fndoc.split()[0], str(e))
            #print(err)
            logging.error(err)
    return inner

def lastit(fn):#内部有产生新数据，会返回新数据名字。
    @functools.wraps(fn) #要加这句，不然inspect的get方法认不到函数，只能认到inner
    def inner(*args):
        newname = fn(*args)
        global ka_lastit
        ka_lastit = newname
        return newname
    return inner

ka_vals = {} #放变量
ka_sys = {} #放语言语法映射
res = []
ka_types = {} #放数据类型
ka_mount = {} #放数据目录
ka_outputs = {} #存放输出设备
ka_lastit = "" #它/他/她的指代
ka_callable_foos = {} #“把XXX执行XX”这样的句子自动对应的操作

ka_imp_fun_name = None

ka_custom_foos = []
 
# 1读取同义词表，并生成一个字典。
ka_combine_dict = {}
# 鸡肋词
ka_jl_words = []

# 初始化各种字典
def initDict():
    jieba.load_userdict(r"dict/分词词典.txt")
    for line in open(r"dict/同义词.txt", "r", encoding='utf-8'):
        seperate_word = line.strip().split()
        for i, word in enumerate(seperate_word):
            if i!=0:
                ka_combine_dict[word] = seperate_word[0]
 
            # 2提升同义词词典中的词的词频，使其能够被jieba识别出来
            if len(word)>1:
                jieba.suggest_freq(word, tune=True)
    for jlline in open(r"dict/鸡肋词.txt", "r", encoding='utf-8'):
        ka_jl_words.extend(jlline.strip().split())
        for i, jlword in enumerate(ka_jl_words):
            if len(jlword)>1:
                jieba.suggest_freq(jlword, tune=True)

initDict()

# 通过jieba分词
def cutWords(string1):
    # 3将语句切分成单词
    seg_list = list(jieba.cut(string1, cut_all=False))

    # 4将“”《》内容合并（不做分词）
    start = False
    seg_list2 = []
    for i, word in enumerate(seg_list):
        if (word == "“" or word == "《") and not start :
            start = True
            seg_list2.append([word])
            continue
        if (word == "”" or word == "》") and start:
            start = False
            seg_list2[-1].append(word)
            seg_list2[-1] = "".join(seg_list2[-1])
            continue
        if not start:
            seg_list2.append(word)
        else:#“”《》里面的内容
            seg_list2[-1].append(word)
    return seg_list2
 
def replaceSynonymWords(words):
    # 返回同义词替换后的句子
    words2 = [ka_combine_dict[word] if word in ka_combine_dict else word for word in words]
    return [w for w in words2 if w not in ka_jl_words]#去除鸡肋词

@catch2cn
def registType(typename, foo):
    """注册数据类型"""
    ka_types[typename]=foo

def ka_get_all_function_in_model():
    return ins.getmembers(sys.modules['__main__'], ins.isfunction)#拿到主模块下所有的函数

# 抽取callbable函数
def scan_callable():
    foos = ins.getmembers(sys.modules['__main__'], ins.isfunction)#拿到主模块下所有的函数
    #print(foos)
    for fn in [f for f in foos if f[0].startswith("ka")]:
        fndoc = ins.getdoc(fn[1])
        #print(fn, fndoc)
        if fndoc and "[k]" in fndoc:
            fnds = [d for d in fndoc.split() if "[k]" in d]
            for fnd in fnds:
                fnl = fnd.split("·")
                ka_callable_foos[fnl[0][3:]] = f"{fn[0]}({fnl[1]})"
        #    pass

ma_import = re.compile(u"^#\s*【引用】(.+)")
ma_code = re.compile(u"^#\s*【实现】")
ma_map = re.compile(u"^#\s*【映射】")
ma_next = re.compile(u"((?:如下|以下)(?:动作|操作)：)")
ma_sub = re.compile(u"^((?:\d|\.)+)）(.+)")
_ka_m_then = re.compile(u"^然后|最后")

_ka_m_deffoo = re.compile(u"怎么\s*(.+)\s*呢")
_ka_m_impfoo = re.compile(u"(?:由|让)(《.[^》]+》)来解释吧?")
_ka_m_runfoo = re.compile(u"用《(.[^》]+)》把《(.[^》]+)》的([^\s]+)设置为(.+)")

@catch2cn
def parsePk(kpf):
    """分析库文件"""
    lines = kpf.readlines()
    codes = []
    mapcodes = []
    now=None
    for line in lines:
        # print(line)
        if ma_import.match(line):
            imps = ma_import.findall(line)[0]
            for imp in imps.split("、"):
                impm = compile(f"import {imp}", kpf.name+" 导入{imp}", "exec")
                try:
                    exec(impm, globals())
                except:
                    raise Exception(f"{kpf.name}导入依赖库{imp}失败，请确认是否安装该库")
            continue
        elif ma_code.match(line):
            now="code"
            continue
        elif ma_map.match(line):
            now="map"
            continue
        if now=="code":
            codes.append(line)
        elif now=="map":
            mapcodes.append(line)

    mapcode = "\n".join(mapcodes)
    m = compile(mapcode, kpf.name, "exec")
    exec(m, globals())
    mup = compile("ka_sys.update(ka_pmap())", "kae", "exec")
    exec(mup, globals())

    code = "\n".join(codes)
    c = compile(code, kpf.name, "exec")
    exec(c, globals())

@catch2cn
def loadkps():
    """加载库目录下所有包文件(包括.kp和.kp.py)"""
    kps = glob.glob(r"./kalib/*.kp")
    kps.extend(glob.glob(r"./kalib/*.kp.py"))
    for kp in kps:
        #print(kp)
        with open(kp, "r", encoding='UTF-8') as kpf:
            parsePk(kpf)
    scan_callable()
    # print(ka_callable_foos)
loadkps()
for k,v in eval("ka_sys").items():
    res.append([re.compile(k), v])

ka_load_urlmaps()
# print(ka_mount)
# 

@catch2cn
def match(code):
    """匹配表达式"""
    for r in res:
        m = r[0].match(code)
        if m:
            gup = re.findall(r[0], code)
            # print("$$$", gup)
            return r[1], gup if type(gup[0])!=tuple else gup[0]
@catch2cn
def matchSub(code):
    """匹配子章节"""
    for r in res:
        m = r[0].match(code)
        if m:
            # print("sub>>", r, m)
            gup = re.findall(r[0], code)
            return r[1], gup
@catch2cn
def typeconv(val, foo):
    """类型转换"""
    m = match(val)
    #print(">>>", val, m)
    if m: #内部还有表达式
        #print(">>>", val, m)
        if "<" in m[0] and ">" in m[0]:
            foo = m[0]
            # farg = m[0][m[0].index("(")+1:-1]
            arg = []
            for i, a in enumerate(m[1]):
                arg.append(parse(a))
            foo=foo.replace("<", "{").replace(">", "}").replace("[", "{").replace("]", "}")
            pa = f"{foo}".format(*arg)
            #print(">>>>>>", pa)
            return pa
        else:
            return f"{m[0].format(*m[1])}"
    # elif val.startswith("“") and val.endswith("”"):#字符串
    #     return '"'+val[1:-1]+'"'
    # elif val.startswith("《") and (val.endswith("》") or val.endswith("》的值")):#变量
    #     return "ka_vals[\""+val[1:val.rindex("》")]+"\"]"
    else:
        return str(val)
@catch2cn
def parse(statement):
    """解析表达式"""
    if statement.endswith("，"):
        statement = statement[0:-1]
    if f"判断{statement}" in ka_custom_foos: #如果是个判断，自动加上“判断”这个词
        statement = f"判断{statement}"
    m = match(statement)
    if m:
        if "(" not in m[0]:#简单的值
            if "{" in m[0]:#依然要带入
                return f"{m[0]}".format(*m[1])
            return m[0]
        arg = []
        foo = m[0]
        farg = m[0][m[0].index("(")+1:-1]
        fargts = list(m[1])
        if "*" in farg:
            sm = re.findall(r"\*(\d)\*", farg)
            begi = int(sm[0])
            aa = fargts[begi].split("、")
            fargts.pop()
            fargts.extend(aa)
            foo=re.sub(r"\*\d+\*", ",".join(["{"+f"{i+begi}"+"}" for i in range(len(aa))]), foo)    
        
        fargs = [fo.strip() for fo in farg.split(",")]
        fis = [int(fo[1:-1]) for fo in fargs if fo.startswith("<") and fo.endswith(">")]
        lis = [int(fo[1:-1]) for fo in fargs if fo.startswith("[") and fo.endswith("]")]
        for i, a in enumerate(fargts):
            if i in fis:
                kcsub = parse(a)
                #print(">>", kcsub)
                arg.append("'"+kcsub.replace("'", r"\'")+"'")
            elif i in lis:
                subm = matchSub(a)
                fmt = subm[0]
                mres = subm[1]
                sublst = []
                for r in mres:
                    # print("###", r)
                    subks = ["'"+parse(ri).replace("'", r"\'")+"'" for ri in r]
                    sublst.append(fmt.replace("<", "{").replace(">", "}").format(*subks))
                arg.append("["+",".join(sublst)+"]")
            else:
                v = typeconv(a, foo)
                if type(v)==list:
                    arg.extend(v)
                else:
                    arg.append(v)
        foo=foo.replace("<", "{").replace(">", "}").replace("[", "{").replace("]", "}")
        #args = ",".join(arg)
        #print(foo, arg)
        kc = f"{foo}".format(*arg)
        return kc
    else:#解析不了的语句
        return statement

# 整数="整数"
# 浮点数="浮点数"
# 字符串="字符串"
# 循环子="循环子"

def print2kc(codes, fname, newfile=False):
    kb = open(f"{fname}.kc", 'w+' if newfile else "a", encoding='utf-8')
    print(codes, file=kb)
    kb.close()

def prepare(argmap):
    for k,v in argmap.items():
        # cmd = f"{k}={v}"
        # print("::", cmd)
        # exec(cmd)
        print("::", k,"=", v)

DEF_TMP = """
def {0}(**aa):
    {1}
"""
def mkdef(ka_fragments, fooname):
    #print("ttt", fooname)
    fraglst = ka_fragments["codes"][fooname]
    #"exec({})".format(f) if f.startswith("parse(") else "exec({})".format(parse(f))
    fragruns = [parse(f) for f in fraglst]
    ka_fragments["foo"].append(DEF_TMP.format("sub_{}".format(ka_fragments["step"]), "\n    ".join(fragruns)))

def startSubFrag(statement, ka_fragments, ordi, substat):
    #print("{", statement, ordi, ka_fragments["step"])
    ka_fragments["step"] += 1
    subfname = "sub_{}".format(ka_fragments["step"])
    cmd = "{0}!{1}".format(re.sub(ma_next, "", substat),subfname)
    ka_fragments["codes"][ka_fragments["stack"][-1]].append(cmd)
    ka_fragments["stack"].append(subfname)
    ka_fragments["codes"][subfname] = []

def endSubFrag(statement, ka_fragments, ordi, substat):
    #
    #print("}", statement)
    subfname = ka_fragments["stack"][-1]
    mkdef(ka_fragments, subfname)
    step = len([i for i in ordi.split(".") if i!=""])
    #print(len(ka_fragments["stack"])-step-1)
    for s in range(len(ka_fragments["stack"])-step-1):
        ka_fragments["stack"].pop() #= [s for i, s in enumerate(ka_fragments["stack"]) if i<ka_fragments["step"]]
    #ka_fragments["codes"][ka_fragments["stack"][-1]].append(subfname)
    ka_fragments["step"] = step
    ka_fragments["codes"][ka_fragments["stack"][-1]].append(substat)

def fragment(statement, ka_fragments):
    if ma_sub.match(statement):#前有标号，已经在子篇章里面了
        subgup = ma_sub.findall(statement)
        ordi = subgup[0][0]
        substat = subgup[0][1]
        #print("X",statement, ordi)
        #ka_fragments["o"][ka_fragments["ptr"]].append(substat)
        if ma_next.search(substat):#开启子篇章
            startSubFrag(statement, ka_fragments, ordi, substat)
        elif len(ordi.split(".")) < ka_fragments["step"]:#结束该篇章
            endSubFrag(statement, ka_fragments, ordi, substat)
        else:
            ka_fragments["codes"][ka_fragments["stack"][-1]].append(substat)
    else:
        if ma_next.search(statement):
            startSubFrag(statement, ka_fragments, None, statement)
        else:
            endSubFrag(statement, ka_fragments, "", statement)

@catch2cn
def ka_def_fun(foo):
    # print("XXX", foo)
    global ka_imp_fun_name
    ka_imp_fun_name = foo

@catch2cn
def ka_imp_fun(foo):
    # print("III", foo)
    if foo.startswith("《") and foo.endswith("》"):
        foo = foo[1:-1]
    if ka_imp_fun_name:
        funname = ka_imp_fun_name
        # print(foo, foo in ka_get_all_function_in_model())
        if foo in ka_get_all_function_in_model(): #如果已经解析过了，就不解析
            return
        karun(foo, f"功能单元/{foo}.ae")
        # ka_sys[foo]=f"abc()"
        res.insert(0, [re.compile(f"{funname}，把《(.[^》]+)》的([^\s]+)设置为(.+)"), 
                r"ka_run_fun('"+foo+"', '{0}', '{1}', '{2}')"])
        res.insert(1, [re.compile(f"{funname}"), 
                r"ka_run_fun('"+foo+"', None, None, None)"])
        ka_custom_foos.append(funname)
        # print(res)

@catch2cn
def ka_run_fun(foo, obj, attr, value):
    """运行功能单元"""
    # print("RRR", foo, obj, attr, value)
    if obj is not None:
        ka_set_obj_attr(obj, attr, value)
        pycallable=f"{foo}(obj='{obj}')"
        # print(pycallable)
    else:
        pycallable=f"{foo}()"
    exec(compile(pycallable, foo, "exec"), globals())
    return None if f"{foo}结果" not in ka_vals else ka_vals[f"{foo}结果"]
    # if foo.startswith("《") and foo.endswith("》"):
    #     foo = foo[1:-1]
    # if ka_imp_fun_name:
    #     karun(foo, f"功能单元/{foo}.ae")
    #     res.insert(0, [re.compile(f"^{ka_imp_fun_name}$"), f"{ka_imp_fun_name}()"])
    #     print(res)

def ka_parse_a_line(ka_fragments, line):
    global nextsth
    if u"【注】" in line:
        line = line.split(u"【注】")[0]
    for statement in re.split(r"。|！|；|？|\?|!|;", line):
        statement = statement.strip()
        #print(statement)
        if statement is None or statement=="" or statement.startswith("开个玩笑哈~") or statement.endswith("……"):
            continue
        try:
            statement = "".join(replaceSynonymWords(cutWords(statement)))
        except:
            print("分词失败!", statement)
        #句式转换
        if statement.endswith("吗"):
            nextsth = "判断：如果"+statement[0:-1]
            continue
        if nextsth is not None:
            if statement.startswith("如果"):
                statement = statement[2:]
            if statement.startswith(nextsth[5:]):
                statement = nextsth+"，"+statement[len(nextsth[5:]):]
            nextsth = None
        stat = re.split("，|,", statement) #判断并|且|接着|然后这些开头的，将其换成句子
        ss = []
        for si in stat:
            if _ka_m_then.match(si):
                ss.append(si[2:])#去掉 然后|最后
            elif len(ss)==0:
                ss.append(si)
            else:
                ss[-1]=ss[-1]+"，"+si
        for s in ss:
            if ma_next.search(s) or ka_fragments["step"]!=0:#下面要开启新的子篇章了或已经在序号里面了
                fragment(s, ka_fragments)
                continue
            if _ka_m_deffoo.search(s):
                ka_def_fun(_ka_m_deffoo.match(s).groups()[0])
                continue
            if _ka_m_impfoo.search(s):
                ka_imp_fun(_ka_m_impfoo.match(s).groups()[0])
                continue
            if _ka_m_runfoo.search(s):
                ka_run_fun(*_ka_m_runfoo.match(s).groups())
                continue
            ka_fragments["codes"]["main"].append(s)


nextsth = None
@catch2cn
def karun(foo, file):
    """主运行函数"""
    with open(file, "r", encoding='UTF-8') as kf:
        lines = [l.strip() for l in kf.readlines()]
        # codes = []
        #codes存放代码段
        ka_fragments = {"step":0, "codes":{"main":[]}, "stack":["main"], "foo":[]}
        for line in lines:
            ka_parse_a_line(ka_fragments, line)

        mainlines = ["    {0}".format(parse(ml)) for ml in ka_fragments["codes"]["main"]]
        kc = DEF_TMP.format(foo, "\n".join(mainlines)[4:])
        ka_fragments["foo"].append(kc)
                # codes.append(kc)
        if foo=="main":
            ka_fragments["foo"].append("main(vals={})")
        #pprint(ka_fragments)
        
        # print2kb("\n".join(codes))
        pycallable = "".join(ka_fragments["foo"])
        print2kc(pycallable, f"{foo}", True)
        # kac = open("kae.kc", 'w+', encoding='utf-8')
        # print("".join(ka_fragments["foo"]), file=kac)    
        # kac.close()
        
        exec(compile(pycallable, kf.name, "exec"), globals())

@catch2cn
def karuncli(linestxt):
    """交互式主运行函数"""
    lines = [l.strip() for l in linestxt.split()]
    #codes存放代码段
    ka_fragments = {"step":0, "codes":{"main":[]}, "stack":["main"], "foo":[]}
    for line in lines:
        ka_parse_a_line(ka_fragments, line)

    mainlines = ["{0}".format(parse(ml)) for ml in ka_fragments["codes"]["main"]]
    # kc = DEF_TMP.format(foo, "\n".join(mainlines)[4:])
    # ka_fragments["foo"].append(kc)
            # codes.append(kc)
    # if foo=="main":
    # ka_fragments["foo"].append("main(vals={})")
    pycallable = "\n".join(mainlines)
    
    print2kc(pycallable, "cli", newfile=True)
    
    exec(compile(pycallable, "cli", "exec"), globals())
    print2kc(ka_vals, "mem", True)

if __name__=="__main__":
    if len(sys.argv)>1:
        karun("main", sys.argv[1])