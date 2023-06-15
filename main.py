from browseGUI_build import browserGUI
from accountGUI_build import signinGUI

signin = signinGUI()
signin.mainloop()

if signin.access:
    browser = browserGUI()
    browser.mainloop()
