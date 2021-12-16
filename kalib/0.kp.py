# 【映射】
KA_DEF = u"(?:新建|创建|定义|有)?"
KA_AS = u"(?:称作|称为|名为|叫|名叫|叫做)"
ka_pmap=lambda:{
    u"^“(.+)”$":'"{0}"',
	u"(?:在|于|用|使用)?(?:控制台)?打印[：:]\s*(.+)":"ka_out(*)",
    u"(?:把|将)?(.+)，并打印":"ka_out(<0>)",
	KA_DEF+u"一个"+KA_AS+"(“.+”)的(.+)，(?:值|初始化)为(.+)":"ka_new({0}, '{1}', '{2}')",
    KA_DEF+u"一个(.[^名]+)"+KA_AS+"(“.+”)，(?:值|初始化)为(.+)":"ka_new({1}, '{0}', '{2}')",
    KA_DEF+u"一个"+KA_AS+"(“.+”)的(.+)":"ka_new({1}, '{0}', None)",
    KA_DEF+u"一个(.[^名]+)"+KA_AS+"(“.+”)":"ka_new({1}, '{0}', None)",
    u"判断：((?:如果|如|若|如若|若是).+，(?:则|就|那么).+，)+(?:否则|不然|不然就)(.+)":"ka_sel([0], <1>)",
    u"(?:启动|开始)循环《(.+)》，(?:运行|执行)(.+)":"ka_for('{0}', <1>, aa)",
    u"(?:如果|如|若|如若|若是)(.+?)，(?:则|就|那么)(.+?)，":"[<0>, <1>]",
    u"(.+)比(.+)大":"ka_gt({0}, {1})",
    u"(.+)大于(.+)":"ka_gt({0}, {1})",
    u"(.+)比(.+)小":"ka_lt({0}, {1})",
    u"(.+)小于(.+)":"ka_lt({0}, {1})",
    u"(.+)不大于(.+)":"ka_lte({0}, {1})",
    u"(.+)不小于(.+)":"ka_gte({0}, {1})",
    u"(.+)等于(.+)":"ka_eq({0}, {1})",
    u"(.+)和(.+)相等":"ka_eq({0}, {1})",
    u"(.+)不等于(.+)":"ka_neq({0}, {1})",
    u"(.+)和(.+)不相等":"ka_neq({0}, {1})",
    u"^(\d+)\s乘以\s(\d+)$":"ka_mu({0}, {1})",
    u"^(.[^“”]+)\s乘以\s(.[^“”]+)$":"ka_mu(<0>, <1>)",
    u"^(\d+)与(\d+)求积$":"ka_mu({0}, {1})",
    u"^(.+)与(.+)求积$":"ka_mu(<0>, <1>)",
    u"^(\d+)加(\d+)$":"ka_add({0}, {1})",
    u"^(.[^“”]+)\s加\s(.[^“”]+)$":"ka_add(<0>, <1>)",
    u"^(\d+)与(\d+)求和$":"ka_add({0}, {1})",
    u"^(\w+)与(\w+)求和$":"ka_add(<0>, <1>)",
    u"^(\d+)减(\d+)$":"ka_mi({0}, {1})",
    u"^(.[^“”]+)\s减\s(.[^“”]+)$":"ka_mi(<0>, <1>)",
    u"^(\d+)与(\d+)求差$":"ka_mi({0}, {1})",
    u"^(\w+)与(\w+)求差$":"ka_mi(<0>, <1>)",
    u"^制表符$":"r'\t'",
    u"^(\d+)$":"{0}",
    u"^!(\w+)$":"!{0}",
    u"^《(\w+)》当前值$":'ka_get("{0}")',
}

# 【实现】

@catch2cn
def ka_out(*a):
    """打印"""
    print(*a)

@catch2cn
def ka_get(key):
    """获取变量"""
    return ka_vals["《"+key+"》当前值"]

def ka_new_str(name, value):
    value=value.replace("“","\"").replace("”","\"")
    exec(f"ka_vals[\"{name}\"]={value}")

def ka_new_num(name, value):
    exec(f"ka_vals[\"{name}\"]={value}")

def ka_new_itor(name, value):
    exec(f"ka_vals[\"{name}\"]=parse('{value}')")

registType("字符串", ka_new_str)
registType("整数", ka_new_num)
registType("浮点数", ka_new_num)
registType("循环子", ka_new_itor)

@catch2cn
def ka_new(name, type, value):
    """创建新对象"""
    ka_types[type](name, value)
@catch2cn
def ka_gt(v1, v2):
    """比较大于"""
    return eval(f"{v1}>{v2}")
@catch2cn
def ka_gte(v1, v2):
    """比较大等于"""
    return eval(f"{v1}>={v2}")
@catch2cn
def ka_lt(v1, v2):
    """比较小于"""
    return eval(f"{v1}<{v2}")
@catch2cn
def ka_lte(v1, v2):
    """比较小等于"""
    return eval(f"{v1}<={v2}")
@catch2cn
def ka_eq(v1, v2):
    """比较等于"""
    return eval(f"{v1}<{v2}")
@catch2cn
def ka_neq(v1, v2):
    """比较不等于"""
    return eval(f"{v1}!={v2}")
@catch2cn
def ka_add(v1, v2):
    """算加法"""
    return eval(f"{v1}+{v2}")
@catch2cn
def ka_mi(v1, v2):
    """算减法"""
    return eval(f"{v1}-{v2}")
@catch2cn
def ka_mu(v1, v2):
    """算乘法"""
    return eval(f"{v1}*{v2}")

@catch2cn
def ka_sel(iflist, elsefoo):
    """条件选择"""
    text = "elif {0}:\n    {1}"
    elsetxt = "else:\n    {0}"
    textline = []
    for con, foo in iflist:
        textline.append(text.format(con, foo))
    textline.append(elsetxt.format(elsefoo))
    ft = "\n".join(textline)[2:]
    exec(compile(ft, "core_if", "exec"))
    
@catch2cn
def ka_for(it, foo, aa):
    """循环遍历"""
    #print("XXXX", it, foo, ka_vals)
    # print("$$", aa)
    if foo.startswith("!"):
        up = 'ka_vals.update({'+f"'《{it}》当前索引':idx,'《{it}》当前值':{it}"+"})\n    "
        foo = up+foo[1:]+"(**aa)"
    else:
        up = 'ka_vals.update({'+f"'《{it}》当前索引':idx,'《{it}》当前值':{it}"+"})\n    "
        foo = up+foo.replace(f"《{it}》当前值", f"{it}").replace(f"《{it}》当前索引", f"idx")
    fortext = "for idx, {0} in enumerate(iter({1})):\n    {2}"
    ft = fortext.format(it, eval(f"ka_vals['{it}']"), foo)
    #return ft
    #print(ft)
    exec(compile(ft, "core_for", "exec"))
