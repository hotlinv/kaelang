import glob
kps = glob.iglob(r"./kalib/*.kp.py")
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

整数="整数"
浮点数="浮点数"
字符串="字符串"

ka_vals = {}

with open(sys.argv[1], "r", encoding='UTF-8') as kf:
    lines = [l.strip() for l in kf.readlines()]
    codes = []
    for line in lines:
        for statement in line.split("。"):
            if statement is None or statement=="" or statement.startswith(u"【注】"):
                continue
            kc = run(statement)
            print("&&&", kc)
            if kc:
                exec(compile(kc, kf.name, "exec"))
