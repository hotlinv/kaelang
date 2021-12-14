import glob

ka_vals = {} #放变量
ka_sys = {} #放语言语法映射
ka_fragments = {"now":0, "codes":[], "o":{}}

kps = glob.glob(r"./kalib/*.kp")
kps.extend(glob.glob(r"./kalib/*.kp.py"))
for kp in kps:
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
        exec(m)
        mup = compile("ka_sys.update(ka_pmap())", "kae", "exec")
        exec(mup)

        code = "\n".join(codes)
        c = compile(code, kpf.name, "exec")
        exec(c)
        

import sys, re
res = []
for k,v in eval("ka_sys").items():
    res.append([re.compile(k), v])

def match(code):
    for r in res:
        m = r[0].match(code)
        if m:
            gup = re.findall(r[0], code)
            # print("$$$", gup)
            return r[1], gup if type(gup[0])!=tuple else gup[0]

def matchSub(code):
    for r in res:
        m = r[0].match(code)
        if m:
            gup = re.findall(r[0], code)
            return r[1], gup

def typeconv(val, foo):
    if val.startswith("“") and val.endswith("”"):#字符串
        return '"'+val[1:-1]+'"'
    elif val.startswith("《") and (val.endswith("》") or val.endswith("》的值")):#变量
        return "ka_vals[\""+val[1:val.rindex("》")]+"\"]"
    else:
        return str(val)

def run(statement):
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
                    kcsub = run(a)
                    #print(">>", kcsub)
                    arg.append("'"+kcsub+"'")
                elif i in lis:
                    subm = matchSub(a)
                    fmt = subm[0]
                    mres = subm[1]
                    sublst = []
                    for r in mres:
                        subks = ["'"+run(ri)+"'" for ri in r]
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

# 整数="整数"
# 浮点数="浮点数"
# 字符串="字符串"
# 循环子="循环子"

def print2kb(txt):
    kb = open("kae.kb", 'w+', encoding='utf-8')
    print(txt, file=kb)
    kb.close()

ma_next = re.compile(u"(?:如下|以下)(?:动作|操作)：")
ma_sub = re.compile(u"^((?:\d|\.)+)）(.+)")

DEF_TMP = """
def {0}():
    {1}
"""
def subdef(fraglst):
    fragruns = ["exec({})".format(f) if f.startswith("run(") else "exec({})".format(run(f)) for f in fraglst]
    ka_fragments["codes"].append(DEF_TMP.format("sub_{}".format(ka_fragments["now"]), "\n    ".join(fragruns)))

def fragment(statement):
    global ka_fragments
    if ma_sub.match(statement):#子代码段
        subgup = ma_sub.findall(statement)
        ordi = subgup[0][0]
        substat = subgup[0][1]
        print(ka_fragments["ptr"])
        ka_fragments["o"][ka_fragments["ptr"]].append(substat)
        #print("###", statement, ka_now_fragment , ordi.split("."))
        if ka_fragments["now"] != len(ordi.split(".")):#结束该篇章
            subdef(ka_fragments["o"][ka_fragments["ptr"]])
            ka_fragments["now"] = len(ordi.split("."))
            ka_fragments["ptr"] = "p_{0}".format(ka_fragments["now"])
        #ka_fragments.append("+"*ka_now_fragment+substat)

with open(sys.argv[1], "r", encoding='UTF-8') as kf:
    lines = [l.strip() for l in kf.readlines()]
    codes = []
    for line in lines:
        if u"【注】" in line:
            line = line.split(u"【注】")[0]
        for statement in line.split("。"):
            statement = statement.strip()
            if statement is None or statement=="":
                continue
            if ma_next.search(statement):#下面要开启新的篇章了
                fragment(statement)
                ka_fragments["now"] += 1
                ka_fragments["ptr"] = "p_{0}".format(ka_fragments["now"])
                ka_fragments["o"][ka_fragments["ptr"]] = []
                #ka_now_frag_ptr = []
                continue
            if ka_fragments["now"]!=0:
                fragment(statement)
                continue
            kc = run(statement)
            if kc is None:#解析不了的语句
                kc = "! "+statement
            #ka_fragments.append(kc)
            codes.append(kc)
    print(ka_fragments)
    print2kb("\n".join(codes))
    kac = open("kae.kc", 'w+', encoding='utf-8')
    for c in ka_fragments["codes"]:
        print(c, file=kac)
    exec(compile("\n".join(ka_fragments["codes"]), kf.name, "exec"))
    for c in codes:
        print(eval(c), file=kac)
        exec(compile(eval(c), kf.name, "exec"))
    kac.close()
