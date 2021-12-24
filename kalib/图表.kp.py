# 【引用】matplotlib

# 【映射】
ka_pmap=lambda:{
    u"在图板上并排(?:展示|绘制)图像(.+)":"ka_plot_show_imgs('{0}')",
    u"在图板上(?:展示|绘制)图像《(.+)》":"ka_plot_show_img('{0}')",
}

# 【实现】
import matplotlib.pyplot as plt
matplotlib.rc("font",family='FangSong')

@catch2cn
def ka_plot_show_img(name):
    """图板上显示图像"""
    plt.figure(name) # 图像窗口名称
    plt.imshow(ka_vals[name])
    plt.axis('on') # 关掉坐标轴为 off
    plt.title(name) # 图像题目
    plt.show()

@catch2cn
def ka_plot_show_imgs(images):
    """图板上显示多张图像"""
    _ka_img_names=re.compile(u"《(.[^《》]+)》")
    ims = _ka_img_names.findall(images)
    imns = [ka_vals[n] for n in ims]
    fig = plt.figure("多图对比") # 图像窗口名称
    if imns[0].mode=="L":
        plt.gray()
    for i, im in enumerate(imns):
        c = len(imns)%4  #默认一排4张
        r = int(len(imns)/4)+1
        idx = i+1
        ax = fig.add_subplot(r*100+c*10+idx)  # left side
        ax.imshow(im)
    plt.show()
