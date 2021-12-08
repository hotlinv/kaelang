# 【映射】
ka_sys = {
	u"(?:在|于|用|使用)?(?:控制台)?打印[：:]\s*(.+)":"ka_pr(*)",
	u"(?:新建|创建|定义|有)?一个名叫(“\w+”)的(.+)，(?:值|初始化)为(.+)":"ka_new({0}, {1}, {2})"
}

# 【实现】
def ka_pr(*a):
    print(*a)

def ka_new(name, type, value):
    if type=="字符串":
        value=value.replace("“","\"").replace("”","\"")
        exec(f"ka_vals[\"{name}\"]=\"{value}\"")
    elif type=="整数" or type=="浮点数":
        exec(f"ka_vals[\"{name}\"]={value}")
        #print(abc)
