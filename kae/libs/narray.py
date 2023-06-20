

from kae.annotations import ka_setobj_rename

_mat_modes = {"整数":"int", "正整数":"uint", "浮点数":"float"}

def mat_getmode(name):
    if name in _mat_modes:
        return _mat_modes[name]
    else:
        return name


@ka_setobj_rename(cntype="矩阵", entype="narray")
class KNarray:
    def __init__(self, arr):
        if arr is not None:
            import numpy as np
            self.val = np.array(arr)
    def setshape(self, shape):
        import re
        yc = re.findall("(\d+)行", shape) 
        xc = re.findall("(\d+)列", shape) 
        self.shape = (int(yc[0]), int(xc[0]))
        return self
    def setmode(self, mode):
        self.mode = mat_getmode(mode)
        return self
    def set(self, val):
        import numpy as np
        if type(val) == int or type(val)==float:
            self.val = np.zeros(self.shape, dtype=self.mode)+val
        return self
    def saveas(self, path):
        from kae.libs.sys import fpath
        from kae import ka_fext
        import numpy as np
        outfile = fpath(path)
        np.savetxt(outfile, self.val)


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