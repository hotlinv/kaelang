from kae.annotations import ka_setobj_rename

@ka_setobj_rename
class AnyDB:
    def open(self, filename):
        self.filename = filename
        from kae.libs.sys import fpath
        self.infile = fpath(filename)
        self.db = self._read(self.infile)
        return self
    def _read(self, filename):
        import pandas as pd
        from kae import ka_fext
        fexts = ka_fext.values()
        fex = [ex for ex in fexts if filename.endswith("."+ex)]
        if len(fex)>0: 
            #pd.read_sql
            return eval(f"pd.read_{fex[0]}('{filename}')")
        else:
            print("未知的数据表格格式")
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
            self.fieldconf = yaml.load(yf, Loader=yaml.FullLoader)
    def query(self, q):
        print(q)