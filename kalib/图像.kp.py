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
import os
def ka_pil_open(path, name):
    ka_vals[name] = Image.open(os.path.join(path, name))

def ka_pil_show(name):
    ka_vals[name].show()

def ka_pil_resize(name, w, h):
    ka_vals[name] = ka_vals[name].resize((w, h))

def ka_pil_save(name, path):
    ka_vals[name].save(path)

def ka_pil_convert(name, mode):
    ka_vals[name] = ka_vals[name].convert(mode)