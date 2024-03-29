import tkinter as tk
from GUI.signupGUI_build import signupGUI

class loginGUI(tk.Tk):

    def __init__(self, controller):
        super().__init__()

        self.title("clippr")
        self.iconbitmap(r"GUI\images\icon.ico")
        self.config(background="white")
        self.geometry("550x370")
        self.resizable(False, False)
        self.access = False
        self.id = None
        self.signup = None
        self.controller = controller
        self.clippr_photo = tk.PhotoImage(file=r"GUI\images\clipprblack.png")

        self.build()

    # This function creates, binds and places the window's Tkinter widgets
    def build(self):

        self.clippr_logo = tk.Label(self, image=self.clippr_photo, bg="white", borderwidth=0,
                                    highlightthickness=0)
        self.username_entry = tk.Entry(self, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                       relief="flat", fg="#b0b0b0", font=("Soleil-Book",10))
        self.password_entry = tk.Entry(self, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                       relief="flat", fg="#b0b0b0", font=("Soleil-Book",10))
        self.error_label = tk.Label(self, background="white", text="", highlightthickness=0, fg="#b0b0b0", font=("Soleil-Book",10))

        self.login_button = tk.Button(self, background="white", text="Log In",
                                               highlightthickness=0, fg="black", font=("SoleilXb", 10),
                                               relief="flat", command=self.sign_in)
        self.create_account_button = tk.Button(self, background="white", text="No sign in? Create Account", highlightthickness=0, fg="black", font=("Soleil-Book",9), relief="flat", command=self.open_signup)

        self.username_entry.insert(0, "Username")
        self.password_entry.insert(0, "Password")

        self.username_entry.bind("<Button-1>", lambda x: [self.username_clicked(), self.username_entry.config(fg="black")])
        self.password_entry.bind("<Button-1>", lambda x: [self.password_clicked(), self.password_entry.config(fg="black", show='•')])
        self.bind("<Return>", lambda x: [self.sign_in()])

        # Place navigation buttons
        self.clippr_logo.place(x=80, y=20)
        self.username_entry.place(x=200, y=170, width=150, height=25)
        self.password_entry.place(x=200, y=200, width=150, height=25)
        self.login_button.place(x=250, y=240)
        self.create_account_button.place(x=195, y=270)

    # This function clears the filler text in username_entry widget when it is clicked;
    # refills the password_entry widget if it is empty
    def username_clicked(self):
        if self.username_entry.get() == "Username":
            self.username_entry.delete(0, "end")
            self.username_entry.config(fg="black")
        if len(self.password_entry.get()) == 0:
            self.password_entry.insert(0, "Password")
            self.password_entry.config(fg="#b0b0b0", show='')

    # This function clears the filler text in password_entry widget when it is clicked;
    # refills the username_entry widget if it is empty
    def password_clicked(self):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, "end")
            self.password_entry.config(fg="black")
        if len(self.username_entry.get()) == 0:
            self.username_entry.insert(0, "Username")
            self.username_entry.config(fg="#b0b0b0", show='')

    # This function creates, binds and places the window's Tkinter widgets
    def get_details(self):

        if self.username_entry.get() != "" and self.username_entry.get() != "Username" and self.password_entry.get() != "" and self.password_entry.get() != "Password":
            username = self.username_entry.get()
            password = self.password_entry.get()
            return username, password

        else:
            self.error_label.place(x=154, y=300)
            self.error_label.config(text="Please enter a username and password")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))
            return None, None

    # This function attempts a login; opens browsing window if successful and prints error if not
    def sign_in(self):

        username, password = self.get_details()
        self.access = self.controller.sign_in(username, password)

        if self.access:
            self.destroy()
        else:
            self.error_label.place(x=170, y=300)
            self.error_label.config(text="Incorrect username or password")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))

    # This function opens a sign-up window, preventing any more from being opened
    def open_signup(self):
        if self.signup is None:
            self.signup = signupGUI(self, self.controller)
            self.signup.username_entry.bind("<Destroy>", lambda x: self.allow_signup())

    # This function frees up a sign-up window to be opened
    def allow_signup(self):
        self.signup = None