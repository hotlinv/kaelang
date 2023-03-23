import cherrypy
import hashlib
from kae.lang import ka_prepare_a_line, ka_parse

class KaeEar(object):
    @cherrypy.expose
    def index(self):
        return "你好，欢迎使用kæ语言!"
    def build(self, slines):
        lines = [l.strip() for l in slines.split("\n")]
        #codes存放代码段
        ka_fragments = {"step":0, "codes":{"main":[]}, "stack":["main"], "foo":[]}
        for line in lines:
            ka_prepare_a_line(ka_fragments, line)

        mainlines = ["{0}".format(ka_parse(ml)) for ml in ka_fragments["codes"]["main"]]
        ka_fragments["foo"].append(r"aa={}")
        ka_fragments["foo"].extend(mainlines)
        pycallable = "\n".join(ka_fragments["foo"])
        return pycallable
    @cherrypy.expose
    def kaeear(self, say=""):
        fmd5 = hashlib.md5("\n".join(say).encode("UTF-8")).hexdigest()
        return f"{fmd5}:{self.build(say)}"
    
if __name__ == "__main__":
    conf = {
        'global': {
        # 主机0.0.0.0表示可以使用本机IP访问，如http://10.190.20.72:8090，可部署给别人访问
        # 否则只可以用http://127.0.0.1:8090
        # 'server.socket_host': service.host,
        # 端口号
        'server.socket_port': 19831,
        # 当代码变动时，是否自动重启服务，True==是，False==否
        # 设为True时，当该PY代码改变，服务会重启
        # 'engine.autoreload.on': False
        },
    }
    cherrypy.quickstart(KaeEar(), "/", conf)