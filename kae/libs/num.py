
cn_num = {
        0: '零',
        1: '一',
        2: '二',
        3: '三',
        4: '四',
        5: '五',
        6: '六',
        7: '七',
        8: '八',
        9: '九'
    }
    
setp = ['亿', '万', '']
setp.reverse()
unit = ['千', '百', '十', '']
unit.reverse()

def _step2cn(numstr, result, stepi):
    print(numstr, stepi)
    result.append(setp[stepi])
    z = False
    for i, n in enumerate(numstr[::-1]):
        if int(n)==0:
            if z:
                result.append("零")
            else:
                result.append("")
            z = False
        else:
            z=True
            result.append(cn_num[int(n)] + unit[i])

def num2cn(num):
    """
    将阿拉伯数字转换为中文数字
    :param num: 阿拉伯数字
    :return: 中文数字
    """
    if num==0:
        return "零"
    import math, re

    result = []
    ceilc = math.ceil(len(str(num))/4)*4
    cnn = str(num).rjust(ceilc, "0")
    print(cnn)
    for i in range(int(ceilc/4)):
        stepi = int(ceilc/4)-1-i
        _step2cn(cnn[stepi*4:(stepi+1)*4], result, i)
    print(result)
    result.reverse()
    cn = "".join(result)
    cn = re.sub(r'^零','',cn)
    cn = re.sub(r'零$','',cn)
    return cn


# print(num2cn(230000705944))