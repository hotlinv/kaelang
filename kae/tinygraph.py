from tinydb import TinyDB, Query
from pydantic import BaseModel, Field, create_model

class _AttrField(BaseModel):
	fieldName: str
	desc: str
	dtype: str

class StrField(_AttrField):
	def __init__(self, name, ename):
		super().__init__(fieldName=name, desc=ename, dtype="str")

class IntField(_AttrField):
	def __init__(self, name, ename):
		super().__init__(fieldName=name, desc=ename, dtype="int")

class FloatField(_AttrField):
	def __init__(self, name, ename):
		super().__init__(fieldName=name, desc=ename, dtype="float")

class DateField(_AttrField):
	def __init__(self, name, ename):
		super().__init__(fieldName=name, desc=ename, dtype="date")

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
        attrs = [eval(r"{}Field('{}', '{}')".format(mod.__fields__[fn].type_.__name__.capitalize(), fn, fconf["title"])) for fn, fconf in mod.schema()["properties"].items()]
        self._schema.insert({
            'type': 'tag', 
            'tagname': mod.schema()["title"], 
            "desc":"" if "description" not in mod.schema() else mod.schema()["description"], 
            "attrs":[j.dict() for j in attrs]})

    def getTag(self, tagname):
        Schema = Query()
        t = self._schema.search((Schema.type=="tag") & (Schema.tagname==tagname))[0]
        #print("doc_id:", t.doc_id)
        at = {it["fieldName"]:(it["dtype"], ...) for it in t["attrs"]}
        return create_model(t["tagname"], type="tag", **at)

    def createRef(self, name, desc, tag1, tag2, attrs):
        self._schema.insert({'type': 'ref', 'refname': name, "desc":desc, "from":tag1, "to":tag2, "attrs":[j.dict() for j in attrs]})

    def createNode(self, name=None, tags=None, data=None):
        if data is not None:
            name = data.name
            tags = [data]
        node = {'type': 'node', 'name': name}
        for tag in tags:
            node.update({k:n for k, n in tag.dict().items() if k!="type"})
        self._graph.insert(node)

    def createEdge(self, name, node1, node2, refs):
        self._graph.insert({'type': 'edge', 'name': name, "from":node1.doc_id, "to":node2.doc_id, "refs":refs})

    def query(self, query):
        pass

    def plot(self):
        import plotly.graph_objects as go
        import networkx as nx
        import random
        G = nx.Graph()
        labels = []
        for idx,n in enumerate(self.nodes):
            G.add_node(n.doc_id, name=n["name"])
            labels.append(n["name"])
        pos = nx.spring_layout(G)
        # pos = nx.nx_agraph.graphviz_layout(G)
        # layt=G.layout('kk', dim=3)
        # print(pos2d)
        # print(pos)
        Xn = [pos[node][0] for node in G.nodes()]
        Yn = [pos[node][1] for node in G.nodes()]
        Zn = [0 for node in G.nodes()]
        
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
        data=[trace2]
        fig=go.Figure(data=data, layout=layout)
        fig.show()

import click, json
@click.command()
@click.option('--db', prompt='数据库文件名',
              help='指定数据库文件.')
def graphcli(db):
    """图数据库cli."""
    # for x in range(count):
    g = Graph(db)
    comm = click.prompt('~~> ')
    while comm!="quit" and comm!="exit":
        if comm=="tags":
            click.echo(g.tags)
        elif comm == "nodes":
            click.echo(g.nodes)
        elif comm.startswith("newtag"):
            carr = comm.split()
            pkgs = carr[1].split(".")
            exec("from "+".".join(pkgs[0:-1])+" import "+pkgs[-1])
            g.createTag(eval(pkgs[-1]))
        elif comm.startswith("newnode"):
            carr = comm.split()
            M = g.getTag(carr[1])
            args = json.loads("".join(carr[2:]))
            m = eval("M(**args)")
            g.createNode(data=m)
        elif comm=="plot":
            g.plot()
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

	


