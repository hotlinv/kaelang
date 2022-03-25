# 【引用】

# 【映射】
ka_pmap=KaeLevMap(lev1={
    u"^(.+)和(.+)(?:前半段|开头)相同$":"ka_str_startswith('{0}', '{1}')",
    u"^(.+)和(.+)(?:后半段|结尾)相同$":"ka_str_endswith('{0}', '{1}')",
    u"^(.+)和(.+)有包含关系$":"ka_str_in('{0}', '{1}')",
})

# 【实现】

def ka_new_str(name, value):
    value=value.replace("“","\"").replace("”","\"")
    exec(f"ka_vals[\"{name}\"]={value}")
    exec(f"ka_vals[\"{name}_type\"]='字符串'")
    return name

registType("字符串", ka_new_str)

@catch2cn
def ka_str_startswith(str1, str2):
    """判断两个字符串是不是相同开头"""
    if len(str1)<len(str2):
        return str2.startswith(str1)
    else:
        return str1.startswith(str2)
@catch2cn
def ka_str_endswith(str1, str2):
    """判断两个字符串是不是相同结尾"""
    if len(str1)<len(str2):
        return str2.endswith(str1)
    else:
        return str1.endswith(str2)

@catch2cn
def ka_str_in(str1, str2):
    """判断两个字符串是不是有包含关系"""
    if len(str1)<len(str2):
        return str1 in str2
    else:
        return str2 in str1