
from kae.annotations import ka_setobj_rename

from PIL import Image
from PIL import ImageDraw
import os, math



def getcolor(name):
    """获取颜色元组"""
    _colors = {"白色":(255,255,255,255), "黑色":(0,0,0,255), "红色":(255, 0, 0, 255), "绿色":(0, 255, 0, 255), "蓝色":(0, 0, 255, 255)}
    if name in _colors:
        return _colors[name]
    else:
        return name

def img_getmode(name):
    _modes = {"二值图":"1", "灰度图":"L", "索引表图":"P", "真彩色图":"RGB", "带透明真彩色图":"RGBA"}
    if name in _modes:
        return _modes[name]
    else:
        return name

@ka_setobj_rename("图像")
class Picture:
    def __init__(self, img):
        self.img = img
    def show(self):
        """显示图像"""
        self.img.show()
    def convert(self, mode):
        """图像模式转换"""
        self.img.convert(img_getmode(mode))
        return self
    def drawPolygon(self, colorname, polyname):
        """图像上绘制多边形"""
        color = ka_vals[colorname]
        poly = ka_vals[polyname]
        if self.img.mode=="1":
            color = tuple([math.ceil(color[0]/255)])
        elif self.img.mode=="L":
            color = tuple(color[:1])
        elif self.img.mode=="RGB":
            color = tuple(color[:3])
        else:
            color = tuple(color)
        #print(img.mode, color)
        pdraw = ImageDraw.Draw(self.img)
        pdraw.polygon([tuple(p) for p in poly] ,fill=color)
        return self

    def enhance(self, scale):
        """增强图像"""
        from PIL import ImageEnhance
        enh = ImageEnhance.Contrast(self.im)
        imgnew = enh.enhance(scale)
        return Picture(imgnew)

    def rotate(self, angle=90):
        """图像旋转
        [k]图像(?:向左|逆时针)(?:进行)?(?:旋转)?(\d+)度(?:旋转)?·'{0}',{1}
        [k]图像(?:向右|顺时针)(?:进行)?(?:旋转)?(\d+)度(?:旋转)?·'{0}',-{1}
        """
        #print(angle)
        if angle==90:
            imgnew = self.img.transpose(Image.ROTATE_90)
        elif angle==180 or angle==-180:
            imgnew = self.img.transpose(Image.ROTATE_180)
        elif angle==-90 or angle==270:
            imgnew = self.img.transpose(Image.ROTATE_270)
        else:
            raise Exception(f"暂不支持非90度倍数的旋转")
        return Picture(imgnew)

    def flip(self, axis=0):
        """图像翻转
        [k]图像上下翻转·'{0}',1
        [k]图像左右翻转·'{0}',0
        """
        if axis==0:
            imgnew = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            imgnew = self.img.transpose(Image.FLIP_TOP_BOTTOM)
        return Picture(imgnew)

    def crop(self, rect):
        """图像区域复制
        [k]图像中?复制出?《(.[^》]+)》范围的数据·'{0}','{1}'
        """
        rd = ka_vals[rect]
        oname = name+"范围内数据"
        box = (int(rd["x"]), int(rd["y"]), int(rd["x"])+int(rd["w"]), int(rd["y"])+int(rd["h"]))
        imgnew = {"data":self.img.crop(box), "rect": box}
        return Picture(imgnew)

    def paste(self, imgname, newrect=""):
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
        return self
        #print(name, imgname, rddata)
    def resize(self, w, h):
        """改变图像大小"""
        self.img = self.img.resize((w, h))
        return self
    def saveas(self, path):
        from kae.libs.sys import fpath
        from kae import ka_fext
        import numpy as np
        outfile = fpath(path)
        self.img.save(outfile)


def ka_new_empty_image(size, mode):
    """新建空图像"""
    # print(mm, sm)
    img=Image.new(img_getmode(mode), [int(s) for s in size])
    return Picture(img)

def ka_new_fillcolor(name, value):
    """新建画刷"""
    ka_vals[name]=getcolor(value)
    ka_vals[f"{name}_type"] = "画刷"

# registType("空图像", ka_new_empty_image)
# registType("色刷", ka_new_fillcolor)

def ka_pil_open(path):
    """打开图像"""
    # print(path, name)
    img = Image.open(path)
    return Picture(img)




  