from kae.annotations import ka_setobj_rename
from kae import ka_path_m as _ka_path_m
from kae import ka_mount, ka_vals

@ka_setobj_rename(cntype="爬虫", entype="netbug")
class KNetbug:
    def __init__(self, urlpath):
        
        self.parseurl(urlpath)
    def parseurl(self, path):
        '''网络路径解析'''
        mf = [p for p in _ka_path_m.findall(path)[0]]
        # print(">>>", mf)
        t = mf[0]
        guo = ka_mount[t+"国"]
        mf[1] = guo[mf[1]+"省"]
        upath = [p2 if p2 not in ka_vals else ka_vals[p2] for p2 in mf[1:-2] if p2!=""]
        # print("##", mf, ospath, os.path.join(*ospath))
        return "/".join(upath)

    def mimetype(self, path):
        '''网络数据mimetype解析'''
        mf = [p for p in _ka_path_m.findall(path)[0]]
        return mf[-1]

    def method(self, path):
        '''网络数据请求方法解析'''
        # print(path)
        METHODS = {"查询":"GET", "更新":"PUT", "新建":"POST", "删除":"DELETE"}
        mf = [p for p in _ka_path_m.findall(path)[0]]
        return METHODS[mf[-2]]

    def mimetype(self, mimetype, txt):
        """根据mimetype建立对应对象"""
        if mimetype=="文本":
            return txt, mimetype
        elif mimetype.lower()=="json":
            import json
            return json.loads(txt), "对象"
        elif mimetype.lower()=="xml":
            import xmltodict
            return xmltodict.parse(txt), "对象"
        return txt, mimetype

    def call(self, url, vname, method, mimetype, dataname):
        """发送网络请求
        """
        import urllib.request as urlreq
        import urllib.parse as urlpar
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        #dict = {'name':'Germey'}
        if dataname:
            dic = ka_vals[dataname]
            dargs = urlpar.urlencode(dic).encode('utf-8')
        # #data参数如果要传必须传bytes（字节流）类型的，如果是一个字典，先用urllib.parse.urlencode()编码。
        #request = urllib.request.Request(url = url,data = data,headers = headers,method = 'POST')
        reqdic = {"url": url}
        if dataname:
            reqdic["data"] = dargs
        if method!="GET":
            reqdic["method"]=method
        # print("get==>", reqdic)
        request = urlreq.Request(**reqdic)
        response = urlreq.urlopen(request)
        ht = response.read().decode('utf-8')
        nht,mt = self.ka_mimetype(mimetype, ht)
        ka_vals[vname] = nht
        ka_vals[vname+"_type"] = mt

    def txt2obj(self, txtname, objname):
        """将txt里的json解析成对象"""
        import json,re
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

