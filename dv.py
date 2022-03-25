
from flexx import flx

class Relay(flx.Component):
    """ Global object to relay messages to all participants.
    """

    @flx.emitter
    def create_message(self, message):
        return dict( message=message)

    @flx.emitter
    def new_name(self):
        return {}

    @flx.emitter
    def click_file(self, name):
        return dict(name=name)

    @flx.action
    def file_clicked(self, name):
        self.emit("click_file", name)

    @flx.emitter
    def exec_output(self, msg):
        # print(msg)
        return dict(msg=msg)
    

# class Files(flx.JsComponent):  # Lives in Js
#     name = flx.StringProp(settable=True)

    

    # @flx.emitter
    # def increase_age(self):
    #     self._mutate_age(self.age + 1)

# Create global relay
relay = Relay()

# class Person(flx.JsComponent):  # Lives in Js
#     name = flx.StringProp(settable=True)
#     age = flx.IntProp(settable=True)

#     @flx.action
#     def increase_age(self):
#         self._mutate_age(self.age + 1)

# class PersonDatabase(flx.PyComponent):  # Lives in Python
#     persons = flx.ListProp()

#     @flx.action
#     def add_person(self, name, age):
#         with self:  # new components need a session
#             p = Person(name=name, age=age)
#         self._mutate_persons([p], 'insert', 99999)

#     @flx.action
#     def new_year(self):
#         for p in self.persons:
#             p.increase_age()

class MultiLineEdit(flx.Widget):
    """ An input widget to edit multiple lines of text.

    The ``node`` of this widget is a
    `<textarea> <https://developer.mozilla.org/docs/Web/HTML/Element/textarea>`_.
    """

    DEFAULT_MIN_SIZE = 100, 30

    CSS = """
        .flx-MultiLineEdit {
            overflow-y: hidden;
            color: #333;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            border: 1px solid #aaa;
            margin: 2px;
            height:30px;
        }
        .flx-MultiLineEdit:focus  {
            outline: none;
            box-shadow: 0px 0px 3px 1px rgba(0, 100, 200, 0.7);
        }
    """

    text = flx.StringProp(settable=True, doc="""
        The current text of the multi-line edit. Settable. If this is an empty
        string, the placeholder_text is displayed instead.
        """)

    def _create_dom(self):
        global window
        node = window.document.createElement('textarea')
        f1 = lambda: self.user_text(self.node.value)
        self._addEventListener(node, 'input', f1, False)
        self._addEventListener(node, 'blur', self.user_done, False)
        return node

    @flx.reaction
    def __text_changed(self):
        self.node.value = self.text
        # print(self.node.scrollHeight)
        self.node.style["height"] = f"{self.node.scrollHeight}px"
        #self.node.rows = self.node.scrollHeight//24

    @flx.action
    def _refresh(self):
        self.node.value = self.text
        self.node.style["height"] = f"{self.node.scrollHeight}px"
        # print(self.text, self.node.scrollHeight)

    @flx.emitter
    def user_text(self, text):
        """ Event emitted when the user edits the text. Has ``old_value``
        and ``new_value`` attributes.
        """
        d = {'old_value': self.text, 'new_value': text}
        self.set_text(text)
        return d

    @flx.emitter
    def user_done(self):
        """ Event emitted when the user is done editing the text by
        moving the focus elsewhere. Has ``old_value`` and ``new_value``
        attributes (which are the same).
        """
        d = {'old_value': self.text, 'new_value': self.text}
        return d

