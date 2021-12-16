# 【引用】PIL、numpy、ima

# 【映射】
ka_pmap=lambda:{
	u"将图(?:像|片)《(.+)》切割成多个矩形“(.+)”":"ka_img_splitrect('{0}', '{1}')"
}

# 【实现】
from PIL import Image
from PIL import ImageDraw
import ima

def ka_img_splitrect(imgname, rectname):
    img = ka_vals[imgname]
    print(ima.splitRects(img))
