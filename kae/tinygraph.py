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
		self.nodes = self._graph.search(Schema.type=="node")
		self.edges = self._graph.search(Schema.type=="edge")

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
		print("doc_id:", t.doc_id)
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




if __name__=="__main__":
	class Man(BaseModel):
		"""人类"""
		name: str = Field(title="姓名")
		age: int = Field(title="年龄")

	g = Graph("g2.json")
	
	# print(g.tags)
	
	# print(g.refs)
	# g.createTag(Man)
	print(Man.schema())

	# M = g.getTag("Man")
	m = Man(name="王五",age=23)
	m2 = Man(name="张三",age=31)

	# g.createNode(data=m)
	# g.createNode(data=m2)
	
	# print(bing.dict())

	
	# print(z.dict())

	