class MessageItem(flx.Widget):

    CSS = """
    .flx-MessageItem {
        background: #e8e8e8;
        border: 1px solid #444;
        margin: 3px;
        flex-grow: 2;
        flex-shrink: 0;
        position:relative;
    }
    """

    text = flx.StringProp(settable=True, doc="""Message text""")

    def init(self, text=""):
        super().init()
        self.set_text(text)
        #self._se = window.document.createElement('div')
        with flx.VBox(flex=1, minsize_from_children=True, style="position:relative") as self.outer:
            with flx.HBox(flex=0, minsize_from_children=True):
                self.lab = flx.Label(flex=0, text="我：")
                self.msg_edit = MultiLineEdit(flex=1, text=text, minsize_from_children=True)
                self.run = flx.Button(text='！')
            with flx.HBox(flex=0, minsize_from_children=True):
                flx.Label(flex=0, text="æ：")
                with flx.VBox(flex=1,  minsize_from_children=True):
                    self.output = flx.Label(flex=0,  minsize_from_children=True)

    @flx.reaction('run.pointer_click')
    def a_button_was_pressed(self, *events):
        ev = events[-1]  # only care about last event
        self.run_text(self.msg_edit.text.split("\n"))
        # 
    @flx.reaction('msg_edit.pointer_click')
    def a_edit_was_selected(self, *events):
        parent = self.parent
        for c in parent.children:
            c.apply_style("background-color:#e8e8e8")
        self.apply_style("background-color:#fafafa")
    @flx.action
    def _reupdate(self):
        self.msg_edit._refresh()

    @flx.action
    def print_output(self, msg):
        # print(msg.split("\n"))
        self.output.set_html("<br/>".join(msg.split("\n")))#self.msg_edit.text

    @flx.emitter
    def run_text(self, statement):
        return dict(statement=statement, source=self)

    @flx.emitter
    def text_inputing(self, textlst):
        return dict(textlst=textlst, source=self)

    @flx.reaction('msg_edit.user_text')
    def a_edit_was_inputing(self, *events):
        ev = events[-1]
        self.text_inputing(ev.new_value.split(" "))

class MessageList(flx.Widget):

    CSS = """
    .flx-MessageList {
        overflow:auto;
        background: #e8ffe8;
        border: 1px solid #444;
        margin: 3px;
        align-content: flex-start;
    }
    """
    activeitem = flx.AnyProp(settable=True, doc="""Active Item""")

    # msgs = flx.ListProp()

    def init(self):
        super().init()
        global window
        #self._se = window.document.createElement('div')
        # with flx.VBox(flex=0, style="overflow:auto"):
        #     with flx.VBox(flex=0, minsize_from_children=True) as self.msglst:
                # self.msglst.minsize_from_children = False
        # self.msgs = [MessageItem()]
        MessageItem("", parent=self)
        for c in self.children:
            c._reupdate()
        # self._mutate_msgs([m], 'insert', 99999)
                #self.output = flx.Label(flex=1, text="结果：")
            
            # flx.Widget(flex=1)

    def sanitize(self, text):
        self._se.textContent = text
        text = self._se.innerHTML
        self._se.textContent = ''
        return text

    @flx.action
    def add_message(self, msg):
        # print(msg)
        # line = '<i>' + self.sanitize(name) + '</i>: ' + self.sanitize(msg)
        # self.set_html(self.html + line + '<br />')
        # self.msgs.append(MessageItem(parent=self, text=msg))
        MessageItem(msg, parent=self)
        for c in self.children:
            c._reupdate()
        # self._mutate_msgs([m], 'insert', 99999)
    
    @flx.action
    def clear(self):
        # line = '<i>' + self.sanitize(name) + '</i>: ' + self.sanitize(msg)
        # self.set_html(self.html + line + '<br />')
        for c in self.children:
            c.set_parent(None)
        # for msg in self.msgs:
        #     msg.set_parent(None)
        # self.msgs = []

    
    @flx.reaction('!children**.run_text')
    def on_run(self, *events):
        for ev in events:
            self.run_statement(ev.statement)
            # print(ev.source)
            self.set_activeitem(ev.source)
    @flx.emitter
    def run_statement(self, statement):
        return dict(statement=statement)   

    @flx.reaction('!children**.text_inputing')
    def on_inputing(self, *events):
        for ev in events:
            self.inputing(ev.textlst)
    @flx.emitter
    def inputing(self, textlst):
        return dict(pinyinList=textlst)   
    
    @flx.action
    def output_message(self, msg):
        # print(self.activeitem)
        self.activeitem.print_output(msg)


# Associate CodeMirror's assets with this module so that Flexx will load
# them when (things from) this module is used.
import os
base_url = '.asserts'
def loadassert(afile):
    with open(os.path.join(base_url, afile), 'r', encoding="UTF-8") as f:
        fsr = f.read()
        flx.assets.associate_asset(__name__, afile, fsr)
