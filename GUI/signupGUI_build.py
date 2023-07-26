import tkinter as tk
import sqlite3
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.models import User, Track, Comment, Like

class signupGUI(tk.Toplevel):

    def __init__(self, master):
        super(signupGUI, self).__init__(master)
        self.transient(master)

        self.iconbitmap(r"GUI\images\icon.ico")
        self.config(background="white")
        self.geometry("500x250")
        self.resizable(False, False)

        self.conn = sqlite3.connect("database/clippr.sqlite3")
        self.cursor = self.conn.cursor()
        self.engine = create_engine('sqlite:///database/clippr.sqlite3', echo=True)

        get_usernames_query = f"""SELECT username FROM user ORDER BY id"""

        self.cursor.execute(get_usernames_query)
        self.username_list = [username[0] for username in self.cursor.fetchall()]

        self.clippr_photo = tk.PhotoImage(file=r"GUI\images\clippruploadlogo.png")

        # Logo
        self.clippr_logo = tk.Label(self, image=self.clippr_photo, bg="white", borderwidth=0,
                                    highlightthickness=0)
        self.username_entry = tk.Entry(self, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                       relief="flat", fg="#b0b0b0", font=("Soleil-Book",10))
        self.password_entry = tk.Entry(self, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                       relief="flat", fg="#b0b0b0", font=("Soleil-Book",10))
        self.error_label = tk.Label(self, background="white", text="", highlightthickness=0, fg="black", font=("Soleil-Book",10))
        self.create_account_button = tk.Button(self, background="white", text="No sign in? Create Account", highlightthickness=0, fg="black", font=("Soleil-Bold",10), relief="flat")

        self.username_entry.insert(0, "Username")
        self.password_entry.insert(0, "Password")

        self.username_entry.bind("<Button-1>", lambda x: [username_clicked(), self.username_entry.config(fg="black")])
        self.password_entry.bind("<Button-1>", lambda x: [password_clicked(), self.password_entry.config(fg="black", show='•')])

        self.bind("<Return>", lambda x: [self.get_details(), self.sign_up()])

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
        self.clippr_logo.place(x=372, y=194)
        self.username_entry.place(x=176, y=98, width=150, height=25)
        self.password_entry.place(x=176, y=128, width=150, height=25)

    def get_details(self):

        if self.username_entry.get() != "" and self.username_entry.get() != "Username" and self.password_entry.get() != "" and self.password_entry.get() != "Password":
            self.username = self.username_entry.get()
            self.password = self.password_entry.get()
            self.hash_password()

        else:
            self.error_label.place(x=154, y=180)
            self.error_label.config(text="Please enter a username and password")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))

    def sign_up(self):

        if self.username in self.username_list:
            self.error_label.place(x=174, y=180)
            self.error_label.config(text="Username already exists")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))
        elif len(self.username) > 16:
            self.error_label.place(x=120, y=170)
            self.error_label.config(text="Username cannot be more than 16 characters")
            self.error_label.after(1500, lambda: self.error_label.config(text=""))
        else:
            new_user = User(username=self.username, password_hash=self.password)

            with Session(self.engine) as sess:
                sess.add(new_user)
                sess.commit()

            get_id_query = """SELECT id FROM user WHERE username = ?"""
            self.cursor.execute(get_id_query, (self.username,))
            self.master.id = self.cursor.fetchall()[0][0]
            self.master.access = True
            self.master.destroy()


    def hash_password(self):

        self.hasher = hashlib.sha256()
        self.hasher.update(bytes(self.password, 'utf-8'))
        self.password = self.hasher.hexdigest()
