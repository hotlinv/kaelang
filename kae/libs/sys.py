from math import *
from kae.annotations import ka_setobj_rename, ka_datasource
from kae.common import Dict as KDict

def cacl(ev):
    return eval(ev)

import re, os
from kae import ka_path_m as _ka_path_m

def fpath(path):
    '''路径分析'''
    from kae import ka_mount, ka_fext
    fext = lambda name: ka_fext[name+"间"]
    # print(ka_mount)
    mf = [p for p in _ka_path_m.findall(path)[0]]
    #print(">>>", mf)
    t = mf[0]
    ext = mf[10]
    guo = ka_mount[t+"国"]
    mf[1] = guo[mf[1]+"省"]
    mf[9] = f"{mf[9]}.{fext(mf[10])}"
    ospath = [p2 for p2 in mf[1:-1] if p2!=""]
    # print("##", mf, ospath, os.path.join(*ospath))
    return os.path.expanduser(os.path.join(*ospath))


def importmod(*modenames):
    '''导入模块'''
    from kae import ka_modules
    # print(ka_modules)
    for modename in modenames:
        impm = compile(f"import {ka_modules[modename]}", "导入", "exec")
        try:
            exec(impm, globals())
        except:
            raise Exception(f"导入依赖库{ka_modules[modename]}失败")
    # exec(f"import {}", globals())
    # print(kae.libs.narray)

@ka_setobj_rename(cntype="整数", entype="int")
class KInt:
    def __init__(self, val):
        self.val = val
        self.type = int
        if val is not None:
            self.val = int(val)
    def set(self, val):
        self.val = val
    def __str__(self) -> str:
        return str(self.val)

@ka_setobj_rename(cntype="浮点数", entype="float")
class KFloat:
    def __init__(self, val):
        self.val = val
        self.type = float
        if val is not None:
            self.val = float(val)
    def set(self, val):
        self.val = val
    def __str__(self) -> str:
        return str(self.val)

@ka_setobj_rename(cntype="字符串", entype="str")
class KStr:
    def __init__(self, val):
        self.val = val
        self.type = str
        if val is not None:
            if type(val)==bytes:
                self.val = val.decode("utf-8")
            else:
                self.val = str(val)
    def set(self, val):
        if type(val)==bytes:
            self.val = val.decode("utf-8")
        else:
            self.val = str(val)
    def __str__(self) -> str:
        return self.val

@ka_setobj_rename(cntype="数组", entype="list")
class KList:
    def __init__(self, val):
        self.val = val
        self.type = str
        if val is not None:
            self.val = list(val)
        else:
            self.val = []
    def set(self, val):
        self.val = val
    def __str__(self) -> str:
        return str(self.val)

def newobj(vtype, name, val):
    '''新建变量'''
    from kae import ka_vals, ka_valtypes
    objtype = vtype
    if objtype is None: #不一定都能直接确定数据类型，可能需要靠val猜。
        if val is None:
            objtype = "字符串"
        if hasattr(val, "cntype"):
            objtype = val.cntype
        elif val is not None:
            ot = type(val).__name__
            regtypes = [it for it in ka_valtypes.values()]
            ts = [rt for rt in regtypes if (lambda s, s2: s.lower().endswith("k"+s2))(rt, ot)]
            if len(ts)>0:
                objtype = [k for k, v in ka_valtypes.items() if v==ts[0]][0]
        
    if objtype in ka_valtypes.keys():
        objtype = ka_valtypes[objtype]
    # print(globals())
    # print(kae.libs.narray)
    # __import__(".".join(objtype.split(".")[:-1]), fromlist=["kae"])
    pack = ".".join(objtype.split(".")[:-1])
    tn = objtype.split(".")[-1]
    exec(f'from {pack} import {tn}')
    # eval("KInt(None)")
    # print(vtype, name, val, f"{tn}({val})")
    ka_vals[name] = eval(f"{tn}({val})")
    ka_vals[name].varname = name
    return ka_vals[name]

def wapperobj(clsname, dataname):
    """把变量的属性名进行对应（英转中）"""
    from kae import ka_vals
    ka_vals[dataname]["__desc__"] = ka_vals[clsname].val

