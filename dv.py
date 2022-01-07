
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

# Create global relay
relay = Relay()

class MessageItem(flx.Widget):

    CSS = """
    .flx-MessageItem {
        overflow:hidden;
        background: #e8e8e8;
        border: 1px solid #444;
        margin: 3px;
    }
    """

    def init(self):
        super().init()
        #self._se = window.document.createElement('div')
        with flx.VBox(flex=0):
            with flx.HBox(flex=1):
                self.lab = flx.Label(flex=0, text="[ ]")
                self.msg_edit = flx.LineEdit(flex=1, placeholder_text=u'输入指令')
                self.ok = flx.Button(text='运行')
            self.output = flx.Label(flex=1, text="结果：")

    # @flx.reaction('box.children*.pointer_click')
    # def a_button_was_pressed(self, *events):
    #     ev = events[-1]  # only care about last event
    #     self.label.set_text(ev.source.id + ' was pressed')

class MessageList(flx.Widget):

    CSS = """
    .flx-MessageList {
        overflow:auto;
        background: #e8ffe8;
        border: 1px solid #444;
        margin: 3px;
    }
    """

    def init(self):
        super().init()
        global window
        #self._se = window.document.createElement('div')
        with flx.VBox(flex=0):
            with flx.VBox(flex=0) as self.msglst:
                # self.msglst.minsize_from_children = False
                MessageItem(flex=0)
                #self.output = flx.Label(flex=1, text="结果：")
            
            flx.Widget(flex=1)

    def sanitize(self, text):
        self._se.textContent = text
        text = self._se.innerHTML
        self._se.textContent = ''
        return text

    @flx.action
    def add_message(self, name, msg):
        # line = '<i>' + self.sanitize(name) + '</i>: ' + self.sanitize(msg)
        # self.set_html(self.html + line + '<br />')
        MessageItem(parent=self.msglst)


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
        

class Kae(flx.PyWidget):
    """ This represents one connection to the chat room.
    """
    # CSS = """
    # .flx-main-widget {
    #     background: #e8ffff;
    # }
    # """
    def init(self):
        with flx.VBox(flex=1, minsize_from_children=False, minsize=350 , style="overflow-y:hidden"):
            with flx.HSplit(flex=1, title=u'kæ语言编辑器', style="overflow-y:hidden"):
                # flx.Widget(flex=1)
                with flx.VBox(flex=1, minsize_from_children=False, minsize=150 , style="overflow-y:hidden"):
                    #self.name_edit = flx.LineEdit(placeholder_text='your name')
                    #self.people_label = flx.Label(flex=1, minsize=250)
                    with flx.TreeWidget(flex=1, max_selected=1) as self.tree:
                        for t in ['foo', 'bar']:
                            with flx.TreeItem(text=t, checked=None):
                                for i in range(4):
                                    flx.TreeItem(text=t + ' %i' % i, checked=False)
                with flx.TabLayout(flex=2, minsize_from_children=False):
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
                        CodeEditor(flex=1)
                    # flx.Widget(flex=1)
                # flx.Widget(flex=1)

        self._update_participants()

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

    # @flx.reaction('name_edit.user_done')  # tell everyone we changed our name
    # def _push_name(self, *events):
    #     relay.new_name()

    # @relay.reaction('new_name')  # check for updated names
    # def _new_name(self, *events):
    #     self._update_participants(self, [])

    @flx.manager.reaction('connections_changed')
    def _update_participants(self, *event):
        if self.session.status:
            # Query the app manager to see who's in the room
            sessions = flx.manager.get_connections(self.session.app_name)
            # names = [s.app.name_edit.text for s in sessions]
            del sessions
            # text = '<br />%i persons in this chat:<br /><br />' % len(names)
            # text += '<br />'.join([name or 'anonymous' for name in sorted(names)])
            # self.people_label.set_html(text)
import os,base64
fname = 'favicon64.ico'
with open(fname, 'rb') as f1:
    base64_str = base64.b64encode(f1.read())  # base64类型
    icos = base64_str.decode()
kae_png = f'data:image/ico;base64,{icos}'
# kae_png = 'favicon32.ico'
# ico = flx.assets.add_shared_data('icon.ico', open(fname, 'rb').read())
app = flx.App(Kae, title=u"kae语言交互终端", icon=kae_png, size=(1000, 800))
app.launch('app')  # to run as a desktop app
# app.launch('browser')  # to open in the browser
flx.run()  # mainloop will exit when the app is closed    