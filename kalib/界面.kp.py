# 【引用】

# 【映射】
ka_pmap=KaeLevMap(lev0={
    u"读取用户界面“(.+)”":"ka_gui_open(os.path.join(ka_workspace(), '数据描述', '{0}.yml'), '{0}')",
    u"展示用户界面《(.+)》":"ka_gui_run('{0}')",
    u"在控件“(.+)”上守候":"ka_gui_find_ctl('{0}')",
    u"当其初始化完成时，读取数据“(.+)”":"ka_gui_setdata('{0}')",
})

# 【实现】
# from kivy.uix.treeview import TreeView, TreeViewLabel

# class FileTree(TreeView):
#     def __init__(self, **kwargs):
#         self.register_event_type('on_create')
#         super(FileTree, self).__init__(**kwargs)
#         self.dispatch('on_create')
#     def on_create(self):
#         n1 = self.add_node(TreeViewLabel(text='项 1', font_name='fzh'))
#         self.add_node(TreeViewLabel(text='SubItem 1', font_name='fzh'), n1)
#         self.add_node(TreeViewLabel(text='SubItem 2', font_name='fzh'), n1)

# from kivy.uix.boxlayout import BoxLayout
# class MyPanel(BoxLayout):
#     def __init__(self, **kwargs):
#         super(MyPanel, self).__init__(**kwargs)
#     def addPanel(self):
#         from kivy.lang import Builder as kvBuilder
#         with open(os.path.join(ka_workspace(), '数据描述', '交互面板.yml'), encoding="utf-8") as f:
#                 pconf = f.read()

#         p = kvBuilder.load_string(pconf)
#         self.add_widget(p)

def init_tree_view(tree_view, parent, node):
    from kivy.uix.treeview import TreeViewLabel
    if parent is None:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                     is_open=True))
    else:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                     is_open=True), parent)

    for child_node in node['children']:
        init_tree_view(tree_view, tree_node, child_node)

@catch2cn
def ka_gui_setdata(dataname):
    # data = ka_vals[f"{dataname}"]
    ui = ka_vals[f"{ka_lastit}"]
    ui.binds[-1].append(dataname)
    #ka_vals[f"{ka_lastit}_cur"] = curel

@catch2cn
def ka_gui_find_ctl(ctlid):
    ui = ka_vals[f"{ka_lastit}"]
    ui.binds.append([f"self.root.ids.{ctlid}"])
    # curel = eval(f"ui.ids.{ctlid}")
    # ka_vals[f"{ka_lastit}_cur"] = curel
    # print("********", ka_lastit, ui, ui.root)

@catch2cn
@lastit
def ka_gui_open(uiconfig, name):
    """打开ui界面"""
    from kivy.app import App as kvApp
    from kivy.lang import Builder as kvBuilder

    from kivy.core.text import LabelBase as kvLabelBase
    
    kvLabelBase.register(name='fzh',fn_regular='.asserts/sarasa.ttf')

    class TestApp(kvApp):
        def on_start(self):
            # print(self.root.ids.tree)
            for b in self.binds:
                ctl = eval(b[0])
                print(b)
                #init_tree_view(ctl, None, ka_vals[b[1]])
        def build(self):
            with open(uiconfig, encoding="utf-8") as f:
                uiconf = f.read()

            root = kvBuilder.load_string(uiconf)
            self.icon = root.app_icon
            self.title = root.app_title
            return root
    
    app = TestApp()
    app.binds = []
    ka_vals[name] = app
    return name

@catch2cn
def ka_gui_run(name):
    ka_vals[name].run()
    