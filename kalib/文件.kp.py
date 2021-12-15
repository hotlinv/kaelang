# 【映射】
ka_pmap=lambda:{
	u"^当前目录$":"ka_workspace()",
}

# 【实现】
import os

def ka_workspace():
    return os.path.abspath(os.path.curdir)


