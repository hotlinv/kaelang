# 【映射】
ka_pmap=lambda:{
	u"^当前目录$":"ka_workspace()",
}

# 【实现】
import os

@catch2cn
def ka_workspace():
    """获取当前目录"""
    return os.path.abspath(os.path.curdir)


