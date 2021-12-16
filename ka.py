import glob
import inspect as ins
from pprint import pprint
import sys, re
import logging
# 配置logging
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d - %(message)s',
    handlers=[
        #logging.FileHandler("ke.log", mode="a"),  # for logs write in file（mode：a为追加log，设置为w则表示每次清空，重新记录log）
        logging.StreamHandler()  # for print at console
    ]
)

def catch2cn(fn):
    def inner(*args):
        try:
            return fn(*args)
        except Exception as e:
            fndoc = ins.getdoc(fn)
            err = u"{}出错：{}".format(fndoc, str(e))
            #print(err)
            logging.error(err)
    return inner

ka_vals = {} #放变量
ka_sys = {} #放语言语法映射
res = []

@catch2cn
def loadkp():
    kps = glob.glob(r"./kalib/*.kp")
    kps.extend(glob.glob(r"./kalib/*.kp.py"))
    for kp in kps:
        #print(kp)
        with open(kp, "r", encoding='UTF-8') as kpf:
            lines = kpf.readlines()
            codes = []
            mapcodes = []
            now=None
            for line in lines:
                # print(line)
                if line.startswith(u"# 【实现】"):
                    now="code"
                    continue
                elif line.startswith(u"# 【映射】"):
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
loadkp()
for k,v in eval("ka_sys").items():
    res.append([re.compile(k), v])

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
            gup = re.findall(r[0], code)
            return r[1], gup
@catch2cn
def typeconv(val, foo):
    """类型转换"""
    m = match(val)
    if m: #内部还有表达式
        #print(">>>", val, m)
        return f"{m[0].format(*m[1])}"
    # elif val.startswith("“") and val.endswith("”"):#字符串
    #     return '"'+val[1:-1]+'"'
    elif val.startswith("《") and (val.endswith("》") or val.endswith("》的值")):#变量
        return "ka_vals[\""+val[1:val.rindex("》")]+"\"]"
    else:
        return str(val)
@catch2cn
def parse(statement):
    """解析表达式"""
    m = match(statement)
    if m:
        if "(" not in m[0]:#简单的值
            if "{" in m[0]:#依然要带入
                return f"{m[0]}".format(*m[1])
            return m[0]
        arg = []
        foo = m[0]
        farg = m[0][m[0].index("(")+1:-1]
        if farg=="*":
            arg.extend([typeconv(v, "f()") for v in m[1][0].split("、")])
            foo=foo.replace("*", ",".join(["{}" for i in range(len(arg))]))
            #print(foo, arg)
        else:
            fargs = [fo.strip() for fo in farg.split(",")]
            fis = [int(fo[1:-1]) for fo in fargs if fo.startswith("<") and fo.endswith(">")]
            lis = [int(fo[1:-1]) for fo in fargs if fo.startswith("[") and fo.endswith("]")]
            for i, a in enumerate(m[1]):
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
                        subks = ["'"+parse(ri)+"'" for ri in r]
                        sublst.append(fmt.replace("<", "{").replace(">", "}").format(*subks))
                    arg.append("["+",".join(sublst)+"]")
                    # print("###", arg)
                else:
                    v = typeconv(a, m[0])
                    if type(v)==list:
                        arg.extend(v)
                    else:
                        arg.append(v)
            foo=foo.replace("<", "{").replace(">", "}").replace("[", "{").replace("]", "}")
        #args = ",".join(arg)
        kc = f"{foo}".format(*arg)
        return kc
    else:#解析不了的语句
        return statement

# 整数="整数"
# 浮点数="浮点数"
# 字符串="字符串"
# 循环子="循环子"

def print2kb(codes):
    kb = open("kae.kb", 'w+', encoding='utf-8')
    print(codes, file=kb)
    kb.close()

ma_next = re.compile(u"((?:如下|以下)(?:动作|操作)：)")
ma_sub = re.compile(u"^((?:\d|\.)+)）(.+)")

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
def main():
    with open(sys.argv[1], "r", encoding='UTF-8') as kf:
        lines = [l.strip() for l in kf.readlines()]
        # codes = []
        #codes存放代码段
        ka_fragments = {"step":0, "codes":{"main":[]}, "stack":["main"], "foo":[]}
        for line in lines:
            if u"【注】" in line:
                line = line.split(u"【注】")[0]
            for statement in line.split("。"):
                statement = statement.strip()
                if statement is None or statement=="":
                    continue
                if ma_next.search(statement) or ka_fragments["step"]!=0:#下面要开启新的子篇章了或已经在序号里面了
                    fragment(statement, ka_fragments)
                    continue
                ka_fragments["codes"]["main"].append(statement)

        mainlines = ["    {0}".format(parse(ml)) for ml in ka_fragments["codes"]["main"]]
        kc = DEF_TMP.format("main", "\n".join(mainlines)[4:])
        ka_fragments["foo"].append(kc)
                # codes.append(kc)
        ka_fragments["foo"].append("main(vals={})")
        #pprint(ka_fragments)
        
        # print2kb("\n".join(codes))
        kac = open("kae.kc", 'w+', encoding='utf-8')
        print("".join(ka_fragments["foo"]), file=kac)
        # exec(compile("\n".join(ka_fragments["codes"]), kf.name, "exec"))
        # for c in codes:
        #     print(eval(c), file=kac)
        #     
        kac.close()
        
        exec(compile("".join(ka_fragments["foo"]), kf.name, "exec"), globals())

main()