loadassert('codemirror.min.css')
loadassert('codemirror.min.js')
loadassert('mode/python/python.js')
loadassert('theme/solarized.css')
loadassert('addon/selection/active-line.js')
loadassert('addon/edit/matchbrackets.js')


class CodeEditor(flx.Widget):
    """ A CodeEditor widget based on CodeMirror.
    """

    CSS = """
    .flx-CodeEditor > .CodeMirror {
        width: 100%;
        height: 100%;
    }
    """

    def init(self):
        global window
        # https://codemirror.net/doc/manual.html
        options = dict(value='import os\n\ndirs = os.walk',
                        mode='python',
                        theme='solarized dark',
                        autofocus=True,
                        styleActiveLine=True,
                        matchBrackets=True,
                        indentUnit=4,
                        smartIndent=True,
                        lineWrapping=True,
                        lineNumbers=True,
                        firstLineNumber=1,
                        readOnly=False,
                        )
        self.cm = window.CodeMirror(self.node, options)

    @flx.reaction('size')
    def __on_size(self, *events):
        self.cm.refresh()

    @flx.action
    def set_text(self, text):
        self.cm.setValue(text)
        self.cm.refresh()
        
class FileTree(flx.TreeWidget):

    selected = flx.StringProp("", settable=True, doc='can have any value')

    def init(self):
        # self.relay = relay
        super().init()
        # self.relay = Files()

    @flx.reaction('children**.pointer_double_click')
    def on_event(self, *events):
        for ev in events:
            # if ev.new_value:
            # text = ev.source.text + ' was ' + ev.type
            # print(ev.type, "---", ev.source.path)
            self.set_selected(ev.source.path)
            # 
            # self.emit("select_item", {})
            self.select_item()
            #relay.file_clicked(text)
            # relay.create_message(name, "新语句")
            # self.relay.click_file(text)
            # self.text = text

    # @flx.reaction('select_item')
    # def __select_changed(self, *events):
        
    @flx.emitter
    def select_item(self):
        return {"name":self.selected}

class FileTreeItem(flx.TreeItem):
    
    path = flx.StringProp("", settable=True, doc='file `s path')

    def init(self):
        # self.relay = relay
        super().init()
        # self.relay = Files()

loadassert('plotly.min.js')

class LocalPlotWidget(flx.Widget):
    data = flx.ListProp(settable=True, doc="""
        The data (list of dicts) that describes the plot.
        This can e.g. be the output of the Python plotly API call.
        """)

    layout = flx.DictProp(settable=True, doc="""
        The layout dict to style the plot.
        """)

    config = flx.DictProp(settable=True, doc="""
        The config for the plot.
        """)

    @flx.reaction
    def __relayout(self):
        global Plotly
        w, h = self.size
        if len(self.node.children) > 0:
            Plotly.relayout(self.node, dict(width=w, height=h))

    @flx.reaction
    def _init_plot(self):
        # https://plot.ly/javascript/plotlyjs-function-reference/#plotlynewplot
        # Overwrites an existing plot
        global Plotly
        Plotly.newPlot(self.node, self.data, self.layout, self.config)                               

from pscript import RawJS
# flx.assets.associate_asset(__name__, "https://code.jquery.com/jquery-3.5.1.js")
# flx.assets.associate_asset(__name__,"https://cdn.datatables.net/1.10.21/css/jquery.dataTables.min.css")
# flx.assets.associate_asset(__name__,"https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js")

loadassert('jquery.js')
loadassert('jquery.dataTables.min.js')
loadassert('jquery.dataTables.min.css')

