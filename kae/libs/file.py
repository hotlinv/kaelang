from kae.annotations import ka_setobj_rename, ka_datasource
from kae import ka_path_m as _ka_path_m
from kae import ka_mount, ka_vals, ka_fext
import os

@ka_setobj_rename(cntype="文本文件")
@ka_datasource("磁颐国") 
class KTextFile:
    def __init__(self, urlpath):
        self.path = self.parseurl(urlpath)
        self.mt = self.urlmimetype(urlpath)
    def parseurl(self, path):
        '''文件路径解析'''
        # mf = [p for p in _ka_path_m.findall(path)[0]]
        # # print(">>>", mf)
        # t = mf[0]
        # guo = ka_mount[t+"国"]
        # mf[1] = guo[mf[1]+"省"]
        # upath = [p2 if p2 not in ka_vals else ka_vals[p2] for p2 in mf[1:-1] if p2!=""]
        # # print("##", mf, ospath, os.path.join(*ospath))
        # return "/".join(upath)

        mf = [p for p in _ka_path_m.findall(path)[0]]
        #print(">>>", mf)
        t = mf[0]
        ext = mf[10]
        guo = ka_mount[t+"国"]
        mf[1] = guo[mf[1]+"省"]
        ext = ka_fext[mf[10]+"间"]
        mf[9] = f"{mf[9]}.{ext}"
        ospath = [p2 for p2 in mf[1:-1] if p2!=""]
        # print("##", mf, ospath, os.path.join(*ospath))
        return os.path.expanduser(os.path.join(*ospath))
    def urlmimetype(self, path):
        '''数据格式解析'''
        mf = [p for p in _ka_path_m.findall(path)[0]]
        return mf[-1]
    def readdata(self, query):
        """读取数据"""
        with open(self.path, 'r',encoding='utf-8') as file:
            txt = file.read()
            print(txt)
            if self.mt=="文本":
                return txt, self.mt
            elif self.mt=="另类标记":
                import yaml
                y = yaml.load(txt, Loader=yaml.FullLoader)
                return y, "对象"
            elif self.mt.lower()=="json":
                import json
                return json.loads(txt), "对象"
            elif self.mt.lower()=="xml":
                import xmltodict
                return xmltodict.parse(txt), "对象"
            return txt, "文本"