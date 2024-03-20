import tkinter as tk
from PIL import Image, ImageEnhance, ImageTk
import tkinter.ttk as ttk
from tkinter import filedialog

class PlaylistBuild:

    def __init__(self, playlist_id, controller, gui_master):
        """

        Parameters
        ----------
        playlist_id
        controller
        gui_master
        """
        self.controller = controller
        self.playlist_id = playlist_id

        self.playlist_name = self.controller.fetch_playlist_info(self.playlist_id)[0]
        self.playlist_cover = self.controller.fetch_playlist_info(self.playlist_id)[1]
        self.playlist_length = self.controller.fetch_playlist_info(self.playlist_id)[2]
        self.master = gui_master

        self.cover_image = Image.open(self.playlist_cover)
        self.cover_image = self.cover_image.resize((83, 83))
        self.cover_photoimage = ImageTk.PhotoImage(self.cover_image)

        self.pngs = {"play": tk.PhotoImage(file=r"GUI/images/play.png"),
                     "cross": tk.PhotoImage(file=r"GUI/images/cross.png")}

        self.brightener = ImageEnhance.Brightness(self.cover_image)

    # This function builds, using Tkinter widgets, a visual representation of a playlist in a given Tkinter frame and given row
    def build(self, frame, row):

        self.artist_label = tk.Label(frame, text=self.controller.current_username, font=("Soleil-Book", 12), bg="white")
        self.title_label = tk.Label(frame, text=self.playlist_name, font=("Soleil-Bold", 22), bg="white")
        self.tracks_length = tk.Label(frame, text=f"{self.playlist_length} songs", font=("Soleil-Book", 8), bg="white", fg="#606060", cursor="hand2")
        self.delete_button = tk.Button(frame, image=self.pngs["cross"], highlightthickness=0, borderwidth=0,
                                     command=self.delete_playlist)

        if len(self.playlist_name) > 16:
            self.title_label.config(text=f"{self.playlist_name[:16]}...")

        self.cover_canvas = tk.Canvas(frame, width=83, height=83, cursor="hand2", bd=0, relief="ridge",
                                      highlightthickness=0)
        self.cover_label = self.cover_canvas.create_image(41, 41, image=self.cover_photoimage)
        self.track_space = tk.Label(frame, text="", font=("Soleil-Bold", 12), bg="white")
        self.play = self.cover_canvas.create_image(41, 41, image=self.pngs["play"])

        self.artist_label.grid(column=0, row=row, sticky="w", columnspan=10, padx=11, pady=(10, 0))
        self.title_label.grid(column=0, row=row + 1, sticky="w", columnspan=5, padx=(10, 0))
        self.tracks_length.grid(column=0, row=row + 2, sticky="w", padx=(10, 0))
        self.delete_button.grid(column=1, row=row + 2, sticky="w", padx=(10, 100))

        self.cover_canvas.grid(column=5, row=row, rowspan=3, padx=(150, 15), pady=(10, 0))
        self.track_space.grid(column=0, row=row + 3, sticky="w", columnspan=10)

        self.cover_canvas.bind("<Enter>", lambda x: [self.darken()])
        self.cover_canvas.bind("<Leave>", lambda x: [self.lighten()])
        self.cover_canvas.bind("<Button-1>", lambda x: [self.open()])
        self.tracks_length.bind("<Button-1>", lambda x: [self.open()])

    # This function darkens the playlist's cover image (used when mouse hovers over it)
    def darken(self):
        self.cover_photoimage = ImageTk.PhotoImage(self.brightener.enhance(0.5))
        self.cover_canvas.itemconfig(self.cover_label, image=self.cover_photoimage)

    # This function lightens the track's cover image (used when mouse leaves cover image, reversing the effect of self.darken())
    def lighten(self):
        self.cover_photoimage = ImageTk.PhotoImage(self.cover_image)
        self.cover_canvas.itemconfig(self.cover_label, image=self.cover_photoimage)

    # This function prompts the main GUI object to display the tracks in the playlist
    def open(self):
        self.master.open_playlist(self.playlist_id)

    # This function deletes the playlist, using the controller object and prompting the main GUI to refresh the playlists page
    def delete_playlist(self):
        self.controller.delete_playlist(self.playlist_id)
        self.master.browse_playlists()