class DataTable(flx.Widget):

    tid = flx.StringProp("", settable=True, doc='table `s id')

    def _create_dom(self):
        global window
        node = self.node = window.document.createElement('table')
        # print("create---", self.tid)
        node.id = self.tid
        node.width="100%"
        return node

    def init(self):
        super().init()
        self.init_tab = False
        
        # global window
        # window.setTimeout(RawJS("$('#tab1').DataTable( {" \
        #     "data: [" \
        #     '[ "Tiger Nixon", "System Architect", "$3,120", "Edinburgh"],' \
        #     '["Garrett Winters", "Director", "$5,300", "Edinburgh"]],' \
        #     "columns: [" \
        #     "{ title: 'name'},{ title: 'salary'},{ title: 'office'},{ title: 'position'}" \
        #     "]} )"), 1000)
        # RawJS("$(document).one('load', '#tab1', function(){$('#tab1').DataTable( {" \
        #     "data: [" \
        #     '[ "Tiger Nixon", "System Architect", "$3,120", "Edinburgh"],' \
        #     '["Garrett Winters", "Director", "$5,300", "Edinburgh"]],' \
        #     "columns: [" \
        #     "{ title: 'name'},{ title: 'salary'},{ title: 'office'},{ title: 'position'}" \
        #     "]} )})")

    @flx.action
    def draw(self):
        # shell = "$('#tab1').DataTable( {" \
        #     "data: [" \
        #     '    [ "Tiger Nixon", "System Architect", "$3,120", "Edinburgh"],' \
        #     '    ["Garrett Winters", "Director", "$5,300", "Edinburgh"]],' \
        #     "columns: [ " \
        #     "    { title: 'name'},{ title: 'salary'},{ title: 'office'},{ title: 'position'}" \
        #     "]} )"
        # print("draw---", shell)
        if not self.init_tab:
            tid = "#"+self.tid
            # print("draw---", tid)
            RawJS("$(tid).DataTable( {" \
                "data: [" \
                '[ "Tiger Nixon", "System Architect", "$3,120", "Edinburgh"],' \
                '["Garrett Winters", "Director", "$5,300", "Edinburgh"]],' \
                "columns: [" \
                "{ title: 'name'},{ title: 'salary'},{ title: 'office'},{ title: 'position'}" \
                "]} )")
            self.init_tab = True
        
        # RawJS("$('#tab1').DataTable( {" \
        #     "data: [" \
        #     '[ "Tiger Nixon", "System Architect", "$3,120", "Edinburgh"],' \
        #     '["Garrett Winters", "Director", "$5,300", "Edinburgh"]],' \
        #     "columns: [" \
        #     "{ title: 'name'},{ title: 'salary'},{ title: 'office'},{ title: 'position'}" \
        #     "]}")

import threading, sys
import queue
from io import StringIO

class CliThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent
        self.queue = queue.Queue(maxsize=1)
        with open("ka.py", "r", encoding='UTF-8') as kf:
            lines = [l for l in kf.readlines()]
            exec("\n".join(lines), globals())
        
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        while True:
            s = self.queue.get(block=True)
            # print(">>>", s)
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            redirected_output = sys.stdout = StringIO()
            redirected_error = sys.stderr = StringIO()
            exec(f"karuncli({str(s)})", globals())
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            stdo = redirected_output.getvalue()
            stde = redirected_error.getvalue()
            if stdo is not None and stdo!="":
                self.parent.output(stdo)
            elif stde:
                self.parent.output(stde)

#语言运行核心
class KaeCore(flx.PyComponent): 
    def init(self, _parent):
        super().init()
        self._parent = _parent
        self.t1 = CliThread(self)
        self.t1.setDaemon(True)
        self.t1.start()

    @flx.action
    def new_statement(self, statement):
        # print(">>", statement)
        self.t1.queue.put_nowait(statement)

    def output(self, msg):
        # self._parent._on_output(msg)
        flx.loop.call_soon(root._on_output, msg)

from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag

