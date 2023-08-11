import inspect
from kivy import platform
from kivy.core.window import Window
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.widget import Widget

if platform == 'android':
    from android.runnable import run_on_ui_thread
    from android import api_version, mActivity
    from jnius import autoclass, cast, java_method, PythonJavaClass

    Intent = autoclass('android.content.Intent')
    wv = autoclass('android.webkit.WebView')
    # wvc = autoclass('android.webkit.WebViewClient')
    wsr = autoclass('android.webkit.WebSettings$RenderPriority')
    View = autoclass('android.view.View')
    viewGroup = autoclass('android.view.ViewGroup')
    layoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    context = autoclass('android.content.Context')
    ActivityManager = autoclass('android.app.ActivityManager')
    activityManager = cast('android.app.ActivityManager',
                           mActivity.getSystemService(context.ACTIVITY_SERVICE))
    processInfo = activityManager.getRunningAppProcesses()
    packageName = mActivity.getPackageName()
    wvSuffix = wv.setDataDirectorySuffix
    CustomWebViewClient = autoclass('org.arncode.CustomWebViewClient')

    if api_version >= 28:
        for pInfo in processInfo:
            if pInfo.processName != packageName:
                wvSuffix(pInfo.processName)

    class CallbackWrapper(PythonJavaClass):
        """
        javacontext: app is needed (since using custom java in the app)
        else an error will happen
        """
        __javacontext__ = 'app'
        __javainterfaces__ = ['org/arncode/CallbackWrapper']

        def __init__(self, target):
            super().__init__()
            self.target = target

        @java_method('(Landroid/webkit/WebView;Ljava/lang/String;Landroid/graphics/Bitmap;)V')
        def onPageStarted(self, view, url, favicon):
            pass
            # if self.target:
            #     self.target.page_started = view, url, favicon
                # return as tuple

        @java_method('(Landroid/webkit/WebView;Ljava/lang/String;)V')
        def onPageFinished(self, view, url):
            pass
            # if self.target:
            #     self.target.page_finished = view, url
                # return as tuple

        @java_method('(Landroid/webkit/WebView;Ljava/lang/String;)V')
        def onPageCommitVisible(self, view, url):
            pass
            # if self.target:
            #     self.target.page_commit_visible = view, url
                # return as tuple

        @java_method('(Landroid/webkit/WebView;Landroid/webkit/WebResourceRequest;Landroid/webkit/WebResourceError;)V')
        def onReceivedError(self, view, request, error):
            pass
            # if self.target:
            #     self.target.received_error = view, request, error
                # return as tuple

        @java_method('(Ljava/lang/String;)Z')
        def shouldOverrideUrlLoading(self, url):
            if self.target:
                self.target.should_override_url_loading = url

else:
    def run_on_ui_thread(f):
        """ Bypass run_on_ui_thread when running on pc """
        def wrapper(self, *args, **kw):
            try:
                return f(self, *args, **kw)
            except Exception as e:
                print('BYPASS ERROR: >> ', self.__class__, inspect.trace()[1][3])
        return wrapper


class WebviewClass(Widget):
    url = StringProperty()

    """ webview size: w, h, x, y """
    webview_size = ListProperty([Window.width, Window.height, 0, 0])

    """ WEBVIEW CLIENT METHODS """
    page_started = ObjectProperty()
    page_finished = ObjectProperty()
    page_commit_visible = ObjectProperty()
    received_error = ObjectProperty()
    should_override_url_loading = ObjectProperty()

    def __init__(self, **kwargs):
        super(WebviewClass, self).__init__(**kwargs)
        self.webview = None
        self.custom_webview_client = None
        self.callback_wrapper = None
        self.webview_setup()

    @run_on_ui_thread
    def webview_setup(self):
        """ assign every java to a variable to avoid jnius error (garbage collector is the cause) """
        self.webview = wv(mActivity)
        self.callback_wrapper = CallbackWrapper(self)
        self.custom_webview_client = CustomWebViewClient(self.callback_wrapper)
        self.webview.setWebViewClient(self.custom_webview_client)
        self.webview.getSettings().setRenderPriority(wsr.HIGH)
        self.webview.getSettings().setJavaScriptEnabled(False)
        self.webview.getSettings().setSafeBrowsingEnabled(True)
        self.webview.getSettings().setBuiltInZoomControls(True)
        self.webview.getSettings().setDisplayZoomControls(False)
        self.webview.getSettings().setAllowFileAccess(True)
        self.webview.setVisibility(View.GONE)
        mActivity.addContentView(self.webview, layoutParams(Window.width, Window.height))

    @run_on_ui_thread
    def on_webview_size(self, _, view_size):
        """ SET WEBVIEW SIZE """
        params = self.webview.getLayoutParams()
        params.width = int(self.webview_size[0])
        params.height = int(self.webview_size[1])
        self.webview.setLayoutParams(params)
        self.webview.setX(self.webview_size[2])
        self.webview.setY(self.webview_size[3])

    @run_on_ui_thread
    def webview_open(self):
        self.webview.loadUrl(self.url)
        self.webview.setVisibility(View.VISIBLE)

    @run_on_ui_thread
    def webview_close(self):
        self.webview.stopLoading()
        self.webview.setVisibility(View.GONE)
