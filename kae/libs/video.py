import os

def compress(file, ofile, **kwargs):
    '''视频压缩'''
    from kae.libs.sys import fpath
    print(fpath(file), fpath(ofile), kwargs)
