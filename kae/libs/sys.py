from math import *

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

def newobj(type, name, val):
    '''新建变量'''
    from kae import ka_vals
    ka_vals[name] = val
    return name

def getobj(name):
    '''获取变量'''
    from kae import ka_vals
    return ka_vals[name]
