# 【引用】matplotlib

# 【映射】
ka_pmap=lambda:{
    u"在图板上(?:展示|绘制)图像《(.[^《》、]+)》、《(.[^《》、]+)》":"ka_plot_show_2img('{0}','{1}')",
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
def ka_plot_show_2img(name1, name2):
    """图板上显示2张图像"""
    fig = plt.figure("双图对比") # 图像窗口名称
    if ka_vals[name1].mode=="L":
        plt.gray()
    ax1 = fig.add_subplot(121)  # left side
    ax2 = fig.add_subplot(122)  # right side
    ax1.imshow(ka_vals[name1])
    #ax1.title(name1) # 图像题目
    ax2.imshow(ka_vals[name2])
    #ax2.title(name2) # 图像题目
    plt.show()
