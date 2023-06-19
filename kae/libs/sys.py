from math import *
from kae.annotations import ka_setobj_rename

def cacl(ev):
    return eval(ev)

import re, os
_ka_path_m=re.compile(u"(?:(.[^国]+)国)?(?:(.[^省]+)省)?(?:(.[^市]+)市)?(?:(.[^区县]+)[县|区])?(?:(.+)(?:乡|镇|街道))?(?:(.+)(?:村|社区))?(?:(.+)路)?(?:(.+)号)?(?:(.+)楼)?(?:(.+)(?:室|单元))?(?:(.+)间)?")

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
    print(kae.libs.narray)

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

def multiply(a, b):
    '''乘法'''
    return a*b