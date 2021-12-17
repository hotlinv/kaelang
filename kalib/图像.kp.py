# 【引用】PIL、numpy

# 【映射】
ka_pmap=lambda:{
	u"打开在(.+)的图(?:像|片)文件“(.+)”":"ka_pil_open(ka_path('{0}'), '{1}')",
    u"(?:将|改变)图(?:像|片)《(.+)》大小(?:改)?为横：(\d+)(?:，)?\s*竖：(\d+)":"ka_pil_resize('{0}', {1}, {2})",
    u"(?:将|改变)图(?:像|片)《(.+)》(?:改|转)?为“(\w+)”模式":"ka_pil_convert('{0}', '{1}')",
    u"(?:显示|展示)图(?:像|片)《(.+)》":"ka_pil_show('{0}')",
    u"将图(?:像|片)《(.+)》另存为：(.+)":"ka_pil_save('{0}', ka_path('{1}'))",
    u"在图(?:像|片)《(.+)》上用色刷《(.+)》绘制多边形图案《(.+)》":"ka_pil_draw_polygon('{0}', '{1}', '{2}')",
}

# 【实现】
from PIL import Image
from PIL import ImageDraw
import os, math

_ka_imgmode=re.compile(u"模式为：“(\w+)”")
_ka_imgsize=re.compile(u"(?:大小|尺寸)?为：(?:横|长)?：(\d+)(?:像素)*?(?:，)?\s*竖：(\d+)(?:像素)*")
_modes = {"二值图":"1", "灰度图":"L", "索引表图":"P", "真色彩图":"RGB", "带透明真色彩图":"RGBA"}
_colors = {"白色":(255,255,255,255), "黑色":(0,0,0,255), "红色":(255, 0, 0, 255), "绿色":(0, 255, 0, 255), "蓝色":(0, 0, 255, 255)}


@catch2cn
def getmode(name):
    """获取图像模式"""
    if name in _modes:
        return _modes[name]
    else:
        return name

@catch2cn
def getcolor(name):
    """获取颜色元组"""
    if name in _colors:
        return _colors[name]
    else:
        return name

@catch2cn
def ka_new_empty_image(name, value):
    """新建空图像"""
    mm = _ka_imgmode.findall(value)
    sm = _ka_imgsize.findall(value)
    ka_vals[name]=Image.new(getmode(mm[0]), [int(s) for s in sm[0]])

@catch2cn
def ka_new_fillcolor(name, value):
    """新建画刷"""
    ka_vals[name]=getcolor(value)

registType("空图像", ka_new_empty_image)
registType("色刷", ka_new_fillcolor)

@catch2cn
def ka_pil_open(path, name):
    """打开图像"""
    # print(path, name)
    ka_vals[name] = Image.open(path)

@catch2cn
def ka_pil_show(name):
    """显示图像"""
    ka_vals[name].show()

@catch2cn
def ka_pil_resize(name, w, h):
    """改变图像大小"""
    ka_vals[name] = ka_vals[name].resize((w, h))

@catch2cn
def ka_pil_save(name, path):
    """图像另存"""
    ka_vals[name].save(path)

@catch2cn
def ka_pil_convert(name, mode):
    """图像模式转换"""
    ka_vals[name] = ka_vals[name].convert(getmode(mode))

@catch2cn
def ka_pil_draw_polygon(imgname, colorname, polyname):
    """图像上绘制多边形"""
    img = ka_vals[imgname]
    color = ka_vals[colorname]
    poly = ka_vals[polyname]
    if img.mode=="1":
        color = tuple([math.ceil(color[0]/255)])
    elif img.mode=="L":
        color = tuple(color[:1])
    elif img.mode=="RGB":
        color = tuple(color[:3])
    else:
        color = tuple(color)
    #print(img.mode, color)
    pdraw = ImageDraw.Draw(img)
    pdraw.polygon([tuple(p) for p in poly] ,fill=color)
