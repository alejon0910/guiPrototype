import tkinter as tk
from GUI.signupGUI_build import signupGUI

class loginGUI(tk.Tk):

    def __init__(self, controller):
        super().__init__()

        self.title("clippr")
        self.iconbitmap(r"GUI\images\icon.ico")
        self.config(background="white")
        self.geometry("550x350")
        self.resizable(False, False)
        self.access = False
        self.id = None
        self.signup = None
        self.controller = controller

        self.clippr_photo = tk.PhotoImage(file=r"GUI\images\clipprblack.png")

        # Logo
        self.clippr_logo = tk.Label(self, image=self.clippr_photo, bg="white", borderwidth=0,
                                    highlightthickness=0)
        self.username_entry = tk.Entry(self, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                       relief="flat", fg="#b0b0b0", font=("Soleil-Book",10))
        self.password_entry = tk.Entry(self, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                       relief="flat", fg="#b0b0b0", font=("Soleil-Book",10))
        self.error_label = tk.Label(self, background="white", text="", highlightthickness=0, fg="black", font=("Soleil-Book",10))
        self.create_account_button = tk.Button(self, background="white", text="No sign in? Create Account", highlightthickness=0, fg="black", font=("Soleil-Bold",10), relief="flat", command=self.open_signup)

        self.username_entry.insert(0, "Username")
        self.password_entry.insert(0, "Password")

        self.username_entry.bind("<Button-1>", lambda x: [username_clicked(), self.username_entry.config(fg="black")])
        self.password_entry.bind("<Button-1>", lambda x: [password_clicked(), self.password_entry.config(fg="black", show='•')])
        self.bind("<Return>", lambda x: [self.sign_in()])

        def username_clicked():
            if self.username_entry.get() == "Username":
                self.username_entry.delete(0, "end")
                self.username_entry.config(fg="black")
            if len(self.password_entry.get()) == 0:
                self.password_entry.insert(0, "Password")
                self.password_entry.config(fg="#b0b0b0", show='')

        def password_clicked():
            if self.password_entry.get() == "Password":
                self.password_entry.delete(0, "end")
                self.password_entry.config(fg="black")
            if len(self.username_entry.get()) == 0:
                self.username_entry.insert(0, "Username")
                self.username_entry.config(fg="#b0b0b0", show='')

        # Place navigation buttons
        self.clippr_logo.place(x=80, y=20)
        self.username_entry.place(x=200, y=170, width=150, height=25)
        self.password_entry.place(x=200, y=200, width=150, height=25)
        self.create_account_button.place(x=156, y=240)

    def get_details(self):

        if self.username_entry.get() != "" and self.username_entry.get() != "Username" and self.password_entry.get() != "" and self.password_entry.get() != "Password":
            username = self.username_entry.get()
            password = self.password_entry.get()
            return username, password

        else:
            self.error_label.place(x=114, y=280)
            self.error_label.config(text="Please enter a username and password")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))
            return None, None

    def sign_in(self):

        username, password = self.get_details()
        self.access = self.controller.sign_in(username, password)

        if self.access:
            self.destroy()
        else:
            self.error_label.place(x=144, y=280)
            self.error_label.config(text="Incorrect username or password")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))


    def open_signup(self):
        if self.signup is None:
            self.signup = signupGUI(self, self.controller)
            self.signup.username_entry.bind("<Destroy>", lambda x: self.allow_signup())


    def allow_signup(self):
        self.signup = None