import tkinter as tk

class signinGUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("clippr")
        self.iconbitmap(r"images\icon.ico")
        self.config(background="white")
        self.geometry("550x350")
        self.resizable(False, False)
        self.access = False

        self.test_usernames = ["alejon0910", "evernowbeats", "tobwil0910"]
        self.test_passwords = ["helloworld", "music", "@lexjonessmells"]

        self.clippr_photo = tk.PhotoImage(file=r"images\clipprblack.png")

        # Logo
        self.clippr_logo = tk.Label(self, image=self.clippr_photo, bg="white", borderwidth=0,
                                    highlightthickness=0)
        self.username_entry = tk.Entry(self, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                       relief="flat", fg="#b0b0b0", font=("Soleil-Book",10))
        self.password_entry = tk.Entry(self, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                       relief="flat", fg="#b0b0b0", font=("Soleil-Book",10))
        self.error_label = tk.Label(self, background="white", text="", highlightthickness=0, fg="black", font=("Soleil-Book",10))
        self.create_account_button = tk.Button(self, background="white", text="Create Account", highlightthickness=0, fg="black", font=("Soleil-Bold",10), relief="flat")

        self.username_entry.insert(0, "Username")
        self.password_entry.insert(0, "Password")

        self.username_entry.bind("<Button-1>", lambda x: [username_clicked(), self.username_entry.config(fg="black")])
        self.password_entry.bind("<Button-1>", lambda x: [password_clicked(), self.password_entry.config(fg="black", show='•')])

        self.bind("<Return>", lambda x: [self.get_details(), self.sign_in()])

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

        # Navigation buttons

        # "Welcome back" label

        # Place tabs

        # Place navigation buttons
        self.clippr_logo.place(x=80, y=20)
        self.username_entry.place(x=200, y=170, width=150, height=25)
        self.password_entry.place(x=200, y=200, width=150, height=25)
        self.create_account_button.place(x=220, y=240)

    def get_details(self):

        if len(self.username_entry.get()) != 0 and self.username_entry.get() != "Username" and len(self.password_entry.get()) != 0 and self.password_entry.get() != "Password":
            self.username = self.username_entry.get()
            self.password = self.password_entry.get()

        else:
            self.error_label.place(x=154, y=280)
            self.error_label.config(text="Please enter a username and password")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))

    def sign_in(self):

        if self.username in self.test_usernames and self.password == self.test_passwords[self.test_usernames.index(self.username)]:
            self.access = True
            self.destroy()
        elif self.username_entry.get() != "Username" and self.password_entry.get() != "Password":
            self.error_label.place(x=174, y=280)
            self.error_label.config(text="Incorrect username or password")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))
