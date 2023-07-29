from GUI.browseGUI_build import browserGUI
from GUI.loginGUI_build import loginGUI
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

class App:
    def __init__(self):

        self.loop()

    def loop(self):

        self.login = loginGUI(self)
        self.login.mainloop()

        if self.login.access:
            self.browser = browserGUI(self, self.login.id)
            self.browser.mainloop()

        if self.browser.signed_out and self.login.access:
            self.loop()


app = App()