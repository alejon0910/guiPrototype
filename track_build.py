import tkinter as tk
from PIL import Image, ImageEnhance, ImageTk

class TrackBuild:

    def __init__(self, artist, title, genre, mood, instrument, cover):
        self.artist = artist
        self.title = title
        self.genre = genre
        self.mood = mood
        self.instrument = instrument
        self.cover_image = Image.open(cover)
        self.cover_photoimage = ImageTk.PhotoImage(self.cover_image)
        self.playpng = tk.PhotoImage(file=r"images\play.png")

        self.brightener = ImageEnhance.Brightness(self.cover_image)

    def build(self, frame, row):

        self.artist_label = tk.Label(frame, text=self.artist, font=("SoleilSb",12), bg="white")
        self.title_label = tk.Label(frame, text=self.title, font=("Soleil-Bold", 22), bg="white")
        self.tags = tk.Label(frame, text=f"{self.genre}    {self.mood}    {self.instrument}", font=("SoleilBk", 8), bg="white", fg="#606060")
        self.cover_label = tk.Label(frame, image=self.cover_photoimage, cursor="hand2")
        self.track_space = tk.Label(frame, text="", font=("Soleil-Bold", 22), bg="white")

        self.artist_label.grid(column=0, row=row, sticky="w", columnspan=10, padx=11, pady=(10,0))
        self.title_label.grid(column=0, row=row+1, sticky="w", columnspan=10, padx=10)
        self.tags.grid(column=0, row=row+2, sticky="w", padx=(10,5))

        self.cover_label.grid(column=4, row=row, rowspan=3, padx=(155,0), pady=(10,0))
        self.track_space.grid(column=0, row=row+3, sticky="w", columnspan=10)

        self.cover_label.bind("<Enter>", lambda x: [self.hover_darken()])
        self.cover_label.bind("<Leave>", lambda x: [self.hover_lighten()])

    def hover_lighten(self):
        self.cover_photoimage = ImageTk.PhotoImage(self.cover_image)
        self.cover_label.config(image=self.cover_photoimage)

    def hover_darken(self):
        self.cover_photoimage = ImageTk.PhotoImage(self.brightener.enhance(0.5))
        self.cover_label.config(image=self.cover_photoimage)