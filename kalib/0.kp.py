# 【映射】
KA_DEF = u"(?:新建|有)?"
KA_AS = u"(?:称为)"
ka_pmap=lambda:{
    u"^“(.+)”$":'"{0}"',
	u"(?:在|于|用|使用)?(控制台|语音)?(?:打印|输出|说)[：:]\s*(.+)":"ka_out('{0}', *1*)",
    u"(?:把|将)?(.+)，并打印":"ka_out(<0>)",
	KA_DEF+u"一个"+KA_AS+"(“.+”)的(.+)，(?:值|初始化)为(.+)":"ka_new({0}, '{1}', '{2}')",
    KA_DEF+u"一个(.[^名]+)"+KA_AS+"(“.+”)，(?:值|初始化)为(.+)":"ka_new({1}, '{0}', '{2}')",
    KA_DEF+u"一个(.+)的(.[^名]+)"+KA_AS+"(“.+”)":"ka_new({2}, '{1}', '{0}')",
    KA_DEF+u"一个"+KA_AS+"(“.+”)的(.+)":"ka_new({1}, '{0}', None)",
    KA_DEF+u"一个(.[^名]+)"+KA_AS+"(“.+”)":"ka_new({1}, '{0}', None)",
    u"判断：((?:如果).+，(?:则).+，)+(?:否则)(.+)":"ka_sel([0], <1>)",
    u"(?:启动)循环《(.+)》，(?:运行|执行)(.+)":"ka_for('{0}', <1>, aa)",
    u"(?:如果)(.+?)，(?:则)(.+?)，":"[<0>, <1>]",
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
    u"^感叹号$":"r'！'",
    u"^(\d+)$":"{0}",
    u"^!(\w+)$":"!{0}",
    u"^《(\w+)》当前值$":'ka_get("{0}")',
    u"^《(\w+)》的值$":'ka_vals["{0}"]',
}

# 【实现】

ka_outputs[""] = "ka_std_print(*)"
ka_outputs["控制台"] = "ka_std_print(*)"
ka_outputs["终端"] = "ka_std_print(*)"

@catch2cn
def ka_std_print(*a):
    """终端打印"""
    print(*a)

@catch2cn
def ka_out(out, *arg):
    """输出"""
    #print(">>>>", arg)
    # arg = []
    # arg.extend([parse(v) for v in a.split("、")])
    foo = ka_outputs[out]
    foo=foo.replace("*", ",".join(['"""{}"""' for i in range(len(arg))]))
    #print(">>>", foo.format(*arg))
    exec(foo.format(*arg))

@catch2cn
def ka_cn2int(nu, defnu):
    # print(nu)
    if nu is None or nu == "":
        return defnu
    if isinstance(nu, int):
        return int(nu)
    else:
        cnn = "零一二三四五六七八九十"
        n = cnn.find(nu)
        if n==-1 and nu=="两":
            return 2
        else:
            return defnu
        return n

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
        # foo = up+foo.replace(f"《{it}》当前值", f"{it}").replace(f"《{it}》当前索引", f"idx")
        foo = up+foo
        # foo = up+foo[1:]+"(**aa)"
    fortext = "for idx, {0} in enumerate(iter({1})):\n    {2}"
    ft = fortext.format(it, eval(f"ka_vals['{it}']"), foo)
    #return ft
    #print(ft)
    exec(compile(ft, "core_for", "exec"))
