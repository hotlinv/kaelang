
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

class MessageItem(flx.VBox):

    CSS = """
    .flx-MessageItem {
        overflow-y:hidden;
        background: #e8e8e8;
        border: 1px solid #444;
        margin: 3px;
    }
    """

    def init(self):
        super().init()
        global window
        #self._se = window.document.createElement('div')
        with flx.HBox(flex=0):
            self.lab = flx.Label(flex=0, text="[ ]")
            self.msg_edit = flx.LineEdit(flex=1, placeholder_text=u'输入指令')
            self.ok = flx.Button(text='运行')
        self.output = flx.Label(flex=1, text="结果：")

    # @flx.reaction('box.children*.pointer_click')
    # def a_button_was_pressed(self, *events):
    #     ev = events[-1]  # only care about last event
    #     self.label.set_text(ev.source.id + ' was pressed')

class MessageBox(flx.VBox):

    CSS = """
    .flx-MessageBox {
        overflow:auto;
        background: #e8ffe8;
        border: 1px solid #444;
        margin: 3px;
        max-height:300px;
    }
    """

    def init(self):
        super().init()
        global window
        #self._se = window.document.createElement('div')
        with flx.VBox(flex=0, style="overflow-y:auto") as self.msglst:
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
        

class Kae(flx.PyWidget):
    """ This represents one connection to the chat room.
    """

    def init(self):
        with flx.HSplit(title=u'kæ语言编辑器', style="overflow-y:hidden"):
            # flx.Widget(flex=1)
            with flx.VBox(flex=1, minsize=150 , style="overflow-y:hidden"):
                #self.name_edit = flx.LineEdit(placeholder_text='your name')
                #self.people_label = flx.Label(flex=1, minsize=250)
                with flx.TreeWidget(flex=1, max_selected=1) as self.tree:
                    for t in ['foo', 'bar']:
                        with flx.TreeItem(text=t, checked=None):
                            for i in range(4):
                                item2 = flx.TreeItem(text=t + ' %i' % i, checked=False)
            with flx.VBox(flex=2, style="overflow-y:hidden"):
                with flx.HBox(flex=0, style="float:left"):
                    # self.msg_edit = flx.LineEdit(flex=1,  placeholder_text=u'输入指令')
                    self.ok = flx.Button(flex=0,text='添加')
                    self.run = flx.Button(flex=0,text='运行')
                    flx.Widget(flex=1)
                self.messages = MessageBox(flex=1, style="float:left")
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

app = flx.App(Kae, title=u"kae语言交互终端", size=(1000, 800))
app.launch('app')  # to run as a desktop app
# app.launch('browser')  # to open in the browser
flx.run()  # mainloop will exit when the app is closed    