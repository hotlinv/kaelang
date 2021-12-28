# 【引用】

# 【映射】
ka_pmap=lambda:{
    
}

# 【实现】

_ka_rect_wh=re.compile(u"(?:大小|尺寸)?为(\d+)(?:行)?\s*(\d+)(?:列)?")
_ka_rect_oxy=re.compile(u"起始(?:点|位置)?为(.+)")
_ka_rect_x=re.compile(u"(?:横向|X|x)(?:第)?(\d+)(?:列|像素)?")
_ka_rect_y=re.compile(u"(?:纵向|Y|y)(?:第)?(\d+)(?:行|像素)?")

@catch2cn
def ka_new_rect(name, value):
    whm = _ka_rect_wh.findall(value)
    oxy = _ka_rect_oxy.findall(value)
    ox = _ka_rect_x.findall(oxy[0])
    oy = _ka_rect_y.findall(oxy[0])
    ka_vals[f"{name}"]={"x":int(ox[0]), "y":int(oy[0]), "w":int(whm[0][1]), "h":int(whm[0][0])}
    ka_vals[f"{name}_type"]="矩形区域"
    # print(ka_vals[f"{name}"])

registType("矩形区域", ka_new_rect)
registType("矩形范围", ka_new_rect)

