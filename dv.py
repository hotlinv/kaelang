
from flexx import flx

class Relay(flx.Component):
    """ Global object to relay messages to all participants.
    """

    @flx.emitter
    def create_message(self, name, message):
        return dict(name=name, message=message)

    @flx.emitter
    def new_name(self):
        return {}

    @flx.emitter
    def click_file(self, name):
        return dict(name=name)

    @flx.action
    def file_clicked(self, name):
        self.emit("click_file", name)
    

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

    def init(self):
        super().init()
        #self._se = window.document.createElement('div')
        with flx.VBox(flex=1, minsize_from_children=True, style="position:relative") as self.outer:
            with flx.HBox(flex=0, minsize_from_children=True):
                self.lab = flx.Label(flex=0, text="我：")
                self.msg_edit = MultiLineEdit(flex=1, minsize_from_children=True)
                self.ok = flx.Button(text='！')
            with flx.HBox(flex=0, minsize_from_children=True):
                flx.Label(flex=0, text="æ：")
                with flx.VBox(flex=1,  minsize_from_children=True):
                    self.output = flx.Label(flex=0,  minsize_from_children=True)

    @flx.reaction('ok.pointer_click')
    def a_button_was_pressed(self, *events):
        ev = events[-1]  # only care about last event
        self.output.set_html("<br/>".join(self.msg_edit.text.split()))
    @flx.reaction('msg_edit.pointer_click')
    def a_edit_was_selected(self, *events):
        parent = self.parent
        for c in parent.children:
            c.apply_style("background-color:#e8e8e8")
        self.apply_style("background-color:#fafafa")

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

    def init(self):
        super().init()
        global window
        #self._se = window.document.createElement('div')
        # with flx.VBox(flex=0, style="overflow:auto"):
        #     with flx.VBox(flex=0, minsize_from_children=True) as self.msglst:
                # self.msglst.minsize_from_children = False
        MessageItem()
                #self.output = flx.Label(flex=1, text="结果：")
            
            # flx.Widget(flex=1)

    def sanitize(self, text):
        self._se.textContent = text
        text = self._se.innerHTML
        self._se.textContent = ''
        return text

    @flx.action
    def add_message(self, name, msg):
        # line = '<i>' + self.sanitize(name) + '</i>: ' + self.sanitize(msg)
        # self.set_html(self.html + line + '<br />')
        MessageItem(parent=self)


# Associate CodeMirror's assets with this module so that Flexx will load
# them when (things from) this module is used.
base_url = 'http://cdnjs.cloudflare.com/ajax/libs/codemirror/'
flx.assets.associate_asset(__name__, base_url + '5.21.0/codemirror.min.css')
flx.assets.associate_asset(__name__, base_url + '5.21.0/codemirror.min.js')
flx.assets.associate_asset(__name__, base_url + '5.21.0/mode/python/python.js')
flx.assets.associate_asset(__name__, base_url + '5.21.0/theme/solarized.css')
flx.assets.associate_asset(__name__, base_url + '5.21.0/addon/selection/active-line.js')
flx.assets.associate_asset(__name__, base_url + '5.21.0/addon/edit/matchbrackets.js')


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
            print(ev.type, "---", ev.source.path)
            self.set_selected(ev.source.path)
            # 
            self.emit("select_item", {})
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
                            self.ok = flx.Button(flex=0,text='添加')
                            self.run = flx.Button(flex=0,text='运行')
                            flx.Widget(flex=1)
                        self.messages = MessageList(flex=1, minsize_from_children=False)
                        with flx.HBox(flex=0) as self.inputbar:
                            flx.Label(flex=0,text='输入法')
                    with flx.VBox(flex=1, title="文本"):
                        with flx.HBox(flex=0) as self.txttoolbar:
                            self.save = flx.Button(flex=0,text='保存')
                            flx.Widget(flex=1)
                        self.cm = CodeEditor(flex=1)
                    # flx.Widget(flex=1)
                # flx.Widget(flex=1)

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

    @flx.reaction('ok.pointer_down')
    def _send_message(self, *events):
        # text = self.msg_edit.text
        # if text:
        name = 'anonymous' #self.name_edit.text or 'anonymous'
        relay.create_message(name, "新语句")
        # self.msg_edit.set_text('')

    @relay.reaction('create_message')  # note that we connect to relay
    def _push_info(self, *events):
        for ev in events:
            self.messages.add_message(ev.name, ev.message)

    @flx.reaction('tree.select_item')  # note that we connect to relay
    def _on_click_file(self, *events):
        for ev in events:
            print("reaction>", ev.source.selected)
            if ev.source.selected.endswith(".ae"):
                self.tabctrl.set_current(0)
            else:
                self.tabctrl.set_current(1)
                with open(ev.source.selected, "r",encoding='utf-8') as file:
                    self.cm.set_text(file.read())


            
    
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


fname = 'favicon64.ico'
with open(fname, 'rb') as f1:
    base64_str = base64.b64encode(f1.read())  # base64类型
    icos = base64_str.decode()
kae_png = f'data:image/ico;base64,{icos}'
# kae_png = 'favicon32.ico'
# ico = flx.assets.add_shared_data('icon.ico', open(fname, 'rb').read())
app = flx.App(Kae, title=u"kæ语言交互终端", icon=kae_png, size=(1000, 800))
app.launch('app')  # to run as a desktop app
# app.launch('browser')  # to open in the browser
flx.run()  # mainloop will exit when the app is closed    