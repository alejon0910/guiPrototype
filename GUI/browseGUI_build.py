import tkinter as tk
from GUI.scrollable_frame import VerticalScrolledFrame
from GUI.track_build import TrackBuild
from GUI.playlist_build import PlaylistBuild, CreatePlaylistWindow
from GUI.uploadGUI_build import uploadGUI
import tkinter.ttk as ttk
from PIL import ImageTk

class browserGUI(tk.Tk):

    def __init__(self, controller):
        super().__init__()

        self.title("clippr")
        self.iconbitmap(r"GUI\images\icon.ico")
        self.config(background="white")
        self.geometry("650x850")
        self.resizable(False, False)
        self.upload = None
        self.playlist_creator = None
        self.signed_out = False
        self.controller = controller

        self.icon_photos = {"clippr": tk.PhotoImage(file=r"GUI/images/clippr2.png"),
                            "home": tk.PhotoImage(file=r"GUI/images/home.png"),
                            "sounds": tk.PhotoImage(file=r"GUI/images/sounds.png"),
                            "liked": tk.PhotoImage(file=r"GUI/images/liked.png"),
                            "search": tk.PhotoImage(file=r"GUI/images/search.png"),
                            "playlists": tk.PhotoImage(file=r"GUI/images/mixes.png"),
                            "upload": tk.PhotoImage(file=r"GUI/images/upload.png"),
                            "profile": tk.PhotoImage(file=r"GUI/images/profile.png"),
                            "sign out": tk.PhotoImage(file=r"GUI/images/signout.png"),
                            "home_title": tk.PhotoImage(file=r"GUI/images/bighomeicon.png"),
                            "sounds_title": tk.PhotoImage(file=r"GUI/images/bigsoundsicon.png"),
                            "liked_title": tk.PhotoImage(file=r"GUI/images/biglikedicon.png"),
                            "playlists_title": tk.PhotoImage(file=r"GUI/images/bigplaylistsicon.png"),
                            "plus": tk.PhotoImage(file=r"GUI/images/plus.png"),
                            "blank": tk.PhotoImage()
                            }

        self.init_build()


    def init_build(self):
        # Tabs
        self.nav_tab = tk.Frame(self, width=110, height=850, bd=0, highlightthickness=0, background="#1c1c1c")
        self.browse_tab = VerticalScrolledFrame(self, width=482, height=10000, background="white")
        self.top_tab = tk.Frame(self, width=622, height=100, background="white")

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
                                       borderwidth=0, highlightthickness=0, cursor="hand2", command=self.open_search)
        self.playlists_button = tk.Button(self, image=self.icon_photos["playlists"], activebackground="#1c1c1c",
                                       borderwidth=0, highlightthickness=0, cursor="hand2", command=self.browse_playlists)
        self.upload_button = tk.Button(self, image=self.icon_photos["upload"], activebackground="#1c1c1c",
                                       borderwidth=0, highlightthickness=0, command=lambda: self.open_upload(),
                                       cursor="hand2")
        self.profile_button = tk.Button(self, image=self.icon_photos["profile"], activebackground="#1c1c1c",
                                        borderwidth=0,
                                        highlightthickness=0, cursor="hand2")
        self.signout_button = tk.Button(self, image=self.icon_photos["sign out"], activebackground="#1c1c1c",
                                        borderwidth=0, highlightthickness=0, cursor="hand2", command=self.sign_out)

        # Place tabs
        self.nav_tab.place(x=0, y=0)
        self.browse_tab.pack(side=tk.RIGHT)

        # Place navigation buttons
        self.clippr_icon.place(x=15, y=17)
        self.home_button.place(x=12, y=69)
        self.sounds_button.place(x=13, y=96)
        self.liked_button.place(x=11, y=130)
        self.search_button.place(x=13, y=158)
        self.playlists_button.place(x=13, y=186)
        self.upload_button.place(x=11, y=759)
        self.profile_button.place(x=13, y=786)
        self.signout_button.place(x=13, y=813)

        self.browse_home()

    def browse_home(self):

        self.top_tab.destroy()
        self.browse_tab.destroy()
        self.browse_tab = VerticalScrolledFrame(self, width=522, height=10000, background="white")
        self.browse_tab.pack(side=tk.RIGHT)

        self.title_label = tk.Label(self.browse_tab, image=self.icon_photos["home_title"], font=("SoleilBk", 23),
                                    bg="white", borderwidth=0, highlightthickness=0)
        self.title_label.grid(column=0, row=0, sticky="w", padx=(10, 0), pady=20, columnspan=99)

        self.username_label = tk.Label(self.browse_tab, text=self.controller.current_username, bg="white", fg="#1c1c1c",
                                       font=("SoleilXb", 15), anchor="e", bd=0, padx=0)
        self.username_label.grid(column=4, row=0, sticky="e", padx=15, pady=(26, 20), columnspan=99)

        for i in self.controller.fetch_home_results():
            self.new_track = TrackBuild(i, self.controller, None)
            self.new_track.build(self.browse_tab, ((5*i)-4))

    def browse_sounds(self):

        self.top_tab.destroy()
        self.browse_tab.destroy()
        self.browse_tab = VerticalScrolledFrame(self, width=522, height=10000, background="white")
        self.browse_tab.pack(side=tk.RIGHT)

        self.title_label = tk.Label(self.browse_tab, image=self.icon_photos["sounds_title"], font=("SoleilBk", 23),
                                    bg="white", borderwidth=0, highlightthickness=0)
        self.title_label.grid(column=0, row=0, sticky="w", padx=(10, 0), pady=20, columnspan=99)

        for i in self.controller.fetch_sounds_results():
            self.new_track = TrackBuild(i, self.controller, None)
            self.new_track.build(self.browse_tab, ((5 * i) - 4))

    def browse_liked(self):

        self.top_tab.destroy()
        self.browse_tab.destroy()
        self.browse_tab = VerticalScrolledFrame(self, width=522, height=10000, background="white")
        self.browse_tab.pack(side=tk.RIGHT)

        self.title_label = tk.Label(self.browse_tab, image=self.icon_photos["liked_title"], font=("SoleilBk", 23),
                                    bg="white", borderwidth=0, highlightthickness=0)
        self.title_label.grid(column=0, row=0, sticky="w", padx=(10, 0), pady=20, columnspan=99)

        for i in self.controller.fetch_liked_results():
            self.new_track = TrackBuild(i, self.controller, None)
            self.new_track.build(self.browse_tab, ((5 * i) - 3))

    def open_search(self):

        self.top_tab.destroy()
        self.browse_tab.destroy()

        self.top_tab = tk.Frame(self, width=622, height=100, background="white")
        self.browse_tab = VerticalScrolledFrame(self, width=522, height=10000, background="white")

        self.top_tab.pack(side=tk.TOP, padx=(76, 0))
        self.browse_tab.pack(side=tk.RIGHT)

        self.search_entry = tk.Entry(self.top_tab, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                    relief="flat", fg="#b0b0b0", font=("SoleilLt-Italic", 20), width=27)
        self.genre_dropdown = ttk.Combobox(self.top_tab, state="readonly", values=self.controller.genre_options, width=18,
                                           font=("SoleilLt-Italic", 8))
        self.mood_dropdown = ttk.Combobox(self.top_tab, state="readonly", values=self.controller.mood_options, width=18,
                                          font=("SoleilLt-Italic", 8))
        self.instrument_dropdown = ttk.Combobox(self.top_tab, state="readonly", values=self.controller.instrument_options, width=18,
                                                font=("SoleilLt-Italic", 8))

        self.search_entry.grid(column=0, row=0, sticky="w", padx=(20, 0), pady=(20,10), columnspan=99)
        self.genre_dropdown.grid(column=0, row=1, sticky="w", padx=(20, 0), pady=10)
        self.mood_dropdown.grid(column=1, row=1, sticky="w", padx=(15, 0), pady=10)
        self.instrument_dropdown.grid(column=2, row=1, sticky="w", padx=(15, 0), pady=10)

        self.search_entry.insert(0, "Search")
        self.search_entry.bind("<Button-1>", lambda x: [self.search_clicked(), self.search_entry.config(fg="black")])
        self.search_entry.bind("<Return>", lambda x: [self.retrieve_search()])

    def retrieve_search(self):

        self.search_term = self.search_entry.get().lower()
        self.get_dropdown_options()
        self.refresh_results()

        self.track_list = self.controller.fetch_searched_results(self.search_term, self.genre_term, self.mood_term, self.instrument_term)

        for i in self.track_list:
            self.new_track = TrackBuild(i, self.controller, None)
            self.new_track.build(self.browse_tab, ((5 * i) - 3))

    def get_dropdown_options(self):

        if len(self.genre_dropdown.get()) != 0:
            self.genre_term = (self.genre_dropdown.get(),'')
        else:
            self.genre_term = tuple(self.controller.genre_options)

        if len(self.mood_dropdown.get()) != 0:
            self.mood_term = (self.mood_dropdown.get(),'')
        else:
            self.mood_term = tuple(self.controller.mood_options)

        if len(self.instrument_dropdown.get()) != 0:
            self.instrument_term = (self.instrument_dropdown.get(),'')
        else:
            self.instrument_term = tuple(self.controller.instrument_options)

    def browse_playlists(self):
        self.top_tab.destroy()
        self.browse_tab.destroy()
        self.browse_tab = VerticalScrolledFrame(self, width=522, height=10000, background="white")
        self.browse_tab.pack(side=tk.RIGHT)

        self.title_label = tk.Label(self.browse_tab, image=self.icon_photos["playlists_title"], font=("SoleilBk", 23),
                                    bg="white", borderwidth=0, highlightthickness=0)
        self.new_playlist_button = tk.Button(self.browse_tab, image=self.icon_photos["plus"], highlightthickness=0,
                                             borderwidth=0,
                                             command=lambda: [self.open_create_playlist(), self.browse_playlists()])
        self.title_label.grid(column=0, row=0, sticky="w", padx=(10, 0), pady=20, columnspan=3)
        self.new_playlist_button.grid(column=4, row=0, sticky="w", padx=(10, 0), pady=20)


        for i in self.controller.fetch_playlists():
            self.new_playlist = PlaylistBuild(i, self.controller, self)
            self.new_playlist.build(self.browse_tab, ((5 * i) - 4))

    def open_playlist(self, playlist_id):
        self.top_tab.destroy()
        self.browse_tab.destroy()

        self.browse_tab = VerticalScrolledFrame(self, width=522, height=10000, background="white")
        self.browse_tab.pack(side=tk.RIGHT)

        for i in self.controller.fetch_playlist_tracks(playlist_id):
            self.new_track = TrackBuild(i, self.controller, playlist_id)
            self.new_track.build(self.browse_tab, ((5 * i) - 3))

    def open_upload(self):
        if self.upload is None:
            self.upload = uploadGUI(self, self.controller)
            self.upload.clipprlogo_label.bind("<Destroy>", lambda x: self.allow_upload())

    def open_create_playlist(self):
        if self.playlist_creator is None:
            self.playlist_creator = CreatePlaylistWindow(self, self.controller)
            self.playlist_creator.clipprlogo_label.bind("<Destroy>", lambda x: [self.allow_playlist_create(), self.browse_playlists()])

    def allow_upload(self):
        self.upload = None

    def allow_playlist_create(self):
        self.playlist_creator = None

    def sign_out(self):

        self.destroy()
        self.signed_out = True

    def search_clicked(self):

        if self.search_entry.get() == "Search":
            self.search_entry.delete(0, "end")
            self.search_entry.config(fg="black")

    def refresh_results(self):
        self.browse_tab.destroy()
        self.browse_tab = VerticalScrolledFrame(self, width=522, height=10000, background="white")
        self.browse_tab.pack(side=tk.RIGHT)