def setattr(objname, attrname, obj):
    """设置对象属性"""
    from kae import ka_vals
    if "__desc__" in ka_vals[objname]:
        attrname = ka_vals[objname]["__desc__"][attrname]
    # print("set_attr", objname, ".", attrname, "=>", obj)
    # if re.match(r"^ka_\w+(.+)$", obj):
    #     ka_vals[objname][attrname] = eval(obj)
    # elif re.match(r"^\d+", obj):
    #     ka_vals[objname][attrname] = re.findall(r"\d+",obj)[0]
    # else:
    ka_vals[objname]["val"][attrname] = obj
    # print(ka_vals[objname])

def createobj(descname, name):
    '''新建变量'''
    from kae import ka_vals
    desc = ka_vals[descname]
    ka_vals[name] = dict2obj({"__desc__": desc.val, "val":{}})
    return ka_vals[name]

def getobj(name,default=None):
    '''获取变量'''
    from kae import ka_vals
    if name in ka_vals:
        obj = ka_vals[name]
    else:
        #如果是局部变量，就获取到我的调用者
        import sys
        callingframe = sys._getframe(1)
        caller = callingframe.f_locals['self']
        name = "arg"+name
        if hasattr(caller, name):
            obj = getattr(caller, name)
        else:
            obj = default
    # print(obj)
    if obj is not None and hasattr(obj, "val"):
        return obj.val
    return obj

def kgetattr(name, attr):
    '''获取变量属性'''
    from kae import ka_vals
    if name in ka_vals:
        obj = ka_vals[name]
    else:
        #如果是局部变量，就获取到我的调用者
        import sys
        callingframe = sys._getframe(1)
        caller = callingframe.f_locals['self']
        name = "arg"+name
        obj = getattr(caller, name)

    # print(obj, ka_vals[name], attr)
    if "__desc__" in obj: #获取属性中英对照表
        if attr in obj["__desc__"].keys():
            attr = obj["__desc__"][attr]

    if "val" in obj:
        obj = obj["val"]
    try:
        if hasattr(obj, "val"):
            obj = obj.val
    except:
        pass

    # print(obj, attr)
    # print("XX"*10, attr, type(attr))
    
    if type(attr) == str:
        if type(obj)==dict:
            return obj[attr]
        else: 
            # print(obj)
            return eval(f"obj.{attr}")
    elif type(attr) == dict or type(attr)==KDict:
        #那么这个obj肯定也是一个dict了
        return _loopattr(obj, attr)
    
def _loopattr(obj, attr):
    if type(attr)==str:
        return obj[attr]
    key = list(attr.keys())[0]
    val = obj[key]
    # print(key, val)
    if type(attr[key])==dict or type(attr)==KDict:
        return _loopattr(val, attr[key])
    else:
        # print(val[attr[key]])
        return val[attr[key]]
    
def convert2str(name):
    obj = getobj(name)
    if hasattr(obj, "val"):
        obj = obj.val
    s = obj
    if hasattr(obj, "tostr"):
        s = obj.tostr()
    return KStr(str(s))

def slice(name, posarr):
    obj = getobj(name)
    return KStr(eval(f"obj[{posarr[0]}:{posarr[1]}]"))

def lslicepos(num):
    return (0, num)

def rslicepos(num):
    return (-num, None)

def ipos(num):
    return (num)

from kae.common import dict2obj

@ka_setobj_rename(cntype="结构化数据", entype="anyStream")
def StructuredData(path,  varname, queryname=None):
    '''可以打开任何流，包括文件，网络'''
    # self.varname= varname
    if path is None or path=="None":
        path = f"磁颐国构申省{varname}室另类标记间"
    from kae import ka_path_m , ka_dataname_class_map
    mf = [p for p in ka_path_m.findall(path)[0]]
    # print(">>>", mf, ka_dataname_class_map)
    t = mf[0]
    cls = ka_dataname_class_map[t+"国"]
    
    print(cls, path, varname)
    obj = eval(f"{cls}('{path}')")
    data, dt = obj.readdata(queryname)
    from kae import ka_vals
    ka_vals[varname] = dict2obj({"val":data, "type":dt})
    # if varname is not None:
    #     obj.renameme(varname)
    # print("c"*10, cls)

    # def setmeta(self, meta):
    #     self.meta = meta
    return obj

ASC = "ASC"
DESC = "DESC"

def multiply(a, b):
    '''乘法'''
    return a*b

@ka_setobj_rename(cntype="任务", entype="task")
class KTask:
    def __init__(self, val):
        pass

    def taskfoo(self, foo):
        self.foo = foo
        return self
    
    def go(self, count):
        for i in range(count):
            self.itor = i+1
            self.foo(self)
        
    def set(self, val):
        return self

    def __str__(self) -> str:
        return self.val