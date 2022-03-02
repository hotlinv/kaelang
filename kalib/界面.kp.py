# 【引用】

# 【映射】
ka_pmap=KaeLevMap(lev0={
    u"读取用户界面“(.+)”":"ka_gui_open(os.path.join(ka_workspace(), '数据描述', '{0}.yml'), '{0}')",
    u"展示用户界面《(.+)》":"ka_gui_run('{0}')",
    u"在控件“(.+)”上守候":"ka_gui_find_ctl('{0}')",
    u"当其初始化完成时，读取数据“(.+)”":"ka_gui_setdata('{0}')",
    u"当其(.+)时，(.+)":"ka_gui_bind('{0}', '{1}')"
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

def set_TreeView(tree_view, node, parent=None):
    from kivy.uix.treeview import TreeViewLabel
    if parent is None:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'], font_name='fzh',
                                                     is_open=True))
    else:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'], font_name='fzh',
                                                     is_open=True), parent)
    if node['children'] is not None:
        for child_node in node['children']:
            set_TreeView(tree_view, child_node, tree_node)

@catch2cn
def ka_gui_setdata(dataname):
    # data = ka_vals[f"{dataname}"]
    ui = ka_vals[ka_lastit]
    what = ui.binds[-1]
    what.append(f"set_%s({what[0]}, ka_vals['{dataname}'])")
    #ka_vals[f"{ka_lastit}_cur"] = curel

def ka_gui_bind(whenst, bind):
    ui = ka_vals[ka_lastit]
    print("u"*20, ui)
    what = ui.binds[-1]
    print("u"*20, what)
    what.append(f"pass")
    #print(whenst, bind)

@catch2cn
def ka_gui_find_ctl(ctlid):
    ui = ka_vals[f"{ka_lastit}"]
    print("g"*20, ui.idpair)
    wid = ui.idpair[ctlid]
    ui.binds.append([f"self.root.ids.{wid}"])
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
            # init_TreeView(self.root.ids.tree, None, ka_vals['配置树'])
            for b in self.binds:
                _classname = str(eval(b[0]).__class__)
                clsname = _classname[_classname.find("'")+1:_classname.rfind("'")].split(".")[-1]
                # print("^"*10, clsname)

                for ec in b[1:]:
                    print("^"*10, ec, clsname)
                    exec(ec % clsname)
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
    import yaml
    with open(uiconfig+".idp", 'r',encoding='utf-8') as f:
        uiconf = yaml.load(f, Loader=yaml.FullLoader)
        # conf = kvBuilder.load_string(uiconf)
        # loopwidget(conf)
        app.idpair = {ck:cv for ck, cv in uiconf.items()}
        print(app.idpair)
    ka_vals[name] = app
    return name

@catch2cn
def ka_gui_run(name):
    ka_vals[name].run()
    