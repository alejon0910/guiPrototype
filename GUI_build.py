import tkinter as tk
import tkinter.ttk as ttk
from scrollable_frame import VerticalScrolledFrame
from track_build import TrackBuild
import time


class GUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("clippr")
        self.iconbitmap(r"images\icon.ico")
        self.config(background="white")
        self.geometry("550x650")
        self.resizable(False, False)
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("TProgressbar", thickness=3, troughcolor="white", background="black")

        self.icon_photos = {"clippr": tk.PhotoImage(file=r"images\clippr2.png"),
                            "home": tk.PhotoImage(file=r"images\home.png"),
                            "sounds": tk.PhotoImage(file=r"images\sounds.png"),
                            "liked": tk.PhotoImage(file=r"images\liked.png"),
                            "search": tk.PhotoImage(file=r"images\search.png"),
                            "upload": tk.PhotoImage(file=r"images\upload.png"),
                            "you": tk.PhotoImage(file=r"images\you.png")}

        # Tabs
        self.nav_tab = tk.Frame(self, width=110, height=650, bd=0, highlightthickness=0, background="#1c1c1c")
        self.browse_tab = VerticalScrolledFrame(self, width=422, height=10000, background="white")

        # Navigation buttons
        self.clippr_icon = tk.Label(self, image=self.icon_photos["clippr"], activebackground="#1c1c1c", borderwidth=0,
                                    highlightthickness=0)
        self.home_button = tk.Button(self, image=self.icon_photos["home"], activebackground="#1c1c1c", borderwidth=0,
                                     highlightthickness=0)
        self.sounds_button = tk.Button(self, image=self.icon_photos["sounds"], activebackground="#1c1c1c",
                                       borderwidth=0, highlightthickness=0)
        self.liked_button = tk.Button(self, image=self.icon_photos["liked"], activebackground="#1c1c1c", borderwidth=0,
                                      highlightthickness=0)
        self.search_button = tk.Button(self, image=self.icon_photos["search"], activebackground="#1c1c1c",
                                       borderwidth=0, highlightthickness=0)
        self.upload_button = tk.Button(self, image=self.icon_photos["upload"], activebackground="#1c1c1c",
                                       borderwidth=0, highlightthickness=0, command=lambda x: self.add())
        self.you_button = tk.Button(self, image=self.icon_photos["you"], activebackground="#1c1c1c", borderwidth=0,
                                    highlightthickness=0)

        # "Welcome back" label
        self.welcome_label = tk.Label(self.browse_tab, text="Welcome back, Alex", font=("SoleilXb-Italic", 29),
                                      bg="white", borderwidth=0, highlightthickness=0)

        # Place tabs
        self.nav_tab.place(x=0, y=0)
        self.browse_tab.pack(side=tk.RIGHT)

        # Place navigation buttons
        self.clippr_icon.place(x=15, y=17)
        self.home_button.place(x=12, y=69)
        self.sounds_button.place(x=13, y=96)
        self.liked_button.place(x=11, y=130)
        self.search_button.place(x=13, y=158)
        self.upload_button.place(x=11, y=569)
        self.you_button.place(x=13, y=596)
        self.welcome_label.grid(column=0, row=0, sticky="w", padx=10, pady=20, columnspan=10)

        self.tracks_test()

    def tracks_test(self):
        self.test_cover = r"images\testcover2.png"

        self.track1 = TrackBuild("evernowbeats", "suite.wav", "house", "chill", "synth", self.test_cover)
        self.track1.build(self.browse_tab, 1)

        self.track2 = TrackBuild("will.is.love", "crosswords.mp3", "dnb", "dark", "synth", self.test_cover)
        self.track2.build(self.browse_tab, 6)

        self.track3 = TrackBuild("emmalevin_tracks", "victory_sfx.mp3", "sfx", "upbeat", "piano", self.test_cover)
        self.track3.build(self.browse_tab, 11)

        self.track4 = TrackBuild("rahhbeats", "sunshine.wav", "hip-hop", "chill", "guitar", self.test_cover)
        self.track4.build(self.browse_tab, 16)

        self.track5 = TrackBuild("evernowbeats", "suite.wav", "house", "chill", "synth", self.test_cover)
        self.track5.build(self.browse_tab, 21)

        self.track6 = TrackBuild("will.is.love", "crosswords.mp3", "dnb", "dark", "synth", self.test_cover)
        self.track6.build(self.browse_tab, 26)

        self.track7 = TrackBuild("emmalevin_tracks", "victory_sfx.mp3", "sfx", "upbeat", "piano", self.test_cover)
        self.track7.build(self.browse_tab, 31)

        self.track8 = TrackBuild("rahhbeats", "sunshine.wav", "hip-hop", "chill", "guitar", self.test_cover)
        self.track8.build(self.browse_tab, 36)


if __name__ == "__main__":
    menu = GUI()
    menu.mainloop()
