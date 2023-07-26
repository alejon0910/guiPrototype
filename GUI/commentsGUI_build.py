import tkinter as tk
from GUI.scrollable_frame import VerticalScrolledFrame
import sqlite3
from GUI.comment_build import CommentBuild
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.models import User, Track, Comment, Like

engine = create_engine('sqlite:///database/clippr.sqlite3', echo=True)


class commentsGUI(tk.Toplevel):

    def __init__(self, track_id, user_id):

        super().__init__()
        self.config(background="white")
        self.geometry("500x300")
        self.iconbitmap(r"GUI\images\icon.ico")
        self.resizable(False, False)
        self.track_id = track_id
        self.conn = sqlite3.connect("database/clippr.sqlite3")
        self.cursor = self.conn.cursor()
        self.comment_adder = None
        self.user_id = user_id

        self.icon_photos = {"plus": tk.PhotoImage(file=r"GUI/images/plus.png"),
                            }

        self.build()

    def build(self):

        self.frame = VerticalScrolledFrame(self, width=500, height=10000, background="white")

        self.comments_title = tk.Label(self.frame, text="Comments", font=("SoleilXb", 23), bg="white", borderwidth=0, highlightthickness=0)
        self.add_comment_button = tk.Button(self.frame, image=self.icon_photos["plus"], highlightthickness=0, borderwidth=0, command=self.add_comment)
        self.nothing_yet_label = tk.Label(self.frame, text="nothing yet!", font=("SoleilLt", 16), bg="white", borderwidth=0, highlightthickness=0)

        self.frame.pack()
        self.comments_title.grid(row=0, column=0, sticky="w", padx=(20,10), pady=(10,20))
        self.add_comment_button.grid(row=0, column=1, sticky="w", padx=0, pady=(10, 20))


        get_comments_query = f"""SELECT id FROM comment WHERE track_id = ?"""

        self.cursor.execute(get_comments_query, (self.track_id,))
        self.comment_list = self.cursor.fetchall()
        index = 0

        if len(self.comment_list) != 0:
            for i in self.comment_list:
                index += 1
                self.new_track = CommentBuild(i[0])
                self.new_track.build(self.frame, ((4 * index) - 2))
        else:
            self.nothing_yet_label.grid(row=1, column=0, columnspan=10, padx=(173,0), pady=(46,0))

    def add_comment(self):
        if self.comment_adder is None:
            self.comment_adder = addCommentGUI(self.track_id, self.user_id)
            self.comment_adder.text_entry.bind("<Destroy>", self.allow_add_comment())

    def allow_add_comment(self):
        self.comment_adder = None


class addCommentGUI(tk.Toplevel):
    def __init__(self, track_id, user_id):

        super().__init__()
        self.config(background="white")
        self.geometry("400x100")
        self.iconbitmap(r"GUI\images\icon.ico")
        self.resizable(True, True)
        self.conn = sqlite3.connect("database/clippr.sqlite3")
        self.cursor = self.conn.cursor()
        self.track_id = track_id
        self.user_id = user_id

        self.icon_photos = {"plus": tk.PhotoImage(file=r"GUI/images/plus.png"),
                            }

        self.build()

    def build(self):

        self.text_entry = tk.Entry(self, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                       relief="flat", fg="#b0b0b0", font=("Soleil-Book", 15), state="normal", width=15)

        self.text_entry.insert(0, "Add comment")
        self.text_entry.bind("<Button-1>", lambda x: [self.entry_clicked()])
        self.bind("<Return>", lambda x: [self.post_comment()])
        self.text_entry.place(x=92, y=33)

    def entry_clicked(self):
        self.text_entry.config(fg="black")
        if self.text_entry.get() == "Add comment":
            self.text_entry.delete(0, "end")

    def post_comment(self):
        self.comment_text = self.text_entry.get()

        new_comment = Comment(user_id=self.user_id, track_id=self.track_id, text=self.comment_text)

        with Session(engine) as sess:
            sess.add(new_comment)
            sess.commit()

        self.destroy()