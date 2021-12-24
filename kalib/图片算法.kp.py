# 【引用】PIL、numpy、scipy

# 【映射】
ka_pmap=lambda:{
	u"将图(?:像|片)《(.+)》切割成多个矩形“(.+)”":"ka_imga_splitrect('{0}', '{1}')",
    u"对图像《(.+)》运行最小值滤波操作，(.+)":"ka_imga_minimum_filter('{0}', '{1}')"
}

# 【实现】
from PIL import Image
from PIL import ImageDraw
from scipy import ndimage, misc
# import ima

def ka_imga_splitrect(imgname, rectname):
    # img = ka_vals[imgname]
    # print(ima.splitRects(img))
    pass

_ka_imga_window_size=re.compile(u"窗口大小为(\d+)")

@catch2cn
def ka_imga_minimum_filter(imgname, param):
    """图像最小滤波操作"""
    ws = _ka_imga_window_size.findall(param)
    #print(ws)
    # ascent = misc.ascent()
    result = ndimage.minimum_filter(ka_vals[imgname], size=int(ws[0]))
    ka_vals[imgname+"最小滤波后"]=result
