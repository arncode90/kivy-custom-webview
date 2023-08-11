from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp

from webview_screen import WebviewModal


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        """ assign webview """
        self.webview = WebviewModal()

    # def on_enter(self, *args):
    #     site = 'https://www.google.com/'
    #     Clock.schedule_once(lambda d: self.button_pressed(site))

    def button_pressed(self, target: str):
        """ target is web url """
        self.webview.url = target
        self.webview.open()


class MainApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='home'))
        return sm


if __name__ == '__main__':
    MainApp().run()
