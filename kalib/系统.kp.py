# 【映射】
ka_sys = {
	u"(?:在|于|用|使用)?(?:控制台)?打印[：:]\s*(.+)":"ka_pr(*)",
	u"(?:新建|创建|定义|有)?一个名叫(“\w+”)的(.+)，(?:值|初始化)为(.+)":"ka_new({0}, {1}, {2})",
    u"(?:新建|创建|定义|有)?一个(.+)叫(“\w+”)，(?:值|初始化)为(.+)":"ka_new({1}, {0}, {2})",
    u"判断：如果(.+)，(?:则|就)(.+)":"ka_sel(<0>, <1>)",
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
        exec(f"ka_vals[\"{name}\"]=\"{value}\"")
    elif type=="整数" or type=="浮点数":
        exec(f"ka_vals[\"{name}\"]={value}")
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

def ka_sel(con, foo):
    if eval(con):
        exec(foo)
