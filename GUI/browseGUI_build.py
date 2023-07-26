import tkinter as tk
from GUI.scrollable_frame import VerticalScrolledFrame
from GUI.track_build import TrackBuild
from GUI.uploadGUI_build import uploadGUI
import sqlite3
import random

class browserGUI(tk.Tk):

    def __init__(self, master, id):
        super().__init__()

        self.title("clippr")
        self.iconbitmap(r"GUI\images\icon.ico")
        self.config(background="white")
        self.geometry("650x850")
        self.resizable(False, False)
        self.upload = None
        self.current_id = id

        self.conn = sqlite3.connect("database/clippr.sqlite3")
        self.cursor = self.conn.cursor()

        self.get_username()

        self.icon_photos = {"clippr": tk.PhotoImage(file=r"GUI/images/clippr2.png"),
                            "home": tk.PhotoImage(file=r"GUI/images/home.png"),
                            "sounds": tk.PhotoImage(file=r"GUI/images/sounds.png"),
                            "liked": tk.PhotoImage(file=r"GUI/images/liked.png"),
                            "search": tk.PhotoImage(file=r"GUI/images/search.png"),
                            "upload": tk.PhotoImage(file=r"GUI/images/upload.png"),
                            "you": tk.PhotoImage(file=r"GUI/images/you.png"),
                            "home_title": tk.PhotoImage(file=r"GUI/images/bighomeicon.png"),
                            "sounds_title": tk.PhotoImage(file=r"GUI/images/bigsoundsicon.png"),
                            "liked_title": tk.PhotoImage(file=r"GUI/images/biglikedicon.png"),
                            "blank": tk.PhotoImage()
                            }

        # Tabs
        self.nav_tab = tk.Frame(self, width=110, height=850, bd=0, highlightthickness=0, background="#1c1c1c")
        self.browse_tab = VerticalScrolledFrame(self, width=482, height=10000, background="white")

        # Navigation buttons
        self.clippr_icon = tk.Label(self, image=self.icon_photos["clippr"], activebackground="#1c1c1c", borderwidth=0,
                                    highlightthickness=0)
        self.home_button = tk.Button(self, image=self.icon_photos["home"], activebackground="#1c1c1c", borderwidth=0,
                                     highlightthickness=0, cursor="hand2", command=self.browse_home)
        self.sounds_button = tk.Button(self, image=self.icon_photos["sounds"], activebackground="#1c1c1c",
                                       borderwidth=0, highlightthickness=0, command=self.browse_sounds, cursor="hand2")
        self.liked_button = tk.Button(self, image=self.icon_photos["liked"], activebackground="#1c1c1c", borderwidth=0,
                                      highlightthickness=0, cursor="hand2", command=self.browse_liked)
        self.search_button = tk.Button(self, image=self.icon_photos["search"], activebackground="#1c1c1c",
                                       borderwidth=0, highlightthickness=0, cursor="hand2")
        self.upload_button = tk.Button(self, image=self.icon_photos["upload"], activebackground="#1c1c1c",
                                       borderwidth=0, highlightthickness=0, command=lambda: self.open_upload(), cursor="hand2")
        self.you_button = tk.Button(self, image=self.icon_photos["you"], activebackground="#1c1c1c", borderwidth=0,
                                    highlightthickness=0, cursor="hand2")



        # Place tabs
        self.nav_tab.place(x=0, y=0)
        self.browse_tab.pack(side=tk.RIGHT)

        # Place navigation buttons
        self.clippr_icon.place(x=15, y=17)
        self.home_button.place(x=12, y=69)
        self.sounds_button.place(x=13, y=96)
        self.liked_button.place(x=11, y=130)
        self.search_button.place(x=13, y=158)
        self.upload_button.place(x=11, y=769)
        self.you_button.place(x=13, y=796)

        self.browse_home()

    def browse_home(self):

        self.browse_tab.destroy()
        self.browse_tab = VerticalScrolledFrame(self, width=522, height=10000, background="white")
        self.browse_tab.pack(side=tk.RIGHT)

        self.title_label = tk.Label(self.browse_tab, image=self.icon_photos["home_title"], font=("SoleilBk", 23),
                                    bg="white", borderwidth=0, highlightthickness=0)
        self.title_label.grid(column=0, row=0, sticky="w", padx=(10, 0), pady=20, columnspan=99)

        self.username_label = tk.Label(self.browse_tab, text=self.current_username, bg="white", fg="#1c1c1c",
                                       font=("SoleilXb", 15), anchor="e", bd=0, padx=0)
        self.username_label.grid(column=4, row=0, sticky="e", padx=15, pady=(26,20), columnspan=99)


        get_home_tracks_query = f"""SELECT id FROM track"""

        self.cursor.execute(get_home_tracks_query)
        self.track_list = self.cursor.fetchall()
        self.display_list = self.generate_random_set()

        index = 0

        for i in self.display_list:
            index += 1
            self.new_track = TrackBuild(i, self.current_id)
            self.new_track.build(self.browse_tab, ((5 * index) - 4))

    def browse_sounds(self):

        self.browse_tab.destroy()
        self.browse_tab = VerticalScrolledFrame(self, width=522, height=10000, background="white")
        self.browse_tab.pack(side=tk.RIGHT)

        self.title_label = tk.Label(self.browse_tab, image=self.icon_photos["sounds_title"], font=("SoleilBk", 23),
                                    bg="white", borderwidth=0, highlightthickness=0)
        self.title_label.grid(column=0, row=0, sticky="w", padx=(10, 0), pady=20, columnspan=99)

        get_sounds_query = f"""SELECT id FROM track WHERE artist = ? ORDER BY id"""

        self.cursor.execute(get_sounds_query, (self.current_id,))
        self.track_list = self.cursor.fetchall()

        for i in self.track_list:
            self.new_track = TrackBuild(i[0], self.current_id)
            self.new_track.build(self.browse_tab, ((5*i[0])-4))

    def browse_liked(self):

        self.browse_tab.destroy()
        self.browse_tab = VerticalScrolledFrame(self, width=522, height=10000, background="white")
        self.browse_tab.pack(side=tk.RIGHT)

        self.title_label = tk.Label(self.browse_tab, image=self.icon_photos["liked_title"], font=("SoleilBk", 23),
                                    bg="white", borderwidth=0, highlightthickness=0)
        self.title_label.grid(column=0, row=0, sticky="w", padx=(10, 0), pady=20, columnspan=99)

        get_liked_query = f"""SELECT id FROM track WHERE id IN (SELECT track_id FROM like WHERE user_id = ?)"""

        self.cursor.execute(get_liked_query, (self.current_id,))
        self. track_list = self.cursor.fetchall()

        for i in self.track_list:
            self.new_track = TrackBuild(i[0], self.current_id)
            self.new_track.build(self.browse_tab, ((5*i[0])-4))

    def open_upload(self):
        if self.upload is None:
            self.upload = uploadGUI(self, self.current_id)
            self.upload.clipprlogo_label.bind("<Destroy>", lambda x: self.allow_upload())

    def get_username(self):

        get_username_query = f"""SELECT username FROM user WHERE id = ?"""
        self.cursor.execute(get_username_query, (self.current_id,))
        self.current_username = self.cursor.fetchall()[0][0]

    def allow_upload(self):
        self.upload = None

    def generate_random_set(self):

        self.row_count = len(self.track_list)

        randint_list = [random.randint(1, self.row_count) for x in range(10)]
        randint_set = set(randint_list)

        while len(randint_list) != len(randint_set):
            randint_list = [random.randint(1, self.row_count) for x in range(10)]
            randint_set = set(randint_list)

        return randint_list
