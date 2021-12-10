# 【映射】
ka_pmap=lambda:{
	u"(?:在|于|用|使用)?(?:控制台)?打印[：:]\s*(.+)":"ka_pr(*)",
	u"(?:新建|创建|定义|有)?一个名叫(“\w+”)的(.+)，(?:值|初始化)为(.+)":"ka_new({0}, '{1}', '{2}')",
    u"(?:新建|创建|定义|有)?一个(.+)叫(“\w+”)，(?:值|初始化)为(.+)":"ka_new({1}, '{0}', '{2}')",
    u"判断：((?:如果|如|若|如若|若是).+，(?:则|就|那么).+，)+(?:否则|不然|不然就)(.+)":"ka_sel([0], <1>)",
    u"(?:启动|开始)循环《(.+)》，(?:运行|执行)：(.+)":"ka_for('{0}', <1>)",
    u"(?:如果|如|若|如若|若是)(.+?)，(?:则|就|那么)(.+?)，":"[<0>, <1>]",
    u"(.+)比(.+)大":"ka_gt({0}, {1})",
    u"(.+)大于(.+)":"ka_gt({0}, {1})",
    u"(.+)比(.+)小":"ka_lt({0}, {1})",
    u"(.+)小于(.+)":"ka_lt({0}, {1})",
    u"(.+)不大于(.+)":"ka_lte({0}, {1})",
    u"(.+)不小于(.+)":"ka_gte({0}, {1})",
    u"(.+)等于(.+)":"ka_eq({0}, {1})",
    u"(.+)不等于(.+)":"ka_neq({0}, {1})",
}

# 【实现】
def ka_pr(*a):
    print(*a)

def ka_new(name, type, value):
    if type=="字符串":
        value=value.replace("“","\"").replace("”","\"")
        exec(f"ka_vals[\"{name}\"]={value}")
    elif type=="整数" or type=="浮点数":
        exec(f"ka_vals[\"{name}\"]={value}")
    elif type=="循环子":
        exec(f"ka_vals[\"{name}\"]=run(value)")
        #print(abc)
def ka_gt(v1, v2):
    return eval(f"{v1}>{v2}")
def ka_gte(v1, v2):
    return eval(f"{v1}>={v2}")
def ka_lt(v1, v2):
    return eval(f"{v1}<{v2}")
def ka_lte(v1, v2):
    return eval(f"{v1}<={v2}")
def ka_eq(v1, v2):
    return eval(f"{v1}<{v2}")
def ka_neq(v1, v2):
    return eval(f"{v1}!={v2}")


def ka_sel(iflist, elsefoo):
    text = "elif {0}:\n    {1}"
    elsetxt = "else:\n    {0}"
    textline = []
    for con, foo in iflist:
        textline.append(text.format(con, foo))
    textline.append(elsetxt.format(elsefoo))
    ft = "\n".join(textline)[2:]
    print2kb(ft)
    exec(compile(ft, "core_if", "exec"))
    
def ka_for(it, foo):
    #print("XXXX", it, foo, eval(f"ka_vals['{it}']"))
    fortext = "for idx, {0} in enumerate(iter({1})):\n    {2}"
    ft = fortext.format(it, eval(f"ka_vals['{it}']"), 
        foo.replace(f"《{it}》当前值", f"{it}").replace(f"《{it}》当前索引", f"idx"))
    print2kb(ft)
    exec(compile(ft, "core_for", "exec"))
