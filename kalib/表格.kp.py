# 【引用】pandas、xlrd、openpyxl

# 【映射】
ka_pmap=KaeLevMap(lev0={
	u"访问在(.+)的表格文件(?:中的)?(.+)?(?:表)?，定义为“(.+)”":"ka_pd_open(ka_path('{0}'), '{1}', '{2}')",
    u"把《(.+)》的值输出表格(.+)":"ka_pd_save(ka_path('{1}'), '{0}')",
})

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

@catch2cn
def ka_pd_save(path, name ):
    """保存表格"""
    path = path+"xlsx"
    # print("###", path)
    df = pd.DataFrame(ka_vals[name])
    # def style_func(x):
    #     color='red' if x!="" else ''
    #     return ';'.join([f'background-color:{color}'])
    # df = df.style.applymap(style_func)
    df.to_excel(path,            # 路径和文件名
            sheet_name=name,     # sheet 的名字
            float_format='%.2f',  # 保留两位小数
            na_rep='')     # 空值的显示
