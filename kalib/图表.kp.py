# 【引用】matplotlib

# 【映射】
ka_pmap=lambda:{
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

