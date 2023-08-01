from kae.annotations import ka_setobj_rename, ka_datasource

@ka_setobj_rename(cntype="记录集")
class KTableResultSet:
    def __init__(self, rs, fc, rfc):
        self.db = rs
        self.fieldconf = fc
        self.rfieldconf = rfc
    def __str__(self):
        # print("ssssss", self.db.size)
        if self.db.size==1:
            return str(self.db.iloc[0])
        return str(self.db)
    def iloc(self, i):
        return self.db.iloc[i]
    def saveas(self, path):
        from kae.libs.sys import fpath
        from kae import ka_fext
        outfile = fpath(path)
        fexts = ka_fext.values()
        # print(fexts)
        fex = [ex for ex in fexts if ex is not None and outfile.endswith("."+ex)]
        if len(fex)>0: 
            #pd.read_sql
            eval(f"self.db.to_{fex[0]}('{outfile}')")
        else:
            print("未知的数据表格格式")

ka_pandas_foo = {"xlsx":"excel", "xls":"excel"}
ka_pandas_engine = {"xlsx":"openpyxl"}

class TabQuery:
    def __init__(self, tab, fieldconf, rfieldconf):
        self.init = False
        self.tab = tab
        self.fieldconf = fieldconf
        self.rfieldconf = rfieldconf
    def orderby(self, ofield, aord):
        self.ofield = ofield
        self.aord = aord
        return self
    def queryend(self, limits, *rfs):
        import kae
        self.init = True
        ret = self.tab
        if self.ofield:
            ret = ret.sort_values(by=self.rfieldconf[self.ofield], ascending=(self.aord==kae.libs.sys.ASC))
        if limits:
            ret = ret.iloc[int(limits[0]):int(limits[1]), :]
        if len(rfs)>0:
            # print(rfs, self.rfieldconf)
            ret = ret[[self.rfieldconf[f] for f in rfs]]
        return KTableResultSet(ret, self.fieldconf, self.rfieldconf)


@ka_setobj_rename(cntype="表格")
@ka_datasource("库源国")
class KAnyDB:
    def __init__(self, filename):
        self.filename = filename
        from kae.libs.sys import fpath
        self.infile = fpath(filename)
        self.db = self._read(self.infile)
    def _read(self, filename):
        import pandas as pd
        from kae import ka_fext
        fexts = ka_fext.values()
        # print(fexts)
        fex = [ex for ex in fexts if ex is not None and filename.endswith("."+ex)]
        if len(fex)>0: 
            readfoo = fex[0]
            if readfoo in ka_pandas_foo:
                readfoo = ka_pandas_foo[readfoo]
            #pd.read_sql
            engop = ""
            if fex[0] in ka_pandas_engine:
                engop = f", engine='{ka_pandas_engine[fex[0]]}'"
            return eval(f"pd.read_{readfoo}('{filename}' {engop})")
        else:
            print("未知的数据表格格式")
    def __str__(self):
        return str(self.db)
    def kacb_setobjNameOK(self):
        # 设置变量名的回调
        from kae import ka_mount
        import os, yaml
        confpath = "./"
        if "磁颐国" in ka_mount:
            if "构申省" in ka_mount["磁颐国"]:
                confpath = ka_mount["磁颐国"]["构申省"]
        conffile = os.path.join(confpath, self.objname+".yml")
        #解析字段对应 
        with open(conffile, 'r',encoding='utf-8') as yf:
            self.fieldconf = yaml.load(yf, Loader=yaml.FullLoader) # 字段 英文:中文
            self.rfieldconf = {v:k for k,v in self.fieldconf.items()} # 字段 中文:英文
    def query(self, q, qname):
        if qname is not None:
            import kae
            qobj = kae.libs.sys.getobj(qname, TabQuery(self.db, self.fieldconf, self.rfieldconf))
            return qobj
        print(q)
        import re
        ret = self.db
        regexall = r"(?:所有)?(.+)的((?:[^、]+(?:、|等)?)*)记录(?:中的?第(\d+)[行条]的?信息){0,1}(?:中的?前(\d+)[行条]的?信息){0,1}"
        regex = r"([^、等]+)(?:、|等){0,1}"

        matches = re.findall(regexall, q)
        matches2 = re.findall(regex, matches[0][1])

        con = matches[0][0]
        if con in self.rfieldconf.keys(): #不含条件
            res = [matches[0][0]]
            res.extend(matches2)
            if len(res)>0:
                ret = self.db[[self.rfieldconf[f] for f in res]]
        else:# 条件表达式
            tab = self.db
            fs = []
            fs.extend(matches2)
            for key, val in self.rfieldconf.items():
                con = con.replace(key, f"tab['{val}']")
            # print(con, fs)
            res = eval(con)
            # print(res)
            ret = tab[res]
            if len(fs)>0:
                ret = ret[[self.rfieldconf[f] for f in fs]]
        if len(matches[0])>1: 
            print(matches)
            iloc = matches[0][2]
            if iloc != "":
                ret = ret.iloc[int(iloc), :]
            leftloc = matches[0][3]
            if leftloc != "":
                ret = ret.iloc[:int(leftloc), :]
        
        return KTableResultSet(ret, self.fieldconf, self.rfieldconf)
    def saveas(self, path):
        from kae.libs.sys import fpath
        from kae import ka_fext
        outfile = fpath(path)
        fexts = ka_fext.values()
        # print(fexts)
        fex = [ex for ex in fexts if ex is not None and outfile.endswith("."+ex)]
        if len(fex)>0: 
            #pd.read_sql
            eval(f"self.db.to_{fex[0]}('{outfile}')")
        else:
            print("未知的数据表格格式")