from GUI.browseGUI_build import browserGUI
from GUI.loginGUI_build import loginGUI
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

class App:
    def __init__(self):

        self.login = loginGUI(self)
        self.login.mainloop()

        if self.login.access:
            browser = browserGUI(self, self.login.id)
            browser.mainloop()

app = App()