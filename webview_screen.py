from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.properties import BooleanProperty
from droid.webview import WebviewClass

Builder.load_file('webview_screen.kv')


class WebviewModal(WebviewClass, ModalView):
    webview_box = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(WebviewModal, self).__init__(**kwargs)

    @mainthread
    def on_open(self):
        """ Set webview size once, and open/show the webview """
        if not self.webview_box:
            x_pos = self.ids.webview_size.x
            y_pos = self.ids.search_bar.height + self.ids.search_bar.parent.padding[0] + \
                    self.ids.search_bar.parent.spacing
            self.webview_size = [self.ids.webview_size.width, self.ids.webview_size.height,
                                 x_pos, y_pos]
            self.webview_box = True
        self.webview_open()
        self.ids.search_input.text = self.url
        self.ids.search_input.cursor = (0, 0)

    @mainthread
    def on_dismiss(self):
        """ Hide webview when modal view is dismiss """
        self.webview_close()

    @mainthread
    def open_website_url(self, link: str):
        """ target is web url from search bar MDTextField input """
        link = "https://www.google.com/search?q=" + link
        self.url = link
        self.webview_open()

    @mainthread
    def on_should_override_url_loading(self, _, obj):
        """
        usage of on_should_override_url_loading from :
            -> WebviewClass.should_override_url_loading : ObjectProperty()
        refer to :
            webview.py > class CallbackWrapper(PythonJavaClass) > shouldOverrideUrlLoading method
        """
        self.ids.search_input.text = str(obj)
        self.ids.search_input.cursor = (0, 0)
