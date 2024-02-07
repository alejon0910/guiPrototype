from GUI.browseGUI_build import browserGUI
from GUI.loginGUI_build import loginGUI
from database.db_controller import Controller

class App:
    def __init__(self):
        self.loop()


    def loop(self):

        self.controller = Controller()
        self.login = loginGUI(self.controller)
        self.login.mainloop()

        if self.controller.current_id is not None:
            self.browser = browserGUI(self.controller)
            self.browser.mainloop()

        if self.browser.signed_out and self.login.access:
            self.loop()


app = App()