# 【引用】

# 【映射】
ka_pmap=lambda:{
    u"访问(?:在|位于)(.+)的数据“(.+)”":"ka_url_get(ka_url_path('{0}'), '{1}', ka_url_mimetype('{0}'))",
    u"解析(?:文本)?《(.+)》中的对象“(.+)”":"ka_txt2obj('{0}', '{1}')",
}

# 【实现】
import urllib.request as urlreq
import urllib.parse as urlpar

@catch2cn
def ka_url_path(path):
    '''网络路径解析'''
    mf = [p for p in _ka_path_m.findall(path)[0]]
    # print(">>>", mf)
    t = mf[0]
    guo = ka_mount[t+"国"]
    mf[1] = guo[mf[1]+"省"]
    upath = [p2 for p2 in mf[1:-2] if p2!=""]
    # print("##", mf, ospath, os.path.join(*ospath))
    return "/".join(upath)

@catch2cn
def ka_url_mimetype(path):
    '''网络数据mimetype解析'''
    mf = [p for p in _ka_path_m.findall(path)[0]]
    # print(">>>", mf)
    #t = mf[0]
    
    # print("##", mf, ospath, os.path.join(*ospath))
    return mf[-1]

@catch2cn
def ka_url_get(url, vname, mimetype):
    """发送get请求
    """
    # print(url, vname)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    #dict = {'name':'Germey'}

    # data = urllib.parse.urlencode(dict).encode('utf-8')
    # #data参数如果要传必须传bytes（字节流）类型的，如果是一个字典，先用urllib.parse.urlencode()编码。
    #request = urllib.request.Request(url = url,data = data,headers = headers,method = 'POST')
    request = urlreq.Request(url)
    response = urlreq.urlopen(request)
    ht = response.read().decode('utf-8')
    ka_vals[vname] = ht
    ka_vals[vname+"_type"] = mimetype


@catch2cn
def ka_txt2obj(txtname, objname):
    """将txt里的json解析成对象"""
    import json
    txt = ka_vals[txtname]
    m = re.search(r"\{|\[",txt)
    if m:
        c = txt[m.span()[0]:m.span()[1]]
        if c=="{":
            e = txt.rfind("}")
        if c=="[":
            e = txt.rfind("]")
        obj = json.loads(txt[m.span()[0]:e+1])
        ka_vals[objname] = obj
        ka_vals[objname+"_type"] = "对象"

