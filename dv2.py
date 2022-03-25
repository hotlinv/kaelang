
from kivy.app import App
from kivy.lang import Builder

from kivy.core.text import LabelBase
LabelBase.register(name='fzh',fn_regular='.asserts/sarasa.ttf')

with open("数据描述/控制台界面.yml", encoding="utf-8") as f:
    uiconf = f.read()

root = Builder.load_string(uiconf)

class TestApp(App):
    def build(self):
        return root

if __name__ == '__main__':
    TestApp().run()
