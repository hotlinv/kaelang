# 【引用】PIL、numpy

# 【映射】
ka_pmap=lambda:{
	u"访问(?:在|位于)(.+)的图像文件“(.+)”":"ka_pil_open(ka_path('{0}'), '{1}')",
    u"(?:把|改变)图像《(.+)》大小变为横：(\d+)(?:，)?\s*竖：(\d+)":"ka_pil_resize('{0}', {1}, {2})",
    u"(?:把|改变)图像《(.+)》变为(\w+)模式":"ka_pil_convert('{0}', '{1}')",
    u"(?:把|改变)图像《(.+)》(?:的)?模式变为(\w+)":"ka_pil_convert('{0}', '{1}')",
    u"展示图像《(.+)》":"ka_pil_show('{0}')",
    u"把图像《(.+)》输出：(.+)":"ka_pil_save('{0}', ka_path('{1}'))",
    u"在图像《(.+)》上用色刷《(.+)》绘制多边形图案《(.+)》":"ka_pil_draw_polygon('{0}', '{1}', '{2}')",
    u"把图像《(.+)》增强为原来的([0-9]*\.?[0-9]*)倍":"ka_pil_im_enhance('{0}', {1})",
    u"把图像《(.+)》向右旋转90度":"ka_pil_im_rotate('{0}', 270)",
    u"把图像《(.+)》向左旋转90度":"ka_pil_im_rotate('{0}', 90)",
    u"把图像《(.+)》向(?:左|右)旋转180度":"ka_pil_im_rotate('{0}', 180)",
    #u"把图像《(.+)》上下翻转":"ka_pil_im_flip('{0}', 1)",
    #u"把图像《(.+)》左右翻转":"ka_pil_im_flip('{0}', 0)",
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

@catch2cn
@lastit
def ka_pil_im_enhance(name, scale):
    """增强图像"""
    from PIL import ImageEnhance
    enh = ImageEnhance.Contrast(ka_vals[name])
    ka_vals[name+"增强后"] = enh.enhance(scale)
    return name+"增强后"

@catch2cn
@lastit
def ka_pil_im_rotate(name, angle=90):
    """图像旋转"""
    im = ka_vals[name]
    oname = name+"旋转后"
    if angle==90:
        ka_vals[oname] = im.transpose(Image.ROTATE_90)
    if angle==180:
        ka_vals[oname] = im.transpose(Image.ROTATE_180)
    elif angle==-90 or angle==270:
        ka_vals[oname] = im.transpose(Image.ROTATE_270)
    else:
        raise Exception(f"暂不支持非90度倍数的旋转")
    return oname

@catch2cn
@lastit
def ka_pil_im_flip(name, axis=0):
    """图像翻转
    [k]图像上下翻转·'{0}',1
    [k]图像左右翻转·'{0}',0
    """
    im = ka_vals[name]
    oname = name+"翻转后"
    if axis==0:
        ka_vals[oname] = im.transpose(Image.FLIP_LEFT_RIGHT)
    else:
        ka_vals[oname] = im.transpose(Image.FLIP_TOP_BOTTOM)
    return oname
