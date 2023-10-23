import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from PIL import Image, ImageTk

class uploadGUI(tk.Toplevel):

    def __init__(self, master, controller):
        super(uploadGUI, self).__init__(master)
        self.transient(master)

        self.config(background="white")
        self.geometry("500x250")
        self.iconbitmap(r"GUI\images\icon.ico")
        self.resizable(False, False)
        self.controller = controller

        self.icon_photos = {"clippr": tk.PhotoImage(file=r"GUI/images/clippruploadlogo.png"),
                            "empty_photo": tk.PhotoImage(file=r"GUI/images/emptyphoto.png"),
                            "select_file": tk.PhotoImage(file=r"GUI/images/select file.png"),
                            "post": tk.PhotoImage(file=r"GUI/images/post.png"),
                            "file_selected": tk.PhotoImage(file=r"GUI/images/file selected.png")}

        self.build()

    def build(self):

        self.clipprlogo_label = tk.Label(self, image=self.icon_photos["clippr"], borderwidth=0, highlightthickness=0)
        self.emptyphoto_button = tk.Button(self, image=self.icon_photos["empty_photo"], borderwidth=0, highlightthickness=0, cursor="hand2", command=self.select_cover)
        self.selectfile_button = tk.Button(self, image=self.icon_photos["select_file"], borderwidth=0, highlightthickness=0, cursor="hand2", command=self.select_track)
        self.post_button = tk.Button(self, image=self.icon_photos["post"], borderwidth=0, highlightthickness=0, cursor="hand2", command=self.post_track)
        self.title_entry = tk.Entry(self, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                       relief="flat", fg="#b0b0b0", font=("SoleilLt-Italic", 12), width=24)

        self.genre_dropdown = ttk.Combobox(self, state="readonly", values=self.controller.genre_options, width=8, font=("SoleilLt-Italic", 8))
        self.mood_dropdown = ttk.Combobox(self, state="readonly", values=self.controller.mood_options, width=8, font=("SoleilLt-Italic", 8))
        self.instrument_dropdown = ttk.Combobox(self, state="readonly", values=self.controller.instrument_options, width=8,font=("SoleilLt-Italic", 8))

        self.title_entry.insert(0, "Title (excl. filetype)")
        self.title_entry.bind("<Button-1>", lambda x: [self.title_clicked(), self.title_entry.config(fg="black")])

        self.genre_dropdown.bind("<<ComboboxSelected>>", lambda e: self.emptyphoto_button.focus())
        self.mood_dropdown.bind("<<ComboboxSelected>>", lambda e: self.emptyphoto_button.focus())
        self.instrument_dropdown.bind("<<ComboboxSelected>>", lambda e: self.emptyphoto_button.focus())

        self.clipprlogo_label.place(x=372, y=194)
        self.emptyphoto_button.place(x=308, y=18)
        self.title_entry.place(x=19, y=18)
        self.genre_dropdown.place(x=19, y=59)
        self.mood_dropdown.place(x=112, y=59)
        self.instrument_dropdown.place(x=205, y=59)
        self.selectfile_button.place(x=19, y=114)
        self.post_button.place(x=19, y=154)

        self.cover_file = None
        self.track_file = None

    def title_clicked(self):

        if self.title_entry.get() == "Title (excl. filetype)":
            self.title_entry.delete(0, "end")
            self.title_entry.config(fg="black")

    def select_track(self):

        self.track_file = filedialog.askopenfilename(filetypes=[("audio files", "*.mp3; *.wav")])
        self.selectfile_button.config(image=self.icon_photos["file_selected"])

    def select_cover(self):

        self.cover_file = filedialog.askopenfilename(filetypes=[("image files", "*.png; *.jpg; *.jpeg")])
        self.cover = Image.open(self.cover_file)
        self.cover = self.cover.resize((168, 168))
        self.cover = ImageTk.PhotoImage(self.cover)
        self.emptyphoto_button.config(image=self.cover)



    def post_track(self):
        if None not in [self.track_file, self.genre_dropdown.get(), self.mood_dropdown.get(), self.instrument_dropdown.get()]:
            self.controller.post_track(self.title_entry.get().lower(), self.genre_dropdown.get(), self.mood_dropdown.get(),
                                    self.instrument_dropdown.get(), self.track_file, self.cover_file)
            self.destroy()

    def allow_upload(self):
        self.master.uploading = False

