from copy import deepcopy

class KaeLevMap:
    def __init__(self, **kwargs):
        self.lmap = {}
        for k,v in kwargs.items():
            if k.startswith("lev"):
                self.lmap[int(k[3:])] = v 
    def update(self, levmap):
        for k,v in levmap.lmap.items():
            if k in self.lmap:
                self.lmap[k].update(v)
            else:
                self.lmap[k] = deepcopy(v)
    def list(self, i):
        ret = []
        if i not in self.lmap:
            return ret
        if type(self.lmap[i])==list:
            for it in self.lmap[i]:
                ret.append(it)
        else:
            for k, v in self.lmap[i].items():
                ret.append([k, v])
        return ret
    def geList(self, i):
        ret = []
        for j in sorted(self.lmap.keys()):
            if j>=i:
                if type(self.lmap[j])==list:
                    for it in self.lmap[j]:
                        ret.append(it)
                else:
                    for k, v in self.lmap[j].items():
                        ret.append([k, v])
        return ret
    def leList(self, i):
        ret = []
        for j in sorted(self.lmap.keys()):
            if j<=i:
                if type(self.lmap[j])==list:
                    for it in self.lmap[j]:
                        ret.append(it)
                else:
                    for k, v in self.lmap[j].items():
                        ret.append([k, v])
        return ret

# if __name__=="__main__":
#     m = KaeLevMap(lev0={"a":"at"}, lev1={"b":"b1", "c":"c2"}, lev2={"k":"t1", "q":"t2"})
#     k = KaeLevMap()
#     k.update(m)
#     print(k.list(1))
#     print(k.geList(1))
#     print(k.leList(1))
