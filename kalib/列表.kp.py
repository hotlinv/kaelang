# 【映射】
ka_pmap=lambda:{
	u"列表：(\w+)到(\w+)":"ka_range({0}, {1})",
    u"在《(.+)》中插入：(.+)":"ka_append('{0}', '{1}')",
    u"将列表《(.+)》(?:用“(.*)”)?(?:来)?(?:进行)?拼接":"ka_join('{0}', '{1}')"
}

# 【实现】

def ka_new_emptylist(name, value):
    exec(f"ka_vals[\"{name}\"]=[]")

registType("空列表", ka_new_emptylist)

@catch2cn
def ka_range(b, e):
    """区间范围"""
    return range(b, e+1)

@catch2cn
def ka_join(lst, op):
    """把列表数据连成一行字符串"""
    ft = f"ka_vals['{lst}拼接后']='{op}'.join([str(i) for i in ka_vals['{lst}']])"
    exec(compile(ft, "list_join", "exec"))
    
@catch2cn
def ka_append(name, lst):
    """列表中追加数据"""
    ls = lst.split("、")
    #print(ka_vals)
    lst2 = [eval(eval(f"parse('{co}')")) for co in ls]
    ft = f"ka_vals['{name}'].extend({lst2})"
    #print(lst, ft)
    exec(compile(ft, "list_append", "exec"))
    