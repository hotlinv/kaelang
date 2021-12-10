# 【映射】
ka_pmap=lambda:{
	u"列表：(\w+)到(\w+)":"ka_range({0}, {1})"
}

# 【实现】
def ka_range(b, e):
    return range(b, e+1)
