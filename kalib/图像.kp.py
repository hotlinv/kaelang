# 【引用】PIL、numpy

# 【映射】
ka_pmap=KaeLevMap(lev0={
	u"访问(?:在|位于)(.+)的图像文件“(.+)”":"ka_pil_open(ka_path('{0}'), '{1}')",
    u"(?:把|改变)图像《(.+)》大小变为横：?(\d+)(?:，)?\s*竖：?(\d+)":"ka_pil_resize('{0}', {1}, {2})",
    u"(?:把|改变)图像《(.+)》变为(\w+)模式":"ka_pil_convert('{0}', '{1}')",
    u"(?:把|改变)图像《(.+)》(?:的)?模式变为(\w+)":"ka_pil_convert('{0}', '{1}')",
    u"展示图像《(.+)》":"ka_pil_show('{0}')",
    u"把图像《(.+)》输出：?(.+)":"ka_pil_save('{0}', ka_path('{1}'))",
    u"在图像《(.+)》上用色刷《(.+)》绘制多边形图案《(.+)》":"ka_pil_draw_polygon('{0}', '{1}', '{2}')",
    u"把图像《(.+)》增强为原来的([0-9]*\.?[0-9]*)倍":"ka_pil_im_enhance('{0}', {1})",
    u"把图像《(.+)》向右旋转90度":"ka_pil_im_rotate('{0}', 270)",
    u"把图像《(.+)》向左旋转90度":"ka_pil_im_rotate('{0}', 90)",
    u"把图像《(.+)》向(?:左|右)旋转180度":"ka_pil_im_rotate('{0}', 180)",
    #u"把图像《(.+)》上下翻转":"ka_pil_im_flip('{0}', 1)",
    #u"把图像《(.+)》左右翻转":"ka_pil_im_flip('{0}', 0)",
})

# 【实现】
from PIL import Image
from PIL import ImageDraw
import os, math

_ka_imgmode=re.compile(u"模式为：?“?(\w+)”?")
_ka_imgsize=re.compile(u"(?:大小|尺寸)?为：?(?:横|横向|长)?：?(\d+)(?:像素|列)?(?:，)?\s*(?:竖|纵向|高)?：?(\d+)(?:像素|行)?")
_modes = {"二值图":"1", "灰度图":"L", "索引表图":"P", "真彩色图":"RGB", "带透明真彩色图":"RGBA"}
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
    # print(mm, sm)
    ka_vals[name]=Image.new(getmode(mm[0]), [int(s) for s in sm[0]])
    ka_vals[f"{name}_type"] = "图像"

@catch2cn
def ka_new_fillcolor(name, value):
    """新建画刷"""
    ka_vals[name]=getcolor(value)
    ka_vals[f"{name}_type"] = "画刷"

registType("空图像", ka_new_empty_image)
registType("色刷", ka_new_fillcolor)

@catch2cn
def ka_pil_open(path, name):
    """打开图像"""
    # print(path, name)
    ka_vals[name] = Image.open(path)
    ka_vals[f"{name}_type"] = "图像"

@catch2cn
def ka_pil_show(name):
    """显示图像"""
    #print("$%", name, ka_vals)
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
    """增强图像
    """
    from PIL import ImageEnhance
    enh = ImageEnhance.Contrast(ka_vals[name])
    ka_vals[name+"增强后"] = enh.enhance(scale)
    ka_vals[f"{name}增强后_type"] = "图像"
    return name+"增强后"

@catch2cn
@lastit
def ka_pil_im_rotate(name, angle=90):
    """图像旋转
    [k]图像(?:向左|逆时针)(?:进行)?(?:旋转)?(\d+)度(?:旋转)?·'{0}',{1}
    [k]图像(?:向右|顺时针)(?:进行)?(?:旋转)?(\d+)度(?:旋转)?·'{0}',-{1}
    """
    #print(angle)
    im = ka_vals[name]
    oname = name+"旋转后"
    if angle==90:
        ka_vals[oname] = im.transpose(Image.ROTATE_90)
        ka_vals[f"{oname}_type"] = "图像"
    elif angle==180 or angle==-180:
        ka_vals[oname] = im.transpose(Image.ROTATE_180)
        ka_vals[f"{oname}_type"] = "图像"
    elif angle==-90 or angle==270:
        ka_vals[oname] = im.transpose(Image.ROTATE_270)
        ka_vals[f"{oname}_type"] = "图像"
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
        ka_vals[f"{oname}_type"] = "图像"
    else:
        ka_vals[oname] = im.transpose(Image.FLIP_TOP_BOTTOM)
        ka_vals[f"{oname}_type"] = "图像"
    return oname

@catch2cn
@lastit
def ka_pil_im_crop(name, rect):
    """图像区域复制
    [k]图像中?复制出?《(.[^》]+)》范围的数据·'{0}','{1}'
    """
    
    im = ka_vals[name]
    rd = ka_vals[rect]
    oname = name+"范围内数据"
    box = (int(rd["x"]), int(rd["y"]), int(rd["x"])+int(rd["w"]), int(rd["y"])+int(rd["h"]))
    ka_vals[oname] = {"data":im.crop(box), "rect": box}
    ka_vals[f"{oname}_type"] = "图像选区"
    
    return oname

@catch2cn
def ka_pil_im_paste(name, imgname, newrect=""):
    """图像选区黏贴
    [k]图像选区(?:黏贴|粘贴)到《(.[^》]+)》中(?:的《(.[^》]+)》)?·'{0}','{1}','{2}'
    """
    rddata = ka_vals[name]
    data = rddata["data"]
    im = ka_vals[imgname]
    tagrect = rddata["rect"]
    # print(newrect)
    if newrect is not None and newrect!="" and newrect!="None":
        rect = ka_vals[newrect]
        tagrect = (int(rect["x"]), int(rect["y"]), int(rect["x"])+int(rect["w"]), int(rect["y"])+int(rect["h"]))
        yn, xn = data.size
        if yn!=int(rect["h"]) or xn!=int(rect["w"]):
            data = data.resize((int(rect["w"]), int(rect["h"])))
    # print(yn, xn, tagrect)
    im.paste(data, tagrect)
    #print(name, imgname, rddata)
    