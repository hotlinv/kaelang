
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.splitter import Splitter
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader

from kivy.core.text import LabelBase
LabelBase.register(name='fzh',fn_regular='.asserts/sarasa.ttf')

class FileTree(TreeView):
    def __init__(self, **kwargs):
        super(FileTree, self).__init__(**kwargs)
        n1 = self.add_node(TreeViewLabel(text='项 1', font_name='fzh'))
        self.add_node(TreeViewLabel(text='SubItem 1', font_name='fzh'), n1)
        self.add_node(TreeViewLabel(text='SubItem 2', font_name='fzh'), n1)


class KaeApp(App):
    def build(self):
        self.icon = '.asserts/favicon.ico'
        self.title = "kæ语言交互终端"
        root = BoxLayout()

        splitter = Splitter(size_hint=(.25, 1), sizable_from = 'right')
        splitter.add_widget(FileTree(hide_root=True))
        splitter.min_size = 200
        splitter.max_size = 350
        root.add_widget(splitter)

        tp = TabbedPanel()
        tp.default_tab_text = "语言交互"
        tp.default_tab_content = Button()
        th = TabbedPanelHeader(text='文本', font_name='fzh')
        label = Label(text='kæ语言交互终端', font_name='fzh',
                      size_hint=(.7, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        th.content = label
        tp.add_widget(th)
        root.add_widget(tp)
        
        return root

if __name__ == '__main__':
    app = KaeApp()
    app.run()