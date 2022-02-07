# 【引用】

# 【映射】
ka_pmap=KaeLevMap(lev0={
    u"展示“(.+)”所描述的用户界面":"ka_gui_open(os.path.join(ka_workspace(), '数据描述', '{0}.yml'))",
})

# 【实现】

@catch2cn
def ka_gui_open(uiconfig):
    """打开ui界面"""
    from kivy.app import App as kvApp
    from kivy.lang import Builder as kvBuilder

    from kivy.core.text import LabelBase as kvLabelBase
    
    kvLabelBase.register(name='fzh',fn_regular='.asserts/sarasa.ttf')

    with open(uiconfig, encoding="utf-8") as f:
        uiconf = f.read()

    root = kvBuilder.load_string(uiconf)

    class TestApp(kvApp):
        def build(self):
            return root
    
    app = TestApp()
    ka_vals["guiapp"] = app
    app.run()
    