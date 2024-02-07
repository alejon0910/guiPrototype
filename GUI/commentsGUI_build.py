import tkinter as tk
from GUI.scrollable_frame import VerticalScrolledFrame
from GUI.comment_build import CommentBuild

class commentsGUI(tk.Toplevel):

    def __init__(self, track_id, controller):

        super().__init__()
        self.config(background="white")
        self.geometry("500x300")
        self.iconbitmap(r"GUI\images\icon.ico")
        self.resizable(False, False)
        self.track_id = track_id
        self.comment_adder = None
        self.controller = controller

        self.icon_photos = {"plus": tk.PhotoImage(file=r"GUI/images/plus.png"),
                            }

        self.build()

    def build(self):

        self.frame = VerticalScrolledFrame(self, width=500, height=10000, background="white")

        self.comments_title = tk.Label(self.frame, text="Comments", font=("SoleilXb", 23), bg="white", borderwidth=0, highlightthickness=0)
        self.add_comment_button = tk.Button(self.frame, image=self.icon_photos["plus"], highlightthickness=0, borderwidth=0, command=self.add_comment)
        self.nothing_yet_label = tk.Label(self.frame, text="nothing yet!", font=("SoleilLt", 16), bg="white", borderwidth=0, highlightthickness=0)
        self.empty_label = tk.Label(self)

        self.frame.pack()
        self.empty_label.pack(side=tk.BOTTOM)
        self.comments_title.grid(row=0, column=0, sticky="w", padx=(20,10), pady=(10,20))
        self.add_comment_button.grid(row=0, column=1, sticky="w", padx=0, pady=(10, 20))

        self.comment_list = self.controller.fetch_comments(self.track_id)

        if len(self.comment_list) != 0:
            for i in self.comment_list:
                self.new_track = CommentBuild(i, self.controller)
                self.new_track.build(self.frame, ((4 * i) - 2))
        else:
            self.nothing_yet_label.grid(row=1, column=0, columnspan=10, padx=(173,0), pady=(46,0))

    def add_comment(self):
        if self.comment_adder is None:
            self.comment_adder = addCommentGUI(self.track_id, self.controller)
            self.comment_adder.bind("<Destroy>", lambda x: [self.allow_add_comment()])

    def allow_add_comment(self):
        self.refresh()
        self.comment_adder = None

    def refresh(self):
        self.empty_label.pack_forget()
        self.frame.destroy()
        self.build()

class addCommentGUI(tk.Toplevel):
    def __init__(self, track_id, controller):

        super().__init__()
        self.config(background="white")
        self.geometry("400x100")
        self.iconbitmap(r"GUI\images\icon.ico")
        self.resizable(False, False)
        self.track_id = track_id
        self.controller = controller

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
        self.controller.post_comment(self.track_id, self.comment_text)
        self.text_entry.destroy()
        self.destroy()