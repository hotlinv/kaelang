import os

class VideoTransform:
    def compress(self, file):
        '''视频压缩'''
        from kae.libs.sys import fpath
        self.infile = fpath(file)
    def setr(self, r):
        '''设置帧率'''
        self.r = r
    def sets(self, s):
        '''设置分辨率'''
        self.s = s
    def setbv(self, bv):
        '''设置码率'''
        self.bv = bv
    def saveas(self, ofile):
        '''另存为'''
        from kae.libs.sys import fpath
        self.ofile = fpath(ofile)
        print(self.infile, self.ofile)