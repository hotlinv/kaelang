import functools
import logging

def catch2cn(fn):
    @functools.wraps(fn) #要加这句，不然inspect的get方法认不到函数，只能认到inner
    def inner(*args):
        # try:
        return fn(*args)
        # except Exception as e:
        #     fndoc = ins.getdoc(fn)
        #     err = u"{} 出错了：{}".format(fndoc.split()[0], str(e))
        #     #print(err)
        #     logging.error(err)
    return inner

def ka_foo(fn):
    '''用于做功能单元的变量初始化和数据回收'''
    @functools.wraps(fn) #要加这句，不然inspect的get方法认不到函数，只能认到inner
    def inner(**args):
        global ka_vals
        global ka_vals_global
        global ka_call_stacks
        try:
            vals = {}
            args["vals"] = vals #初始化本地数据（不污染全局变量）
            args["_id"] = id(vals)
            param, param_type, param_map = None, None, None
            if "obj" in args:
                if args["obj"] in ka_vals:
                    param = ka_vals[args["obj"]]
                if args["obj"]+"_type" in ka_vals:
                    param_type = ka_vals[args["obj"]+"_type"]
                if args["obj"]+"_map" in ka_vals:
                    param_map = ka_vals[args["obj"]+"_map"]
            ps = {}
            if "params" in args:
                ps = {k:ka_vals[k] for k in args["params"] }
            ka_vals_global[args["_id"]] = vals
            ka_vals = vals
            if param:
                ka_vals[args["obj"]] = param
            if param_type:
                ka_vals[args["obj"]+"_type"] = param_type
            if param_map:
                ka_vals[args["obj"]+"_map"] = param_map
            ka_vals.update(ps)
            ka_call_stacks.append(args["_id"])
            # print("ffff", ka_vals)
            ret = fn(**args) ##########运行函数
            #取出返回
            retmap = {}
            for k in [key for key in ka_vals.keys() if key.startswith(fn.__name__)]:
                retmap[k] = ka_vals[k]
            # print(retmap)
            #恢复上级环境
            ka_call_stacks.pop()
            if len(ka_call_stacks)>0:
                ka_vals = ka_vals_global[ka_call_stacks[-1]]
            else:
                ka_vals = ka_vals_global
            #保存返回
            ka_vals.update(retmap)
            #可以做垃圾回收
            return ret
        except Exception as e:
            err = u"{} 出错了：{}".format(fn.__name__, str(e))
            logging.error(err)
    return inner

def lastit(fn):#内部有产生新数据，会返回新数据名字。
    @functools.wraps(fn) #要加这句，不然inspect的get方法认不到函数，只能认到inner
    def inner(*args):
        newname = fn(*args)
        global ka_lastit
        ka_lastit = newname
        return newname
    return inner

def ka_reset_object_name(self, name):
    if name.startswith('"') and name.endswith('"'):#如果有双引号，就去掉
        name = name[1:-1]
    from kae import ka_vals
    ka_vals[name] = self
    self.objname = name # 对象可知自己叫什么变量名
    if hasattr(self, "kacb_setobjNameOK"):
        self.kacb_setobjNameOK()

import types
from functools import wraps
def ka_setobj_rename(cntype="", entype=""):
    '''为对象注入rename方法'''
    def decorate(cls):
        from kae import ka_valtypes
        ka_valtypes[cntype] = cls.__module__+".K"+entype.capitalize() #注册中文和英文名
        @wraps(cls)
        def wapperfoo(*args, **kw):
            obj = cls(*args, **kw)
            obj.cntype=cntype
            obj.renameme = types.MethodType(ka_reset_object_name, obj)
            return obj
        return wapperfoo
    return decorate
