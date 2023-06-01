import os

class VideoTransform:
    def compress(self, file):
        '''视频压缩'''
        from kae.libs.sys import fpath
        self.infile = fpath(file)
        return self
    def setr(self, r):
        '''设置帧率'''
        self.r = f"-r {r}"
        return self
    def sets(self, s):
        '''设置分辨率'''
        self.s = f"-s {s}"
        return self
    def setbv(self, bv):
        '''设置码率'''
        self.bv = f"-b:v {bv}"
        return self
    def saveas(self, ofile):
        '''另存为'''
        from kae.libs.sys import fpath
        self.ofile = fpath(ofile)
        r = self.r if hasattr(self, "r") else ""
        s = self.s if hasattr(self, "s") else ""
        bv = self.bv if hasattr(self, "bv") else ""
        cmd = f"ffmpeg -i {self.infile} {r} {s} {bv} {self.ofile}"
        print(cmd)
        os.system(cmd)