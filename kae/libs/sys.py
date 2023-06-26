from math import *
from kae.annotations import ka_setobj_rename, ka_datasource

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


def importmod(modename):
    '''导入模块'''
    from kae import ka_modules
    print(ka_modules)
    impm = compile(f"import {ka_modules[modename]}", "导入", "exec")
    try:
        exec(impm, globals())
    except:
        raise Exception(f"导入依赖库{ka_modules[modename]}失败")
    # exec(f"import {}", globals())
    # print(kae.libs.narray)

@ka_setobj_rename("整数", "int")
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

@ka_setobj_rename("浮点数", "float")
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

@ka_setobj_rename("字符串", "str")
class KStr:
    def __init__(self, val):
        self.val = val
        self.type = str
        if val is not None:
            self.val = str(val)
    def set(self, val):
        self.val = val
    def __str__(self) -> str:
        return self.val

@ka_setobj_rename("数组", "list")
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

def newobj(type, name, val):
    '''新建变量'''
    from kae import ka_vals, ka_valtypes
    objtype = type
    if objtype in ka_valtypes.keys():
        objtype = ka_valtypes[objtype]
    # print(globals())
    # print(kae.libs.narray)
    ka_vals[name] = eval(f"{objtype}({val})")
    return ka_vals[name]

def getobj(name):
    '''获取变量'''
    from kae import ka_vals
    if hasattr(ka_vals[name], "val"):
        return ka_vals[name].val
    return ka_vals[name]

def getattr(name, attr):
    '''获取变量属性'''
    from kae import ka_vals
    obj = ka_vals[name]
    if "val" in ka_vals[name]:
        obj = ka_vals[name]["val"]
    if hasattr(ka_vals[name], "val"):
        obj = ka_vals[name].val
    
    if type(obj)==dict:
        return obj[attr]
    else: 
        print(obj)
        return eval(f"obj.{attr}")

from kae.common import dict2obj

@ka_setobj_rename(cntype="结构化数据", entype="anyStream")
def StructuredData(path,  varname, queryname=None):
    '''可以打开任何流，包括文件，网络'''
    # self.varname= varname
    from kae import ka_path_m , ka_dataname_class_map
    mf = [p for p in ka_path_m.findall(path)[0]]
    # print(">>>", mf)
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

def multiply(a, b):
    '''乘法'''
    return a*b