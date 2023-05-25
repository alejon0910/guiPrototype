import tkinter as tk
from PIL import Image, ImageEnhance, ImageTk
import time

class TrackBuild:

    def __init__(self, artist, title, genre, mood, instrument, cover):
        self.artist = artist
        self.title = title
        self.genre = genre
        self.mood = mood
        self.instrument = instrument
        self.progress_var = tk.DoubleVar()
        self.cover_image = Image.open(cover)
        self.cover_photoimage = ImageTk.PhotoImage(self.cover_image)
        self.playpng = tk.PhotoImage(file=r"images\play.png")
        self.pausepng = tk.PhotoImage(file=r"images\pause.png")
        self.playing = False
        self.brightener = ImageEnhance.Brightness(self.cover_image)

    def build(self, frame, row):

        self.artist_label = tk.Label(frame, text=self.artist, font=("SoleilSb",12), bg="white")
        self.title_label = tk.Label(frame, text=self.title, font=("Soleil-Bold", 22), bg="white")
        self.tags = tk.Label(frame, text=f"{self.genre}    {self.mood}    {self.instrument}", font=("SoleilBk", 8), bg="white", fg="#606060")
        self.cover_canvas = tk.Canvas(frame, width=83, height=83, cursor="hand2", bd=0, relief="ridge", highlightthickness=0)
        self.cover_label = self.cover_canvas.create_image(41, 41, image=self.cover_photoimage)
        self.track_space = tk.Label(frame, text="", font=("Soleil-Bold", 12), bg="white")
        self.play_pause = self.cover_canvas.create_image(41, 41, image=self.playpng)
        self.artist_label.grid(column=0, row=row, sticky="w", columnspan=10, padx=11, pady=(10,0))
        self.title_label.grid(column=0, row=row+1, sticky="w", columnspan=10, padx=10)
        self.tags.grid(column=0, row=row+2, sticky="w", padx=(10,5))


        self.cover_canvas.grid(column=4, row=row, rowspan=3, padx=(155,0), pady=(10,0))
        self.track_space.grid(column=0, row=row+3, sticky="w", columnspan=10)

        self.cover_canvas.bind("<Enter>", lambda x: [self.darken()])
        self.cover_canvas.bind("<Leave>", lambda x: [self.lighten()])
        self.cover_canvas.bind("<Button-1>", lambda x: [self.do_play_pause()])

    def lighten(self):
        self.cover_photoimage = ImageTk.PhotoImage(self.cover_image)
        self.cover_canvas.itemconfig(self.cover_label, image=self.cover_photoimage)

    def darken(self):
        self.cover_photoimage = ImageTk.PhotoImage(self.brightener.enhance(0.5))
        self.cover_canvas.itemconfig(self.cover_label, image=self.cover_photoimage)

    def do_play_pause(self):

        if self.playing:
            self.cover_canvas.itemconfig(self.play_pause, image=self.playpng)
            self.playing = False
            self.cover_canvas.bind("<Leave>", lambda x: [self.lighten()])
        else:
            self.cover_canvas.itemconfig(self.play_pause, image=self.pausepng)
            self.playing = True
            self.cover_canvas.bind("<Leave>", lambda x: [self.darken()])
