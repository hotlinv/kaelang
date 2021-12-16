# 【引用】PIL、numpy

# 【映射】
ka_pmap=lambda:{
	u"打开在(.+)的图(?:像|片)文件“(.+)”":"ka_pil_open({0}, '{1}')",
    u"(?:将|改变)图(?:像|片)《(.+)》大小(?:改)?为横：(\d+)(?:，)?\s*竖：(\d+)":"ka_pil_resize('{0}', {1}, {2})",
    u"(?:将|改变)图(?:像|片)《(.+)》(?:改|转)?为“(\w+)”模式":"ka_pil_convert('{0}', '{1}')",
    u"(?:显示|展示)图(?:像|片)《(.+)》":"ka_pil_show('{0}')",
    u"将图(?:像|片)《(.+)》另存为：(.+)":"ka_pil_save('{0}', {1})",
}

# 【实现】
from PIL import Image
from PIL import ImageDraw
import os

_ka_imgmode=re.compile(u"模式为：“(\w+)”")
_ka_imgsize=re.compile(u"(?:大小|尺寸)?为：(?:横|长)?：(\d+)(?:像素)*?(?:，)?\s*竖：(\d+)(?:像素)*")

def ka_new_empty_image(name, value):
    mm = _ka_imgmode.findall(value)
    sm = _ka_imgsize.findall(value)
    ka_vals[name]=Image.new(mm[0], [int(s) for s in sm[0]])

registType("空图像", ka_new_empty_image)

@catch2cn
def ka_pil_open(path, name):
    """打开图像"""
    ka_vals[name] = Image.open(os.path.join(path, name))

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
    ka_vals[name] = ka_vals[name].convert(mode)