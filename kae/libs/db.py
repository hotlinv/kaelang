
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