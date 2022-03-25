# 【引用】PIL、numpy、scipy

# 【映射】
ka_pmap=KaeLevMap(lev0={
	#u"把图像《(.+)》切割成多个矩形“(.+)”":"ka_imga_splitrect('{0}', '{1}')",
    #u"对图像《(.+)》运行最小值滤波操作，(.+)":"ka_imga_minimum_filter('{0}', '{1}')"
})

# 【实现】
from PIL import Image
from PIL import ImageDraw
from scipy import ndimage, misc

@catch2cn
@lastit
def ka_imga_splitrect(imgname):
    """图像切割
    [k]图像(?:进行|执行)?(?:切割|切分)·'{0}'
    """
    import ima
    img = ka_vals[imgname]
    ka_vals[imgname+"切割后"] = ima.splitRects(img)
    ka_vals[f"{imgname}切割后_type"] = "图像"
    return f"{imgname}切割后"
    

_ka_imga_window_size=re.compile(u"窗口大小为(\d+)")

@catch2cn
@lastit
def ka_imga_minimum_filter(imgname, param):
    """图像最小滤波操作
    [k]图像(?:进行|执行)?最小值滤波操作·'{0}','{1}'
    """
    ws = _ka_imga_window_size.findall(param)
    # print(ws)
    # ascent = misc.ascent()
    result = ndimage.minimum_filter(ka_vals[imgname], size=int(ws[0]))
    ka_vals[imgname+"最小滤波后"]=result
    ka_vals[f"{imgname}最小滤波后_type"] = "图像"
    return imgname+"最小滤波后"