class Kae(flx.PyWidget):
    """ This represents one connection to the chat room.
    """
    # CSS = """
    # .flx-main-widget {
    #     background: #e8ffff;
    # }
    # """
    def init(self):
        self.kk = urlmapconf
        self.kaecore = KaeCore(self)
        # pdb = PersonDatabase()
        # with self:
        #     self.jsr = Files()
        with flx.VBox(flex=1, minsize_from_children=False, minsize=350 , style="overflow-y:hidden"):
            with flx.HSplit(flex=1, title=u'kæ语言编辑器', style="overflow-y:hidden"):
                # flx.Widget(flex=1)
                with flx.VBox(flex=1, minsize_from_children=False, minsize=150 , style="overflow-y:hidden"):
                    #self.name_edit = flx.LineEdit(placeholder_text='your name')
                    #self.people_label = flx.Label(flex=1, minsize=250)
                    self.tree = FileTree(flex=1, max_selected=1)
                    for k,v in self.kk.items():
                        guo = FileTreeItem(title=k, checked=None, parent=self.tree)
                        if v is not None:
                            for k2, v2 in v.items():
                                sheng = FileTreeItem(title=k2, checked=None, parent=guo)
                                if k=="磁颐国" and v2 is not None:
                                    self.makepathtreeitem(sheng, v2)
                with flx.TabLayout(flex=2, minsize_from_children=False) as self.tabctrl:
                    with flx.VBox(flex=1, minsize_from_children=False, title="控制台", style="overflow-y:hidden"):
                        with flx.HBox(flex=0) as self.toolbar:
                            # self.msg_edit = flx.LineEdit(flex=1,  placeholder_text=u'输入指令')
                            self.newline = flx.Button(flex=0,text='添加')
                            self.run = flx.Button(flex=0,text='运行')
                            flx.Widget(flex=1)
                        self.messages = MessageList(flex=1, minsize_from_children=False)
                        with flx.HBox(flex=0) as self.inputbar:
                            self.cim = flx.Label(flex=0,text='输入法')
                    with flx.VBox(flex=1, title="文本"):
                        with flx.HBox(flex=0) as self.txttoolbar:
                            self.save = flx.Button(flex=0,text='保存')
                            flx.Widget(flex=1)
                        self.cm = CodeEditor(flex=1)
                    with flx.VBox(flex=1, title="表格"):
                        # self.tabflush = flx.Button(flex=0,text='刷新')
                        self.table = DataTable(tid="table1")
                        
                    with flx.VBox(flex=1, title="图表"):
                        # DataTable(title='Start date')
                        # flx.PlotWidget(xdata=[0,1,2,3,4], ydata=[1,3,4,2,5],
                        #         line_width=4, line_color='red', marker_color='',
                        #         minsize=200)
                        # data = [{'type': 'bar',
                        #         'x': ['giraffes', 'orangutans', 'monkeys'],
                        #         'y': [20, 14, 23]}]
                        values = [
                            ['Salaries', 'Office', 'Merchandise', 'Legal', '<b>TOTAL</b>'],
                            [1200000, 20000, 80000, 2000, 12120000],
                            [1300000, 20000, 70000, 2000, 130902000],
                            [1300000, 20000, 120000, 2000, 131222000],
                            [1400000, 20000, 90000, 2000, 14102000]]

                        data = [{
                            "type": 'table',
                            "header": {
                                "values": [[u"<b>得分</b>"], ["<b>Q1</b>"],
                                            ["<b>Q2</b>"], ["<b>Q3</b>"], ["<b>Q4</b>"]],
                                "align": "center",
                                "line": {"width": 1, "color": 'black'},
                                "fill": {"color": "grey"},
                                "font": {"family": "Arial", "size": 12, "color": "white"}
                            },
                            "cells": {
                                "values": values,
                                "line": {"color": "black", "width": 1},
                                "font": {"family": "Arial", "size": 11, "color": ["black"]}
                            }
                        }]
                        LocalPlotWidget(data=data)
                    # flx.Widget(flex=1)
                # flx.Widget(flex=1)
        # self.table.draw()
        # self._update_participants()
    @flx.action
    def makepathtreeitem(self, node, vals):
        if isinstance (vals , list):
            for f in vals:
                if isinstance(f, str):
                    names = os.path.split(f)
                    FileTreeItem(path=f, title=names[-1], checked=None, parent=node)
                else:
                    self.makepathtreeitem(node, f)
        else:
            for k in vals:
                names = os.path.split(k)
                now = FileTreeItem(path=k, title=names[-1], checked=None, parent=node)
                self.makepathtreeitem(now, vals[k])

    @flx.reaction('newline.pointer_down')
    def _send_message(self, *events):
        # text = self.msg_edit.text
        # if text:
        # name = 'anonymous' #self.name_edit.text or 'anonymous'
        relay.create_message("")
        # self.msg_edit.set_text('')
    @flx.reaction("tabctrl.user_current")
    def refresh_tab(self, *events):
        for ev in events:
            # print(ev.new_value.title)
            if ev.new_value.title=="表格":
                self.table.draw()

    @relay.reaction('create_message')  # note that we connect to relay
    def _push_info(self, *events):
        for ev in events:
            self.messages.add_message(ev.message)

    @flx.action  # note that we connect to relay
    def _on_output(self, msg):
        self.messages.output_message(msg)

    @flx.reaction('tree.select_item')  # note that we connect to relay
    def _on_click_file(self, *events):
        for ev in events:
            # print("reaction>", ev.source.selected)
            if ev.source.selected.endswith(".ae"):
                self.tabctrl.set_current(0)
                with open(ev.source.selected, "r",encoding='utf-8') as file:
                    self.messages.clear()
                    self.messages.add_message(file.read())
            else:
                self.tabctrl.set_current(1)
                with open(ev.source.selected, "r",encoding='utf-8') as file:
                    self.cm.set_text(file.read())
            
    @flx.reaction('messages.run_statement')
    def _run_kae_statement(self, *events):
        for ev in events:
            text = ev.statement
            self.kaecore.new_statement(text)

    @flx.reaction('messages.inputing')
    def pinyin_2_hanzi(self, *events):
        for ev in events:
            dagParams = DefaultDagParams()
            # 10个候选值
            result = dag(dagParams, ev.pinyinList, path_num=10, log=True)
            resset = []
            for item in result:
                socre = item.score # 得分
                res = item.path # 转换结果
                resset.append("".join(res))
                # print(socre, res)
            tlst = [f"{i+1}.{t}" for i,t in enumerate(set(resset))]
            self.cim.set_html("&nbsp;".join(tlst))

        # lists = ['wo', 'you', 'yi', 'zhi', 'xiao', 'mao', 'lv']
        # pinyin_2_hanzi(lists)

    
    # @flx.reaction('name_edit.user_done')  # tell everyone we changed our name
    # def _push_name(self, *events):
    #     relay.new_name()

    # @relay.reaction('new_name')  # check for updated names
    # def _new_name(self, *events):
    #     self._update_participants(self, [])

    # @flx.manager.reaction('connections_changed')
    # def _update_participants(self, *event):
    #     if self.session.status:
    #         # Query the app manager to see who's in the room
    #         sessions = flx.manager.get_connections(self.session.app_name)
    #         # names = [s.app.name_edit.text for s in sessions]
    #         del sessions
            # text = '<br />%i persons in this chat:<br /><br />' % len(names)
            # text += '<br />'.join([name or 'anonymous' for name in sorted(names)])
            # self.people_label.set_html(text)
