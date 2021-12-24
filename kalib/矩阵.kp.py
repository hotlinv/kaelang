# 【引用】numpy

# 【映射】
ka_pmap=lambda:{
    u"从“(.+)”(?:读取|加载)(?:本地)?矩阵文件(?:，)?(?:并)?(?:将其命名为)?“(.+)”":"ka_numpy_loadtxt(ka_path('{0}'), '{1}')",
    u"把矩阵《(.+)》输出：(.+)":"ka_numpy_savetxt('{0}', ka_path('{1}'))",
}

# 【实现】
import numpy as np

_ka_matmode=re.compile(u"模式为(\w+)")
_ka_matshape=re.compile(u"(?:大小|尺寸)?为(\d+)(?:行)?\s*(\d+)(?:列)?")
_mat_modes = {"整形":"int", "正整形":"uint", "浮点型":"float"}

@catch2cn
def mat_getmode(name):
    if name in _mat_modes:
        return _mat_modes[name]
    else:
        return name

@catch2cn
def ka_new_zeros(name, value):
    """新建全0矩阵"""
    mm = _ka_matmode.findall(value)
    sm = _ka_matshape.findall(value)
    ka_vals[name]=np.zeros(tuple([int(s) for s in sm[0]]), dtype=mat_getmode(mm[0]))
    ka_vals[f"{name}_type"]="矩阵"

@catch2cn
def ka_new_ones(name, value):
    """新建全1矩阵"""
    mm = _ka_matmode.findall(value)
    sm = _ka_matshape.findall(value)
    ka_vals[name]=np.ones(tuple([int(s) for s in sm[0]]), dtype=mat_getmode(mm[0]))
    ka_vals[f"{name}_type"]="矩阵"

registType("全0矩阵", ka_new_zeros)
registType("全1矩阵", ka_new_ones)

@catch2cn
def ka_numpy_loadtxt(path, name):
    """加载矩阵文本文件"""
    ka_vals[name] = np.loadtxt(path)

@catch2cn
def ka_numpy_savetxt(mn, path):
    """保存矩阵文本文件"""
    path = path+"npt"
    np.savetxt(path, ka_vals[mn])