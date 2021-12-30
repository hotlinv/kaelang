# 【映射】
ka_pmap=lambda:{
	u"^当前目录$":"ka_workspace()",
    u"从(.+)(?:读取|加载)(?:本地)?(json|yaml)?数据(?:，)?(?:并)?(?:将其命名为)?“(.+)”":"ka_loadfile('{1}', ka_path('{0}'), '{2}')",
    u"访问(.+)，(?:读取|加载)?数据(?:，)?(?:并)?(?:将其命名)?为“(.+)”":"ka_loadfile(None, ka_path('{0}'), '{1}')",
    u"(?:读取|加载)?(数据描述)“(.+)”":"ka_loadfile(None, os.path.join(ka_workspace(), '{0}', '{1}.yml'), '{1}')",
}

# 【实现】
import os, json, yaml

@catch2cn
def ka_load_urlmaps():
    '''加载路径对应文件'''
    global ka_mount
    f = open("urlmap.yml", 'r',encoding='utf-8')
    y = yaml.load(f, Loader=yaml.FullLoader)
    ka_mount = y
    #把路径加入分词中
    for k, val in y.items():
        jieba.suggest_freq(k, tune=True)
        if val:
            for sk, sv in val.items():
                jieba.suggest_freq(sk, tune=True)


_ka_path_m=re.compile(u"(?:(.[^国]+)国)?(?:(.[^省]+)省)?(?:(.[^市]+)市)?(?:(.[^区县]+)[县|区])?(?:(.+)(?:乡|镇|街道))?(?:(.+)(?:村|社区))?(?:(.+)路)?(?:(.+)号)?(?:(.+)楼)?(?:(.+)(?:室|单元))?(?:(.+)间)?")
@catch2cn
def ka_path(path):
    '''路径分析'''
    mf = [p for p in _ka_path_m.findall(path)[0]]
    #print(">>>", mf)
    t = mf[0]
    ext = mf[10]
    guo = ka_mount[t+"国"]
    mf[1] = guo[mf[1]+"省"]
    mf[9] = f"{mf[9]}.{mf[10]}"
    ospath = [p2 for p2 in mf[1:-1] if p2!=""]
    # print("##", mf, ospath, os.path.join(*ospath))
    return os.path.join(*ospath)

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
    f = open(path, 'r',encoding='utf-8')
    y = yaml.load(f, Loader=yaml.FullLoader)
    ka_vals[name] = y

@catch2cn
def ka_loadfile(type, path, name):
    """加载文件（yaml或json）"""
    if type=="json":
        ka_loadjson(path, name)
    elif type=="yaml":
        ka_loadyaml(path, name)
    elif path.endswith(".yml"):
        ka_loadyaml(path, name)
    elif path.endswith(".json"):
        ka_loadjson(path, name)