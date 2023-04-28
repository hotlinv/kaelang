from tinydb import TinyDB, Query
from pydantic import BaseModel, Field, create_model
from typing import Optional, List
from pydantic.fields import FieldInfo
import inspect

class _AttrField(BaseModel):
    fieldName: str
    desc: str
    dtype: str
    required: bool

class StrField(_AttrField):
	def __init__(self, name, ename, required=True):
		super().__init__(fieldName=name, desc=ename, required=required, dtype="str")

class IntField(_AttrField):
	def __init__(self, name, ename, required=True):
		super().__init__(fieldName=name, desc=ename, required=required, dtype="int")

class FloatField(_AttrField):
	def __init__(self, name, ename, required=True):
		super().__init__(fieldName=name, desc=ename, required=required, dtype="float")

class DateField(_AttrField):
	def __init__(self, name, ename, required=True):
		super().__init__(fieldName=name, desc=ename, required=required, dtype="date")

class List_int_Field(_AttrField):
	def __init__(self, name, ename,  required=True):
		super().__init__(fieldName=name, desc=ename, required=required, dtype="List[int]")

class List_str_Field(_AttrField):
	def __init__(self, name, ename,  required=True):
		super().__init__(fieldName=name, desc=ename, required=required, dtype="List[str]")

class Graph:
    def __init__(self, path):
        self._db = TinyDB(path)
        self._schema = self._db.table("schema")
        Schema = Query()
        self.tags = self._schema.search(Schema.type=="tag")
        self.refs = self._schema.search(Schema.type=="ref")
        self._graph = self._db.table("graph")
        GraphData = Query()
        self.nodes = self._graph.search(GraphData.type=="node")
        self.edges = self._graph.search(GraphData.type=="edge")

    def createTag(self, mod):
        fieldname = lambda f: f.outer_type_.__name__.capitalize() if "_name" not in dir(f.outer_type_) else f.outer_type_._name.capitalize()+"_"+f.type_.__name__+"_"
        attrs = [eval(r"{}Field('{}', '{}', {})".format(fieldname(mod.__fields__[fn]), fn, fconf["title"], fn in mod.schema()["required"])) for fn, fconf in mod.schema()["properties"].items()]
        self._schema.insert({
            'type': 'tag', 
            'tagname': mod.schema()["title"], 
            "classname": inspect.getmodule(mod).__name__+"."+mod.schema()["title"],
            "desc":"" if "description" not in mod.schema() else mod.schema()["description"], 
            "attrs":[j.dict() for j in attrs]})

    def getTag(self, tagname):
        Schema = Query()
        t = self._schema.search((Schema.type=="tag") & (Schema.tagname==tagname))[0]
        #print("doc_id:", t.doc_id)
        # at = {it["fieldName"]:(eval(it["dtype"]) if it["required"] else eval(f'Optional[{it["dtype"]}]'), ...) for it in t["attrs"]}
        # print(at)
        # return create_model(t["tagname"], type="tag", **at)
        mn = t["classname"].split(".")
        exec(f"from {'.'.join(mn[0:-1])} import {mn[-1]}")
        return eval(t["tagname"])

    def createRef(self, rmod):
        attrs = [eval(r"{}Field('{}', '{}', {})".format(rmod.__fields__[fn].type_.__name__.capitalize(), fn, fconf["title"], fn in rmod.schema()["required"])) for fn, fconf in rmod.schema()["properties"].items()]
        self._schema.insert({
            'type': 'ref', 
            'refname': rmod.schema()["title"], 
            "desc":"" if "description" not in rmod.schema() else rmod.schema()["description"],
            #"from":tag1, "to":tag2, 
            "attrs":[j.dict() for j in attrs]})

    def createNode(self, nodetype, name=None, tags=None, data=None):
        if data is not None:
            name = data.name
            tags = [data]
        node = {'type': 'node', "nodetype":nodetype, 'name': name}
        for tag in tags:
            node.update({k:n for k, n in tag.dict().items() if k!="type"})
        nid = self._graph.insert(node)
        return nid

    def updateNode(self, nodeid, **args):
        print(args)
        self._graph.update(args, doc_ids=[nodeid])

    def getNodes(self, nodetype, name=None):
        Data = Query()
        q = (Data.type=="node") & (Data.nodetype==nodetype)
        if name is not None:
            q = q & (Data.name==name)
        ns = self._graph.search( q )
        return ns

    def createEdge(self, edgetype, node1name, node2name):
        Node = Query()
        node1id = None
        if node1name is not None:
            node1 = self._graph.search((Node.type=="node") & (Node.name==node1name))[0]
            node1id = node1.doc_id
        node2 = self._graph.search((Node.type=="node") & (Node.name==node2name))[0]
        nid = self._graph.insert({
            'type': 'edge', 
            'name': edgetype, 
            "src":node1id, 
            "tar":node2.doc_id, 
            "attrs":[]})
        return nid

    def getEdge(self, etype, src, tar):
        Data = Query()
        node1id = None
        if src is not None:
            node1 = self._graph.search((Data.type=="node") & (Data.name==src))[0]
            node1id = node1.doc_id
        node2 = self._graph.search((Data.type=="node") & (Data.name==tar))[0]
        q = (Data.type=="edge") & (Data.name==etype) & (Data.src==node1id) & (Data.tar==node2.doc_id)
        ns = self._graph.search( q )
        # print(ns)
        return ns[0] if len(ns)>0 else None

    def di(self, nid):
        Node = Query()
        node1 = self._graph.get(doc_id=nid)
        return node1

    def query(self, q):
        if type(q).__name__=="ModelMetaclass":
            Node = Query()
            return self._graph.search(Node.nodetype==q.__name__)
        return #self._graph.search(q)

    def plot(self):
        import plotly.graph_objects as go
        import networkx as nx
        import random
        G = nx.Graph()
        
        labels = []
        for idx,n in enumerate(self.nodes):
            G.add_node(n.doc_id, name=n["name"])
            labels.append(n["name"])
        for edge in self.edges:
            if edge["src"] is not None:
                G.add_edge(edge["src"], edge["tar"])
            # x0, y0 = G.nodes[edge[0]]['pos']
            # x1, y1 = G.nodes[edge[1]]['pos']
            # edge_x.append(x0)
            # edge_x.append(x1)
            # edge_x.append(None)
            # edge_y.append(y0)
            # edge_y.append(y1)
            # edge_y.append(None)
        pos = nx.spring_layout(G)
        # pos = nx.nx_agraph.graphviz_layout(G)
        # layt=G.layout('kk', dim=3)
        # print(pos2d)
        # print(pos)
        Xn = [pos[node][0] for node in G.nodes()]
        Yn = [pos[node][1] for node in G.nodes()]
        Zn = [0 for node in G.nodes()]
        edge_x = []
        edge_y = []
        edge_z = []
        for edge in G.edges:
            edge_x.append(pos[edge[0]][0])
            edge_x.append(pos[edge[1]][0])
            edge_x.append(None)
            edge_y.append(pos[edge[0]][1])
            edge_y.append(pos[edge[1]][1])
            edge_y.append(None)
            edge_z.append(0)
            edge_z.append(0)
            edge_z.append(None)

        edge_trace = go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')
        
        trace2=go.Scatter3d(x=Xn,
               y=Yn,
               z=Zn,
               mode='markers',
               name='actors',
               marker=dict(symbol='circle',
                             size=6,
                             #color=group,
                             colorscale='Viridis',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
               )
        # vis = go.GraphVisualization(G, pos2d)
        # fig = vis.create_figure()
        axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

        layout = go.Layout(
                title="Network of coappearances of characters in Victor Hugo's novel<br> Les Miserables (3D visualization)",
                width=1000,
                height=1000,
                showlegend=False,
                scene=dict(xaxis=dict(axis),yaxis=dict(axis),zaxis=dict(axis),),
            margin=dict(t=100),
            hovermode='closest',
            annotations=[
                dict(
                showarrow=False,
                    text="图结构",
                    xref='paper',
                    yref='paper',
                    x=0,
                    y=0.1,
                    xanchor='left',
                    yanchor='bottom',
                    font=dict(size=14)
                    )
                ],    ) 
        data=[edge_trace, trace2]
        fig=go.Figure(data=data, layout=layout)
        fig.show()

def _newtag(g, comm):
    carr = comm.split()
    pkgs = carr[1].split(".")
    exec("from "+".".join(pkgs[0:-1])+" import "+pkgs[-1])
    g.createTag(eval(pkgs[-1]))

def _newref(g, comm):
    carr = comm.split()
    pkgs = carr[1].split(".")
    exec("from "+".".join(pkgs[0:-1])+" import "+pkgs[-1])
    g.createRef(eval(pkgs[-1]))

def _newnode(g, comm):
    carr = comm.split()
    M = g.getTag(carr[1])
    args = json.loads("".join(carr[2:]))
    for k, v in args.items():
        if k.startswith("$"):
            del args[k]
            args[k[1:]] = vars[v]
    # print(M, args)
    m = eval("M(**args)")
    g.createNode(M.schema()["title"], data=m)

def _newedge(g, comm):
    carr = comm.split()
    edgetype = carr[1]
    idn = carr[2] #id保存到变量名

    node2name = carr[-1]
    node1name = None if carr[-3]==carr[2] else carr[-3]
    nid = g.createEdge(edgetype, node1name, node2name)
    exec(f"vars['{idn}']={nid}")

vars = {}
def _newlist(comm):
    carr = comm.split()
    listname = carr[1]
    arr = [vars[vn] for vn in carr[2:]]
    vars[listname] = arr

TAGMAP = {"动作":r"{action}", "目标":r"{target}", "内容":r"{args}", "目标名称":r"{tarargs}", "对象参数":r"{tarargs}", "可选":"~", "目标类型": r"{tartype}"}

def parseTemplFile(g, comm):
    # 解析word来进行语料训练
    import docx
    carr = comm.split()
    document = docx.Document(carr[1])

    for p in document.paragraphs:
        if p.text!="":
            # print( [ r.comments for r in p.runs])
            iis = [ix for ix, e in enumerate( [len(r.comments) for r in p.runs]) if e !=0]
            props = [p.runs[i-1].text+":"+TAGMAP[p.runs[i].comments[0].text] for i in iis]
            line = f"parse sentence {p.text} {' '.join(props)}"
            parseTempl(g, line)
    
def parseTempl(g, comm):
    # 自动分析语句，进行图谱构建。
    import jieba
    import jieba.posseg as pseg
    from kae.model import Word, Sentence
    from kae.zhcompiler import replaceSame, cut, splitSentence
    carr = comm.split()
    nodetype = carr[1]
    tmpl = f"{carr[2]}" #句式模板
    wordlst = g.getNodes("Word")
    wordls = [w["name"] for w in wordlst]
    wordcs = [w["wordclass"] for w in wordlst]
    segoa = splitSentence(f"{tmpl}")[0] #先分词一遍，获取词性
    segks = [w.name for w in segoa]
    keyts = {r"{args}":r"nm*+", r"{tarargs}":r"nmnznsnfs*"}   #需要修改此处
    optionals = []
    for it in carr[3:]: #对应参数
        k, v = it.split(":")
        k1 = k.replace("“", '"').replace("”", '"')#做字符串判断时候会有符号变化
        if k1 in segks:
            keyts[v]=[w.wordclass for w in segoa if w.name==k1][0]
        if v.startswith("{") and v.endswith("}") :
            if v not in wordls:
                jieba.add_word(k)
        elif v=="~":#可选
            optionals.append(k)
            continue
        tmpl = tmpl.replace(k, v)
    
    print(segoa, keyts, optionals)
    
    seg_list = splitSentence(tmpl)[0]#pseg.lcut(tmpl)
    replaceSame(g, seg_list)
    # print(tmpl, [s for s in seg_list])
    #合并{}
    for ix, si in enumerate(seg_list): 
        if si.name=="}":
            seg_list[ix-1].name = "{"+seg_list[ix-1].name+"}"
            seg_list[ix-1].wordclass = keyts[seg_list[ix-1].name]
    # print(seg_list)
    seglist = [(s.name, s.wordclass) for s in seg_list if s.name not in "}{" ]
    # for w,f in seg_list:
    #     #print(s)
    #     seglist.append((w,f))
    print(seglist)
    # vars = {}
    #开始处理
    for word, flag in seglist:
        print("-"*10, word, flag)
        
        if word not in wordls:
            nid = g.createNode("Word", data=Word(name=word, wordclass=flag))
        else:
            nw = g.getNodes("Word", word)[0]
            if flag not in nw["wordclass"]:
                g.updateNode(nw.doc_id, wordclass=nw["wordclass"]+flag)
        
        wordlst = g.getNodes("Word")
        wordls = [w["name"] for w in wordlst]
    
    edges = []
    last = []
    for word, flag in seglist:
        la = last.pop() if len(last)>0 else None
        while True:
            src = la
            tar = word
            e = g.getEdge("NextRef", src, tar)
            if e is None:
                eid = g.createEdge("NextRef", src, tar)
            else:
                eid = e.doc_id
            print(eid, src, "->>", tar)
            edges.append(eid)
            if len(last)>0:
                la = last.pop()
            else:
                break
        
        if word in optionals:#可选
            last.append(la)
        last.append(word)
        # print(last)
        
    print("edges", edges)
    g.createNode("Sentence", data=Sentence(name=tmpl, edges=edges))
    
    

import click, json, os
@click.command()
@click.option('--db', prompt='数据库文件名', help='指定数据库文件.')
@click.option('--script', required=False, help='导入文件到数据库（不打开交互控制台）.')
def graphcli(db, script):
    """图数据库cli."""
    # for x in range(count):
    if script is not None and os.access(db, os.F_OK):
        os.remove(db) #重新初始化的时候要删除原数据库
    g = Graph(db)
    if script is not None:
        #导入文件
        if os.access(script, os.F_OK):
            with open(script, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("newtag"):
                        _newtag(g, line)
                    elif line.startswith("newref"):
                        _newref(g, line)
                    elif line.startswith("newnode"):
                        _newnode(g, line)
                    elif line.startswith("newedge"):
                        _newedge(g, line)
                    elif line.startswith("newlist"):
                        _newlist(line)
                    elif line.startswith("parse"):
                        parseTempl(g, line)
                    elif line.startswith("train"):
                        parseTemplFile(g, line)
        return 
    comm = click.prompt('~~> ')
    while comm!="quit" and comm!="exit":
        if comm=="tags":
            click.echo(g.tags)
        elif comm == "nodes":
            click.echo(g.nodes)
        elif comm.startswith("newtag"):
            _newtag(g, comm)
        elif comm.startswith("newref"):
            _newref(g, comm)
        elif comm.startswith("newnode"):
            _newnode(g, comm)
        elif comm.startswith("newedge"):
            _newedge(g, comm)
        elif comm=="plot":
            g.plot()
        elif comm.startswith("newlist"):
            _newlist(comm)
        comm = click.prompt('~~> ')


if __name__=="__main__":
	class Man(BaseModel):
		"""人类"""
		name: str = Field(title="姓名")
		age: int = Field(title="年龄")

	# g = Graph("g2.json")

	graphcli()
	
	# print(g.tags)
	
	# print(g.refs)
	# g.createTag(Man)
	# print(Man.schema())

	# M = g.getTag("Man")
	# m = Man(name="王五",age=23)
	# m2 = Man(name="张三",age=31)

	# g.createNode(data=m)
	# g.createNode(data=m2)
	
	# print(bing.dict())

	
	# print(z.dict())

	


