import tkinter as tk

class signupGUI(tk.Toplevel):

    def __init__(self, master, controller):
        super(signupGUI, self).__init__(master)
        self.transient(master)

        # This code sets up the window
        self.iconbitmap(r"GUI\images\icon.ico")
        self.config(background="white")
        self.geometry("500x280")
        self.resizable(False, False)
        self.controller = controller

        self.build()

    # This function creates, binds and places the window's Tkinter widgets
    def build(self):

        self.clippr_photo = tk.PhotoImage(file=r"GUI\images\clippruploadlogo.png")
        self.clippr_logo = tk.Label(self, image=self.clippr_photo, bg="white", borderwidth=0,
                                    highlightthickness=0)
        self.username_entry = tk.Entry(self, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                       relief="flat", fg="#b0b0b0", font=("Soleil-Book", 10))
        self.password_entry = tk.Entry(self, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                       relief="flat", fg="#b0b0b0", font=("Soleil-Book", 10))
        self.error_label = tk.Label(self, background="white", text="", highlightthickness=0, fg="#b0b0b0",
                                    font=("Soleil-Book", 10))
        self.signup_button = tk.Button(self, background="white", text="Sign Up",
                                       highlightthickness=0, fg="black", font=("SoleilXb", 10),
                                       relief="flat", command=lambda: [self.get_details(), self.sign_up()])

        self.username_entry.insert(0, "Username")
        self.password_entry.insert(0, "Password")
        self.clippr_logo.place(x=372, y=224)
        self.username_entry.place(x=176, y=98, width=150, height=25)
        self.password_entry.place(x=176, y=128, width=150, height=25)
        self.signup_button.place(x=225, y=168)

        self.username_entry.bind("<Button-1>", lambda x: [self.username_clicked(), self.username_entry.config(fg="black")])
        self.password_entry.bind("<Button-1>", lambda x: [self.password_clicked(), self.password_entry.config(fg="black", show='•')])
        self.bind("<Return>", lambda x: [self.get_details(), self.sign_up()])

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

    # This function retrieves the details entered by the user
    def get_details(self):

        if self.username_entry.get() != "" and self.username_entry.get() != "Username" and self.password_entry.get() != "" and self.password_entry.get() != "Password":
            username = self.username_entry.get()
            password = self.password_entry.get()
            return username, password

        else:
            self.error_label.place(x=131, y=200)
            self.error_label.config(text="Please enter a username and password")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))
            return None, None

    # This function attempts a sign-up, prints relevant errors from the database controller
    # if sign-up fails and destroys the window if it succeeds
    def sign_up(self):

        username, password = self.get_details()
        sign_up_attempt = self.controller.sign_up(username, password)

        if sign_up_attempt == "username in use":
            self.error_label.place(x=176, y=200)
            self.error_label.config(text="Username already exists")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))
        elif sign_up_attempt == "username bad length":
            self.error_label.place(x=118, y=200)
            self.error_label.config(text="Username must be between 4 and 16 characters")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))
        elif sign_up_attempt == "username no alpha":
            self.error_label.place(x=118, y=200)
            self.error_label.config(text="Username must contain letters")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))
        elif sign_up_attempt == "password too short":
            self.error_label.place(x=118, y=200)
            self.error_label.config(text="Password must be at least 4 characters")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))
        else:
            self.master.destroy()