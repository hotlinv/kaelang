

ka_mount = {} #放数据配置(目录,环境等）

ka_fext = {} #放数据扩展名

ka_vals = {} #放变量

ka_valtypes = {} #放变量类型

ka_modules = {}# 放模块路径对应map

ka_dataname_class_map = {} #放数据名称对应

import re
ka_path_m=re.compile(u"(?:(.[^国]+)国)?(?:(.[^省]+)省)?(?:(.[^市]+)市)?(?:(.[^区县]+)[县|区])?(?:(.+)(?:乡|镇|街道))?(?:(.+)(?:村|社区))?(?:(.+)路)?(?:(.+)号)?(?:(.+)楼)?(?:(.+)(?:室|单元))?(?:(.+)间)?")

ka_foos = {}

class Foo:
    '''函数实现类'''
    def __init__(self, fname):
        self.name = fname
    def foo(self, sourcename):
        '''指定函数体'''
        ka_foos[self.name] = sourcename
    
        
        

def deffoo(name):
    '''定义函数'''
    return Foo(name)

def isnamedfoo(name):
    return name in ka_foos

def mkmodule(name):
    '''编译源码'''
    import os.path
    import hashlib
    sp = os.path.join("功能单元", ka_foos[name]+".ae")
    print(sp)
    hl = hashlib.md5()
    hl.update(name.encode("utf-8"))
    modelname = f"m{hl.hexdigest()}"
    with open(os.path.join("modbin", modelname+".py"), "w", encoding="utf-8") as af:
        lines = ["from kae.annotations import ka_setobj_rename",
            f"@ka_setobj_rename(cntype='整数', entype='int')",
            f"def {name}():",
            f"  print('{name}', 'is', 'run')",
            f"  return 1000"
        ]
        af.writelines([ w+"\n" for w in lines])
    # import importlib
    # m = importlib.import_module(f'modbin.{modelname}')
    m = __import__(f'modbin.{modelname}', fromlist=["modbin"])
    return m

def runfoo(name):
    '''运行函数'''
    if name in ka_foos:
        ka_foos[name]()
        return True
    return False
