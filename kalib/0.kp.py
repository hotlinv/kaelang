# 【映射】
from sys import stderr


KA_DEF = u"(?:新建|有)?"
KA_AS = u"(?:称为)"
KA_OBJ_VAL = u"^《(\w+)》的值$"
KA_OBJ_ATTR = u"^《(\w+)》的(\w+)$"
KA_ITER_NOW = u"^《(\w+)》当前值$"
ka_pmap=KaeLevMap(lev0={
    u"^“(.+)”$":'"{0}"',
	u"(?:在|于|用|使用)?(控制台|语音)?(?:打印|输出|说|说出)[：:]\s*(.+)":"ka_out('{0}', *1*)",
    u"(?:把|将)?(.+)，并打印":"ka_out(<0>)",
	KA_DEF+u"一个"+KA_AS+"(“.+”)的(.+)，(?:值为|初始化为)?(.+)":"ka_new({0}, '{1}', '{2}')",
    KA_DEF+u"一个(.[^名]+)"+KA_AS+"(“.+”)，(?:值为|初始化为)?(.+)":"ka_new({1}, '{0}', '{2}')",
    KA_DEF+u"一个(.+)的(.[^名]+)"+KA_AS+"(“.+”)":"ka_new({2}, '{1}', '{0}')",
    KA_DEF+u"一个"+KA_AS+"(“.+”)的(.+)":"ka_new({1}, '{0}', None)",
    KA_DEF+u"一个(.[^名]+)"+KA_AS+"(“.+”)":"ka_new({1}, '{0}', None)",
    u"判断：((?:如果).+，(?:则).+)+，?(?:(?:否则)(.+))?":"ka_sel([0], <1>)",
    #u"(.+)吗？(.+)":"ka_sel(<0>, <1>)",
    u"(?:启动)循环《(.+)》，(?:进行|运行|执行)(.+)":"ka_for('{0}', <1>, aa)",
    u"(?:如果)(.+?)，(?:则)([^如否]+)(?:，|。|；)?":"[<0>, <1>]",
    u"(?:把|将|对)(.+)?《(.+?)》进行(.+)":"ka_call('{0}', '{1}', '{2}', None)",
    u"(?:把|将|对)(.+)?《(.+?)》(.+)进行(.+)":"ka_call('{0}', '{1}', '{3}', '{2}')",
    u"(?:从)(.+)?《(.+?)》(?:中|里|里面)(.+)":"ka_from_do('{0}', '{1}', '{2}')",
    #u"(?:把|将|对)(.+)?《(.+?)》(.+)":"ka_call('{0}', '{1}', '{2}', None)",
    u"^([^，]+)结果即为([^，]+)$":"ka_fun_return('{0}', '{1}')",
    u"监听对象(.+)":"ka_fun_param(aa, *0*)",
    u"(?:把|将)(?:其|它|他|她)(?:重定义|定义)为(.+)":"ka_rename('{0}', None)",
    u"(?:把|将)(.+)(?:重定义|定义)为(.+)":"ka_rename('{1}','{0}')",
    u"(?:把|将)(?:其|它|他|她)(.+)":"ka_next_do('{0}')",
    u"以《(.[^》]+)》来描述《(.[^》]+)》":"ka_map4obj('{0}', '{1}')",
    u"依照《(.[^》]+)》构建(.+)":"ka_class2obj('{0}', '{1}')",
    u"设置《(.[^》]+)》的(.+)为(.+)":"ka_set_obj_attr('{0}', '{1}', '{2}')",
    u"把《(.[^》]+)》的(.+)设置为(.+)":"ka_set_obj_attr('{0}', '{1}', '{2}')",
    u"^(.+)和(.+)(?:前半段|开头)相同$":"ka_str_startswith('{0}', '{1}')",
    u"^(.+)和(.+)(?:后半段|结尾)相同$":"ka_str_endswith('{0}', '{1}')",
    u"^(.+)和(.+)有包含关系$":"ka_str_in('{0}', '{1}')",
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
    KA_ITER_NOW:'ka_get("{0}")',
    KA_OBJ_VAL:'ka_vals["{0}"]',
    KA_OBJ_ATTR:'ka_get_obj_attr("{0}", "{1}")',
    u"^是$":"True",
    u"^否$":"False",
})

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
def ka_fun_param(aa, *arg):
    '''函数设置参数'''
    foo=",".join(["{}" for i in range(len(arg))])
    # print(">>>", aa, foo.format(*arg))
    ka_vals[foo.format(*arg)] = ka_vals[aa["obj"]]
    if aa["obj"]+"_map" in ka_vals:
        ka_vals[foo.format(*arg)+"_map"] = ka_vals[aa["obj"]+"_map"]
    # print(ka_vals)
    # exec(foo.format(*arg))

