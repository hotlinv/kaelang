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

from _ctypes import PyObj_FromPtr
 
def di(obj_id):
    """ 通过变量ID 得到变量的值"""
    return PyObj_FromPtr(obj_id)

class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__
    __contains__ = dict.__contains__


def dict2obj(dictObj):
    if not isinstance(dictObj, dict):
        return dictObj
    d = Dict()
    for k, v in dictObj.items():
        d[k] = dict2obj(v)
    return d