# 【映射】
ka_pmap=lambda:{
	u"^当前目录$":"ka_workspace()",
    u"从“(.+)”(?:读取|加载)(?:本地)?(json|yaml)文件(?:，)?(?:并)?(?:将其命名为)?“(.+)”":"ka_loadfile('{1}', '{0}', '{2}')"
}

# 【实现】
import os, json, yaml

@catch2cn
def ka_workspace():
    """获取当前目录"""
    return os.path.abspath(os.path.curdir)

@catch2cn
def ka_loadjson(path, name):
    """加载json文件"""
    with open(path, "r") as read_file:
        j = json.load(read_file)
        ka_vals[name] = j

@catch2cn
def ka_loadyaml(path, name):
    """加载文件（yaml或json）"""
    f = open(path)
    y = yaml.load(f, Loader=yaml.FullLoader)
    ka_vals[name] = y

@catch2cn
def ka_loadfile(type, path, name):
    """加载文件（yaml或json）"""
    if type=="json":
        ka_loadjson(path, name)
    elif type=="yaml":
        ka_loadyaml(path, name)