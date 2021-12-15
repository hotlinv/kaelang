# 【映射】
ka_pmap=lambda:{
	u"列表：(\w+)到(\w+)":"ka_range({0}, {1})",
    u"在《(.+)》中插入：(.+)":"ka_append('{0}', '{1}')",
    u"将列表《(.+)》(?:用“(.*)”)?(?:来)?(?:进行)?拼接":"ka_join('{0}', '{1}')"
}

# 【实现】
def ka_range(b, e):
    return range(b, e+1)

def ka_join(lst, op):
    ft = f"ka_vals['{lst}拼接后']='{op}'.join([str(i) for i in ka_vals['{lst}']])"
    exec(compile(ft, "list_join", "exec"))
    

def ka_append(name, lst):
    ls = lst.split("、")
    #print(ka_vals)
    lst2 = [eval(eval(f"parse('{co}')")) for co in ls]
    ft = f"ka_vals['{name}'].extend({lst2})"
    #print(ft)
    exec(compile(ft, "list_append", "exec"))
    