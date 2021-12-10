# 【映射】
ka_pmap=lambda:{
	u"列表：(\w+)到(\w+)":"ka_range({0}, {1})",
    u"在《(.+)》中插入：(.+)":"ka_append('{0}', '{1}')",
    u"将列表《(.+)》拼接在一起":"ka_join({0})"
}

# 【实现】
def ka_range(b, e):
    return range(b, e+1)

def ka_join(lst):
    return "".join(lst)

def ka_append(name, lst):
    ls = lst.split("、")
    lst2 = [eval(eval(f"run('{co}')")) for co in ls]
    #print(lst2)
    ft = f"ka_vals['{name}'].extend({lst2})"
    exec(compile(ft, "list_append", "exec"))