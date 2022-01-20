# 【映射】
ka_pmap=KaeLevMap(lev0={
	u"列表：(\w+)到(\w+)":"ka_range({0}, {1})",
    u"在《(.+)》中插入：(.+)":"ka_append('{0}', *1*)",
    u"查找《(.[^》]+)》中“(.[^”]+)”和《(.[^》]+)》的“(.[^”]+)”(.+)的(首条|所有)?记录":"ka_list_find('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')",
    u"过滤(?:列表)?《(.+)》中(.+)的元素组成(?:“)?(.[^”]+)(?:”)?":'ka_list_filter("{0}","{1}","{2}")',
    u"清空(?:列表)?《(.+)》":'ka_list_clear("{0}")',
    # u"把列表《(.+)》(?:用“(.*)”)?(?:来)?(?:进行)?拼接":"ka_join('{0}', '{1}')",
    #u"把列表《(.+)》(?:正向|从小到大)?(?:进行)?排序":"ka_sort('{0}')",
    #u"把列表《(.+)》(?:反向|从大到小)?(?:进行)?排序":"ka_rsort('{0}')",
},lev1={
    u"^《(\w+)》的长度$":"ka_list_len('{0}')",
    u"^《(\w+)》的元素(?:个数|总数)$":"ka_list_len('{0}')",
})

# 【实现】

def ka_new_emptylist(name, value):
    ka_vals[f"{name}"]=[]
    ka_vals[f"{name}_type"]="列表"

registType("空列表", ka_new_emptylist)

@catch2cn
def ka_range(b, e):
    """区间范围"""
    return range(b, e+1)

@catch2cn
def ka_join(lst, op):
    """把列表数据连成一行字符串
    [k]列表(?:用“(.*)”)?(?:进行)?(?:拼接|拼接起来)·'{0}','{1}'
    """
    # print("call join", lst, op)
    ft = f"ka_vals['{lst}拼接后']='{op}'.join([str(i) for i in ka_vals['{lst}']])"
    exec(compile(ft, "list_join", "exec"))
    
@catch2cn
def ka_append(name, *ls):
    """列表中追加数据"""
    # ls = lst.split("、")
    #print(ls)
    #lst2 = [eval(eval(f"parse('{co}')")) for co in ls]
    ka_vals[name].extend(ls)
    # print(name, id(ka_vals[name]))
    #print(lst, ft)
    # exec(compile(ft, "list_append", "exec"))
    
@catch2cn
def ka_list_sort(lstn):
    """把列表数据从小到大排序
    [k]列表(?:正向|从小到大)?(?:进行)?排序·'{0}'
    """
    ka_vals[lstn].sort()

@catch2cn
def ka_list_rsort(lstn):
    """把列表数据从大到小排序
    [k]列表(?:反向|从大到小)(?:进行)?排序·'{0}'
    """
    ka_vals[lstn].sort(reverse=True)

@catch2cn
def ka_list_get(lstn, i, name):
    """选择《序列》中第i个元素作为基准数
    [k]列表中第(\d+)个元素作为(.+)·"{0}",{1},"{2}"
    """
    # print(lstn, i, name)
    ka_vals[f"{name}"] = ka_vals[lstn][i-1]
    ka_vals[f"{name}_i"] = i-1
    
@catch2cn
def ka_list_filter(lstn, cmp, name):
    """过滤列表中的元素组成新数组
    """
    p = ka_parse("a"+cmp)
    ka_vals[name] = [a for a in ka_vals[lstn] if eval(p)]
    ka_vals[name+"_type"] = "列表"
    
@catch2cn
def ka_list_clear(lstn):
    """清空列表所有元素
    [k]列表清空·'{0}'
    """
    ka_vals[lstn].clear()
@catch2cn
@lastit
def ka_list_flatten(lstn):
    """任意维数组一维化
    [k]列表一维化·'{0}'
    """
    a = ka_vals[lstn]
    flatten = lambda x: [y for l in x for y in flatten(l)] if type(x) is list else [x]
    ka_vals[lstn+"一维化后"] = flatten(a)
    ka_vals[lstn+"一维化后_type"] = "列表"
    return lstn+"一维化后"

@catch2cn
def ka_list_len(lstn):
    """获取列表长度"""
    # print(lstn,ka_vals[lstn], len(ka_vals[lstn]))
    return len(ka_vals[lstn])

@catch2cn
@lastit
def ka_list_find(lstname, rattname, cname, cattname, conp, all):
    """查找列表中满足条件的记录
    """
    ret = []
    lst = ka_vals[lstname]
    if lstname+"_map" in ka_vals:
        lstmap = ka_vals[lstname+"_map"]
        rattname = lstmap[rattname]
    cmpo = ka_vals[cname]
    if cname+"_map" in ka_vals:
        cmap = ka_vals[cname+"_map"]
        cname = cmap[cattname]
    cmpval = cmpo[cname]
    for i,item in enumerate(lst):
        rval = item[rattname]
        m = ka_parse(f"{rval}和{cmpval}"+conp)
        #print("find", conp,"==>", m)
        if m and m!=conp and eval(m.format(rval, cmpval)):
            ret.append(item)
    if all=="首条":
        ka_vals[lstname+"查找结果"] = ret[0]
        ka_vals[lstname+"查找结果_type"] = "对象"
    else:
        ka_vals[lstname+"查找结果"] = ret
        ka_vals[lstname+"查找结果_type"] = "列表"
    if lstname+"_map" in ka_vals:
        ka_vals[lstname+"查找结果_map"] = ka_vals[lstname+"_map"]
    # print(ka_vals)
    return lstname+"查找结果"