import os,base64

def loadUrlmaps():
    def makepathtree(node, keyname):
        path = node[keyname]
        fs = os.listdir(path)
        node[keyname] = []
        for f in fs:
            if f.startswith(".") or f=="__pycache__":
                continue
            jp = os.path.join(path, f)
            # print(jp)
            if os.path.isfile(jp):
                node[keyname].append(jp) 
            elif os.path.isdir(jp):
                newnode = {jp:jp}
                node[keyname].append(newnode)
                makepathtree(newnode, jp)
    import yaml
    # from pprint import pprint
    with open("urlmap.yml", 'r',encoding='utf-8') as yf:
        y = yaml.load(yf, Loader=yaml.FullLoader)
        for k,v in y.items():
            if v is not None:
                for k2, v2 in v.items():
                    if k=="磁颐国" and v2 is not None:
                        makepathtree(y[k], k2)
        # pprint(y)
        return y  
urlmapconf = loadUrlmaps()
# print(urlmapconf)

flx.config.hostname = "192.168.2.195"
flx.config.port = 8139

fname = '.asserts/favicon64.ico'
with open(fname, 'rb') as f1:
    base64_str = base64.b64encode(f1.read())  # base64类型
    icos = base64_str.decode()
kae_png = f'data:image/ico;base64,{icos}'
# kae_png = 'favicon32.ico'
# ico = flx.assets.add_shared_data('icon.ico', open(fname, 'rb').read())
# , windowmode="maximized",
app = flx.App(Kae, title=u"kæ语言交互终端", icon=kae_png)
root = app.launch('app', size=(1300, 700), windowmode="maximized")  # to run as a desktop app
#root = app.launch('browser')  # to open in the browser
flx.run()  # mainloop will exit when the app is closed 
# app.serve('')
# # root = app.launch('browser')
# from flexx.app import manager
# manager.register_app(app)
# session = manager.create_session("__main__")
# root = session.app
# flx.start()