@catch2cn
def ka_cn2int(nu, defnu):
    """把中文数字变为数字"""
    # print(nu)
    if nu is None or nu == "":
        return defnu
    if nu.isdigit():
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

@catch2cn
def ka_map4obj(clsname, dataname):
    """把变量的属性名进行对应（英转中）"""
    ka_vals[dataname+"_map"] = ka_vals[clsname]

@catch2cn
def ka_class2obj(clsname, obj):
    """按照类描述新建对象"""
    # print("cls2obj", clsname, obj)
    ka_vals[obj] = {}
    ka_vals[obj+"_map"] = ka_vals[clsname]

@catch2cn
def ka_set_obj_attr(objname, attrname, obj):
    """设置对象属性"""
    if objname+"_map" in ka_vals:
        attrname = ka_vals[objname+"_map"][attrname]
    # print("set_attr", objname, ".", attrname, "=>", obj)
    if re.match(r"^ka_\w+(.+)$", obj):
        ka_vals[objname][attrname] = eval(obj)
    elif re.match(r"^\d+", obj):
        ka_vals[objname][attrname] = re.findall(r"\d+",obj)[0]
    else:
        ka_vals[objname][attrname] = obj

@catch2cn
def ka_get_obj_attr(objname, attrname):
    """获取变量的属性"""
    # print("get_attr", objname, ".", attrname)
    obj = ka_vals[objname]
    if objname+"_map" in ka_vals:
        omap = ka_vals[objname+"_map"]
        key = omap[attrname]
        #递归获取到对应的属性
        fval = lambda k, obj: obj[k] if type(k)==str else fval(k[list(k.keys())[0]], obj[list(k.keys())[0]])
        return fval(key, obj)
    else:
        return obj[attrname]

@catch2cn
def ka_call(_type, objname, nextop, usesth):
    """执行动作"""
    if _type is None or _type=="":
        _type = ka_vals[f"{objname}_type"]
    nextops = re.split(r"，", nextop)
    txtemp = lambda x: x if x else ""
    runmatch = _type+ txtemp(usesth) +nextops[0]
    # print("call =>", _type, objname, nextop, runmatch, usesth, ka_callable_foos, file=stderr)
    for k, v in ka_callable_foos.items():
        m = re.match(k, runmatch)
        if m:
            g = m.groups()
            g = [gi if gi else "" for gi in g]
            if len(nextops)>1:#执行后面的语句
                for i in range(1, len(nextops)):
                    #print(nextops[i])
                    g.append(ka_parse(nextops[i]))
            pycallable = v.format(objname, *g)
            #print("call ===>>>", pycallable)
            print2kc(f"# call({_type} {objname} {nextop} {usesth}) => "+pycallable, "ka")
            exec(pycallable)
            return pycallable

@catch2cn
def ka_from_do(_type, objname, nextop):
    """执行从XX做XX的动作"""
    if _type is None or _type=="":
        _type = ka_vals[f"{objname}_type"]
    nextops = re.split(r"，", nextop)
    runmatch = _type +nextops[0]
    # print("from_do =>", _type, objname, nextop, runmatch)
    for k, v in ka_callable_foos.items():
        m = re.match(k, runmatch)
        if m:
            g = m.groups()
            g = [gi if gi else "" for gi in g]
            if len(nextops)>1:#执行后面的语句
                for i in range(1, len(nextops)):
                    #print(nextops[i])
                    g.append(ka_parse(nextops[i]))
            pycallable = v.format(objname, *g)
            #print("call ===>>>", pycallable)
            print2kc(f"# from_do({_type} {objname} {nextop} ) => "+pycallable, "ka")
            exec(pycallable)
            return pycallable

