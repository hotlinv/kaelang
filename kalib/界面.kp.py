# 【引用】

# 【映射】
ka_pmap=KaeLevMap(lev0={
    u"展示“(.+)”所描述的用户界面":"ka_gui_open(os.path.join(ka_workspace(), '数据描述', '{0}.yml'))",
})

# 【实现】
from kivy.uix.treeview import TreeView, TreeViewLabel

class FileTree(TreeView):
    def __init__(self, **kwargs):
        self.register_event_type('on_create')
        super(FileTree, self).__init__(**kwargs)
        self.dispatch('on_create')
    def on_create(self):
        n1 = self.add_node(TreeViewLabel(text='项 1', font_name='fzh'))
        self.add_node(TreeViewLabel(text='SubItem 1', font_name='fzh'), n1)
        self.add_node(TreeViewLabel(text='SubItem 2', font_name='fzh'), n1)

@catch2cn
def ka_gui_open(uiconfig):
    """打开ui界面"""
    from kivy.app import App as kvApp
    from kivy.lang import Builder as kvBuilder

    from kivy.core.text import LabelBase as kvLabelBase
    
    kvLabelBase.register(name='fzh',fn_regular='.asserts/sarasa.ttf')

    class TestApp(kvApp):
        def build(self):
            with open(uiconfig, encoding="utf-8") as f:
                uiconf = f.read()

            root = kvBuilder.load_string(uiconf)
            self.icon = root.app_icon
            self.title = root.app_title
            return root
    
    app = TestApp()
    ka_vals["guiapp"] = app
    app.run()
    