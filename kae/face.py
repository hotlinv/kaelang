from pywebio.input import input, FLOAT, TEXT
from pywebio.output import put_text
from kae.zhcompiler import compile

def bmi():
    height = input("请输入你的身高(cm)：", type=FLOAT)
    weight = input("请输入你的体重(kg)：", type=FLOAT)

    BMI = weight / (height / 100) ** 2

    top_status = [(14.9, '极瘦'), (18.4, '偏瘦'),
                  (22.9, '正常'), (27.5, '过重'),
                  (40.0, '肥胖'), (float('inf'), '非常肥胖')]

    for top, status in top_status:
        if BMI <= top:
            put_text('你的 BMI 值: %.1f，身体状态：%s' % (BMI, status))
            break

def kface():
    ips = input("请输入：", type=TEXT)
    while ips:
        exs = compile(ips)
        for ex in exs:
            if ex["errno"]==0:
                put_text("编译结果：%s" % ex["exec"])
            elif ex["errno"]==1:
                put_text("编译失败，无法解析的语句：%s" % ex["input"])
            elif ex["errno"]==2:
                put_text("编译失败，不会执行的语句：%s" % ex["input"])
        ips = input("请输入：", type=TEXT)

if __name__ == '__main__':
    kface()