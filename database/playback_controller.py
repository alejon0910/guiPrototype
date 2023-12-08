import tkinter as tk
from just_playback import Playback
import random

class PlaybackController(tk.Tk):

    def __init__(self):
        super().__init__()
        self.playback = Playback()
        self.playing_id = None
        self.change_flag = tk.Label(self)
        self.change_flag.pack()
        self.width = 0
        self.iconify()

    def play(self, filepath, playing_id):
        self.playback.load_file(filepath)
        self.playback.play()
        self.playing_id = playing_id
        self.width += 1
        self.change_flag.config(width=self.width)

    def pause(self):
        self.playback.pause()
