import cherrypy
from kae.annotations import ka_setobj_rename, ka_get_namedobj
import types, functools
models = []
def ka_cls():
    '''为对象注入页面的方法'''
    def decorate(cls):
        @functools.wraps(cls)
        def wapperfoo(*args, **kw):
            obj = cls(*args, **kw)
            inters = obj.inters
            for inter in inters:
                name = inter["name"]
                foo = inter["foo"]
                foos = foo.split(".")
                model = ".".join(foos[:-1])
                fooname = foos[-1]
                if model not in models:
                    exec(f"from {model} import {fooname}")
                    models.append(model)
                efn = eval(f"cherrypy.expose({fooname})")
                if inter["resp"]=="json":
                    efn = cherrypy.tools.json_out()(efn)
                exec(f"obj.{name} = types.MethodType(efn, obj)")
            # obj.md52 = types.MethodType(, obj)
            return obj
        return wapperfoo
    return decorate


def index(serv):
    return {"title":"I`m index!"}

def hello(serv):
    return {"title":"Hello world!"}

def md5(serv, inputstr):
    import hashlib
    m = hashlib.md5(inputstr.encode(encoding="UTF-8")).hexdigest()
    return {"input":inputstr, "output":m}

# def md52(self, inputstr):
#     print(inputstr)
#     import hashlib
#     m = hashlib.md5(inputstr.encode(encoding="UTF-8")).hexdigest()
#     return {"input":inputstr, "output":m}

@ka_cls()
@ka_setobj_rename(cntype="在线服务")
class KServer:
    # @ka_get_namedobj
    def __init__(self, conf):
        self.conf = conf
        self.port = 8080 if "端口" not in conf else conf["端口"]
        self.inters = conf["接口"]

# @ka_get_namedobj
def runkserv(serv):
    cherrypy.quickstart(serv)