import tkinter as tk
from PIL import Image, ImageEnhance, ImageTk
from just_playback import Playback
from GUI.commentsGUI_build import commentsGUI

class TrackBuild:

    track_instances = []

    def __init__(self, track_id, controller, playback_controller):

        self.controller = controller
        self.playback_controller = playback_controller
        self.track_id = track_id
        self.track_info = self.controller.fetch_track_info(self.track_id)

        TrackBuild.track_instances.append(self)

        self.viewer_id = self.controller.current_id
        self.artist = self.controller.fetch_username(self.track_info[0])
        self.title = self.track_info[1]
        self.genre = self.track_info[2]
        self.mood = self.track_info[3]
        self.instrument = self.track_info[4]
        self.sound_filepath = self.track_info[5]
        self.cover_filepath = self.track_info[6]

        self.cover_image = Image.open(self.cover_filepath)
        self.cover_image = self.cover_image.resize((83, 83))
        self.cover_photoimage = ImageTk.PhotoImage(self.cover_image)

        self.playpng = tk.PhotoImage(file=r"GUI/images/play.png")
        self.pausepng = tk.PhotoImage(file=r"GUI/images/pause.png")
        self.heartpng = tk.PhotoImage(file=r"GUI/images/heart.png")
        self.heartedpng = tk.PhotoImage(file=r"GUI/images/hearted.png")
        self.commentpng = tk.PhotoImage(file=r"GUI/images/comment.png")

        self.playing = False
        self.play_authorized = False
        self.comments = None
        self.playback = Playback()
        self.brightener = ImageEnhance.Brightness(self.cover_image)

    def build(self, frame, row):

        self.artist_label = tk.Label(frame, text=self.artist, font=("Soleil-Book", 12), bg="white")
        self.title_label = tk.Label(frame, text=self.title, font=("Soleil-Bold", 22), bg="white")

        if len(self.title) > 16:
            self.title_label.config(text=f"{self.title[:16]}...")

        self.tags = tk.Label(frame, text=f"{self.genre}    {self.mood}    {self.instrument}", font=("Soleil-Book", 8),
                             bg="white", fg="#606060")
        self.cover_canvas = tk.Canvas(frame, width=83, height=83, cursor="hand2", bd=0, relief="ridge",
                                      highlightthickness=0)
        self.cover_label = self.cover_canvas.create_image(41, 41, image=self.cover_photoimage)
        self.track_space = tk.Label(frame, text="", font=("Soleil-Bold", 12), bg="white")
        self.play_pause = self.cover_canvas.create_image(41, 41, image=self.playpng)
        self.like_button = tk.Button(frame, image=self.heartpng, highlightthickness=0, borderwidth=0,
                                     command=self.like_track)
        self.comment_button = tk.Button(frame, image=self.commentpng, highlightthickness=0, borderwidth=0,
                                        command=self.open_comments)

        self.artist_label.grid(column=0, row=row, sticky="w", columnspan=10, padx=11, pady=(10, 0))
        self.title_label.grid(column=0, row=row + 1, sticky="w", columnspan=5, padx=(10, 0))
        self.tags.grid(column=2, row=row + 2, sticky="w", padx=(10, 5))
        self.like_button.grid(column=0, row=row + 2, sticky="w", padx=(13, 5))
        self.comment_button.grid(column=1, row=row + 2, sticky="w", padx=(0, 5))

        self.cover_canvas.grid(column=4, row=row, rowspan=3, padx=(205, 15), pady=(10, 0))
        self.track_space.grid(column=0, row=row + 3, sticky="w", columnspan=10)

        self.cover_canvas.bind("<Enter>", lambda x: [self.darken()])
        self.cover_canvas.bind("<Leave>", lambda x: [self.lighten()])
        self.cover_canvas.bind("<Button-1>", lambda x: [self.do_play_pause()])
        self.playback_controller.change_flag.bind("<Configure>", self.shared_force_pause)

        self.liked = self.controller.config_like(self.track_id, self.viewer_id)
        self.config_like_button()

    def lighten(self):
        self.cover_photoimage = ImageTk.PhotoImage(self.cover_image)
        self.cover_canvas.itemconfig(self.cover_label, image=self.cover_photoimage)

    def darken(self):
        self.cover_photoimage = ImageTk.PhotoImage(self.brightener.enhance(0.5))
        self.cover_canvas.itemconfig(self.cover_label, image=self.cover_photoimage)

    def force_pause(self):
        if self.playback_controller.playing_id != self.track_id:
            self.cover_canvas.itemconfig(self.play_pause, image=self.playpng)
            self.playing = False
            self.cover_canvas.bind("<Leave>", lambda x: [self.lighten()])

    def do_play_pause(self):
        if self.playing:
            self.cover_canvas.itemconfig(self.play_pause, image=self.playpng)
            self.playing = False
            self.cover_canvas.bind("<Leave>", lambda x: [self.lighten()])

            self.playback_controller.pause()

        else:
            self.cover_canvas.itemconfig(self.play_pause, image=self.pausepng)
            self.playing = True
            self.cover_canvas.bind("<Leave>", lambda x: [self.darken()])

            self.playback_controller.play(self.sound_filepath, self.track_id)

    def like_track(self):

        self.controller.like_track(self.track_id, self.viewer_id)
        self.liked = self.controller.config_like(self.track_id, self.viewer_id)
        self.config_like_button()

    def config_like_button(self):
        if self.liked:
            self.like_button.config(image=self.heartedpng)
        else:
            self.like_button.config(image=self.heartpng)


    def open_comments(self):
        if self.comments is None:
            self.comments = commentsGUI(self.track_id, self.controller)
            self.comments.empty_label.bind("<Destroy>", lambda x: self.allow_comments())

    def allow_comments(self):
        self.comments = None

    def shared_force_pause(cls, event):
        for instance in cls.track_instances:
            instance.force_pause()