@catch2cn
def ka_rename(newname, keyname):
    """重命名"""
    # print(">>>", newname, keyname)
    if keyname and keyname!="":
        key = None
        fooname = None
        attrname = None
        KA_FOO = r"(ka_\w+)\(\"(\w+)\"\s*,?\s*(?:\"(\w+)\")?\)"
        if re.match(KA_OBJ_VAL, keyname):
            key = re.findall(KA_OBJ_VAL, keyname)[0]
            fooname = ka_sys[KA_OBJ_VAL]
        elif re.match(KA_OBJ_ATTR, keyname):
            key = re.findall(KA_OBJ_ATTR, keyname)[0]
            fooname = ka_sys[KA_OBJ_ATTR]
        elif re.match(KA_FOO, keyname):
            fooname,key,attrname = re.findall(KA_FOO, keyname)[0]
            fooname = f"{fooname}(\"{key}\",\"{attrname}\")" if attrname else f"ka_vals[\"{key}\"]"
        # print("rename=>", key, fooname, attrname)
        ka_vals[newname] = eval(fooname)
        if ka_lastit+"_type" in ka_vals:
            ka_vals[f"{newname}_type"] = ka_vals[f"{key}_type"]
        if key+"_map" in ka_vals:
            ka_vals[f"{newname}_map"] = ka_vals[f"{key}_map"]
    elif ka_lastit in ka_vals:
        # print(ka_lastit, newname)
        ka_vals[newname] = ka_vals[ka_lastit]
        if ka_lastit+"_type" in ka_vals:
            ka_vals[f"{newname}_type"] = ka_vals[f"{ka_lastit}_type"]
        if ka_lastit+"_map" in ka_vals:
            ka_vals[f"{newname}_map"] = ka_vals[f"{ka_lastit}_map"]
        # print(ka_vals)

@catch2cn
def ka_next_do(nextop):
    """执行下一步动作"""
    if ka_lastit in ka_vals:
        # print(ka_lastit, newname)
        objname = ka_lastit
        _type = ka_vals[f"{ka_lastit}_type"]
    nextops = re.split(r"，", nextop)
    runmatch = _type+nextops[0]
    # print("nextdo =>", nextop, runmatch)
    for k, v in ka_callable_foos.items():
        m = re.match(k, runmatch)
        if m:
            g = m.groups()
            g = [gi if gi else "" for gi in g]
            if len(nextops)>1:#执行后面的语句
                for i in range(1, len(nextops)):
                    #print(nextops[i])
                    g.append(ka_parse(nextops[i]))
            pycallable = v.format(objname, *g)
            #print("call ===>>>", pycallable)
            print2kc(f"# nextdo({_type} {objname} {nextop} ) => "+pycallable, "ka")
            exec(pycallable)
            return pycallable

def ka_new_str(name, value):
    value=value.replace("“","\"").replace("”","\"")
    exec(f"ka_vals[\"{name}\"]={value}")
    exec(f"ka_vals[\"{name}_type\"]='字符串'")
    return name

def ka_new_num(name, value):
    exec(f"ka_vals[\"{name}\"]={value}")
    exec(f"ka_vals[\"{name}_type\"]='数'")
    return name

def ka_new_itor(name, value):
    exec(f"ka_vals[\"{name}\"]=ka_parse('{value}')")
    exec(f"ka_vals[\"{name}_type\"]='循环子'")
    return name

@catch2cn
@lastit
def ka_fun_return(foo, keyname):
    # print("==>", foo, keyname)
    key = None
    fooname = None
    attrname = None
    KA_FOO = r"(ka_\w+)\(\"([^\"]+)\"\s*,?\s*(?:\"([^\"]+)\")?\)"
    if re.match(KA_OBJ_VAL, keyname):
        key = re.findall(KA_OBJ_VAL, keyname)[0]
        fooname = ka_sys[KA_OBJ_VAL]
    elif re.match(KA_OBJ_ATTR, keyname):
        key = re.findall(KA_OBJ_ATTR, keyname)[0]
        fooname = ka_sys[KA_OBJ_ATTR]
    elif re.match(KA_FOO, keyname):
        fooname,key,attrname = re.findall(KA_FOO, keyname)[0]
        fooname = f"{fooname}(\"{key}\",\"{attrname}\")" if attrname else f"ka_vals[\"{key}\"]"
    else:
        key = foo
        fooname = keyname
    newname = foo+"结果"
    ka_vals[newname] = eval(fooname)
    if key+"_type" in ka_vals:
        ka_vals[f"{newname}_type"] = ka_vals[f"{key}_type"]
    if key+"_map" in ka_vals:
        ka_vals[f"{newname}_map"] = ka_vals[f"{key}_map"]
    return newname

registType("字符串", ka_new_str)
registType("整数", ka_new_num)
registType("浮点数", ka_new_num)
registType("数字", ka_new_num)
registType("循环子", ka_new_itor)

@catch2cn
@lastit
def ka_new(name, type, value):
    """创建新对象"""
    ka_types[type](name, value)
    return name
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

@catch2cn
def ka_sel(iflist, elsefoo):
    """条件选择"""
    # print(iflist, elsefoo)
    if elsefoo is None or elsefoo=="":
        elsefoo = "pass"
    text = "elif {0}:\n    {1}"
    elsetxt = "else:\n    {0}"
    textline = []
    for con, foo in iflist:
        textline.append(text.format(con, foo))
    textline.append(elsetxt.format(elsefoo))
    ft = "\n".join(textline)[2:]
    # print(ft)
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


