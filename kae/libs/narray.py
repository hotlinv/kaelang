

from kae.annotations import ka_setobj_rename

_mat_modes = {"整形":"int", "正整形":"uint", "浮点型":"float"}

def mat_getmode(name):
    if name in _mat_modes:
        return _mat_modes[name]
    else:
        return name

@ka_setobj_rename("矩阵")
class NArray:
    def __init__(self, arr):
        self.arr = arr
    def saveas(self, path):
        from kae.libs.sys import fpath
        from kae import ka_fext
        import numpy as np
        outfile = fpath(path)
        np.savetxt(outfile, self.arr)


def create_zeros(size, mode):
    """新建全0矩阵"""
    import numpy as np
    arr=np.zeros(tuple([int(s) for s in size]), dtype=mat_getmode(mode))
    return NArray(arr)

def create_ones(size, mode):
    """新建全1矩阵"""
    import numpy as np
    arr=np.ones(tuple([int(s) for s in size]), dtype=mat_getmode(mode))
    return NArray(arr)

def load_numpy_txt(path):
    """加载矩阵文本文件"""
    import numpy as np
    arr = np.loadtxt(path)
    return NArray(arr)

# def ka_numpy_savetxt(mn, path):
#     """保存矩阵文本文件"""
#     path = path+"npt"
#     np.savetxt(path, ka_vals[mn])