import jieba
import logging

# 配置logging
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d - %(message)s',
    handlers=[
        #logging.FileHandler("ke.log", mode="a"),  # for logs write in file（mode：a为追加log，设置为w则表示每次清空，重新记录log）
        logging.StreamHandler()  # for print at console
    ]
)
jieba.setLogLevel(logging.INFO)

def ka_replaceQuot(s):
    '''把单引号变为转义字符'''
    ss = s.split("'")
    sss = []
    for idx, si in enumerate(ss):
        sss.append(si)
        if idx==0 or idx==len(ss)-2:
            sss.append("'")
        elif si.endswith(r"\\"):
            sss.append("'")
        else:
            sss.append(r"\'")
    return "".join(sss[:-1])