class AddToPlaylistWindow(tk.Toplevel):

    def __init__(self, track_id, controller):
        """

        Parameters
        ----------
        track_id
        controller
        """
        super().__init__()
        self.config(background="white")
        self.geometry("240x160")
        self.resizable(False, False)

        self.track_id = track_id
        self.controller = controller
        self.playlist_id_list = self.controller.fetch_playlists()
        self.playlist_name_list = self.controller.fetch_playlist_names()

        self.build()

    # This method builds the 'add to playlist' window using Tkinter widgets
    def build(self):
        self.add_label = tk.Label(self, text="add to playlist", font=("Soleil-Bold", 16), fg="#1c1c1c", bg="white")
        self.playlist_options = ttk.Combobox(self, values=self.playlist_name_list, state="readonly", font=("SoleilLt-Italic", 8))
        self.add_button = tk.Button(self, background="white", text="add", highlightthickness=0, fg="black", font=("SoleilXb", 10), command=self.add_track)

        self.add_label.grid(row=0, column=0, sticky="news", padx=42, pady=(20,5))
        self.playlist_options.grid(row=1, column=0, sticky="news", padx=42, pady=5)
        self.add_button.grid(row=2, column=0, sticky="news", padx=42, pady=5)

    # This method adds the track to the playlist specified in the dropdown box
    def add_track(self):
        chosen_playlist = self.playlist_id_list[self.playlist_name_list.index(self.playlist_options.get())]
        self.controller.add_track_to_playlist(self.track_id, chosen_playlist)
        self.destroy()

class CreatePlaylistWindow(tk.Toplevel):
    def __init__(self, master, controller):
        """

        Parameters
        ----------
        master
        controller
        """
        super(CreatePlaylistWindow, self).__init__(master)
        self.transient(master)

        self.config(background="white")
        self.geometry("500x250")
        self.iconbitmap(r"GUI\images\icon.ico")
        self.resizable(False, False)
        self.controller = controller

        self.icon_photos = {"clippr": tk.PhotoImage(file=r"GUI/images/clippruploadlogo.png"),
                            "empty_photo": tk.PhotoImage(file=r"GUI/images/emptyphoto.png"),
                            "create": tk.PhotoImage(file=r"GUI/images/create.png")}

        self.build()

    # This method builds the 'create playlist' window using Tkinter widgets
    def build(self):

        self.clipprlogo_label = tk.Label(self, image=self.icon_photos["clippr"], borderwidth=0, highlightthickness=0)
        self.emptyphoto_button = tk.Button(self, image=self.icon_photos["empty_photo"], borderwidth=0, highlightthickness=0, cursor="hand2", command=self.select_cover)
        self.create_button = tk.Button(self, image=self.icon_photos["create"], borderwidth=0, highlightthickness=0, cursor="hand2", command=self.add_playlist)
        self.title_entry = tk.Entry(self, background="#e0e0e0", highlightcolor="#b0b0b0", highlightthickness=1,
                                       relief="flat", fg="#b0b0b0", font=("SoleilLt-Italic", 12), width=28)

        self.title_entry.insert(0, "Title")
        self.title_entry.bind("<Button-1>", lambda x: [self.title_clicked(), self.title_entry.config(fg="black")])
        self.clipprlogo_label.place(x=372, y=194)
        self.emptyphoto_button.place(x=308, y=18)
        self.title_entry.place(x=19, y=100)
        self.create_button.place(x=19, y=154)

        self.cover_file = None
        self.track_file = None

    # This method clears the title entry's filler text when it is clicked
    def title_clicked(self):

        if self.title_entry.get() == "Title":
            self.title_entry.delete(0, "end")
            self.title_entry.config(fg="black")

    # This method, via a file dialog, allows the user to select the playlist's cover from their files
    def select_cover(self):

        self.cover_file = filedialog.askopenfilename(filetypes=[("image files", "*.png; *.jpg; *.jpeg")])
        self.cover = Image.open(self.cover_file)
        self.cover = self.cover.resize((168, 168))
        self.cover = ImageTk.PhotoImage(self.cover)
        self.emptyphoto_button.config(image=self.cover)

    # This method creates the playlist, using the controller object to add it to the database
    def add_playlist(self):
        if self.title_entry.get() is not None:
            self.controller.create_playlist(self.title_entry.get().lower(), self.cover_file)
            self.destroy()