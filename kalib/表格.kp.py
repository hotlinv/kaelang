# 【引用】pandas、xlrd、xlwt

# 【映射】
ka_pmap=lambda:{
	u"打开在(.+)的表格文件(?:中的)?(.+)?(?:表)?，命名为“(.+)”":"ka_pd_open(ka_path('{0}'), '{1}', '{2}')",
}

# 【实现】
import pandas as pd

@catch2cn
def ka_pd_open(path, tab, name ):
    """打开表格"""
    #ka_vals[name] = Image.open(path)
    if tab:
        ef = pd.read_excel(path, sheet_name = tab) 
    else:
        ef = pd.read_excel(path)# sheet_name不指定时默认返回全表数据
    df = pd.DataFrame(ef)
    ka_vals[name] = df
