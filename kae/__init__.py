

ka_mount = {} #放数据配置(目录,环境等）

ka_fext = {} #放数据扩展名

ka_vals = {} #放变量

ka_valtypes = {} #放变量类型

ka_modules = {}# 放模块路径对应map

ka_dataname_class_map = {} #放数据名称对应

import re
ka_path_m=re.compile(u"(?:(.[^国]+)国)?(?:(.[^省]+)省)?(?:(.[^市]+)市)?(?:(.[^区县]+)[县|区])?(?:(.+)(?:乡|镇|街道))?(?:(.+)(?:村|社区))?(?:(.+)路)?(?:(.+)号)?(?:(.+)楼)?(?:(.+)(?:室|单元))?(?:(.+)间)?")


def fromnetgetbin(serv, source):
    # 请求
    import requests
    import urllib.parse
    # 定义请求的URL
    url = f"http://{serv}/kaeear"

    # 定义请求头和数据
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"say": "\n".join(source)}
    # print(data)
    data = urllib.parse.urlencode(data)

    # 发送POST请求并获取响应
    response = requests.post(url, headers=headers, data=data)

    # 打印响应内容
    if response.status_code==200:
        bincode = response.content.decode()
        pos = bincode.index(":")
        binfn, pycallable = bincode[:pos], bincode[pos+1:]
    else:
        pycallable = ""
    return pycallable


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
    import os
    import hashlib
    sp = os.path.join("功能单元", ka_foos[name]+".ae")
    # print(sp)
    with open(sp, "r", encoding="utf-8") as ss:
        source = ss.read()
    hl = hashlib.md5()
    hl.update(name.encode("utf-8"))
    modelname = f"m{hl.hexdigest()}"
    if not os.access("modbin", os.F_OK):
        os.mkdir("modbin")
    if not os.access("modbin/__init__.py", os.F_OK):
        if "mknod" in dir(os):
            os.mknod("modbin/__init__.py")
        else:
            open("modbin/__init__.py",'w').close()
    with open(os.path.join("modbin", f"{modelname}.py"), "w", encoding="utf-8") as af:
        preblock = "    "
        lines = ["from kae.annotations import ka_return_rename",
            f"from kae.libs.sys import newobj,getobj",
            f"@ka_return_rename",
            f"def K{name}():",
            f"{preblock}print('{name}', 'is', 'run')",
            f"{preblock}newobj('整数', '{name}_ret', 100)",
        ]
        serv = "localhost"
        if "运行时" in ka_mount and "服务器" in ka_mount["运行时"]:
            serv = ka_mount["运行时"]["服务器"]
        pycallable = fromnetgetbin(serv, source)
        for cmdline in pycallable.splitlines():
            if r"%fooname%" in cmdline:
                cmdline = cmdline.replace(r"%fooname%", name) #把函数名换成现在函数的名字
            lines.append(preblock+cmdline)
        lines.append(f"{preblock}return getobj('{name}_ret')")
        af.writelines([ w+"\n" for w in lines])
    # import importlib
    # m = importlib.import_module(f'modbin.{modelname}')
    # print(f'modbin.{modelname}')
    m = __import__(f'modbin.{modelname}', fromlist=["modbin"])
    return m

def fooreturn(fooname, val):
    from kae.libs.sys import newobj
    newobj(None, fooname+"_ret", val)

def runfoo(name):
    '''运行函数'''
    if name in ka_foos:
        ka_foos[name]()
        return True
    return False
