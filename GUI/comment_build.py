import tkinter as tk
from PIL import Image, ImageEnhance, ImageTk
import time
import sqlite3
from just_playback import Playback
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.models import User, Track, Comment, Like
import sqlite3

engine = create_engine('sqlite:///database/clippr.sqlite3', echo=True)

class CommentBuild:

    def __init__(self, comment_id):

        self.conn = sqlite3.connect("database/clippr.sqlite3")
        self.cursor = self.conn.cursor()
        self.fetch_info(comment_id)

    def build(self, frame, row):

        self.commenter_label = tk.Label(frame, text=self.commenter, font=("SoleilSb", 12), bg="white")
        self.text_label = tk.Label(frame, text=self.comment_text, wraplength=400, font=("SoleilLt", 15), bg="white")

        self.comment_space = tk.Label(frame, text="", font=("Soleil-Bold", 12), bg="white")

        self.commenter_label.grid(column=0, row=row, sticky="w", padx=20, pady=0)
        self.text_label.grid(column=0, row=row + 1, sticky="w", padx=(20,0), pady=0, columnspan=10)
        self.comment_space.grid(column=0, row=row + 2, sticky="w", columnspan=10)

    def fetch_info(self, comment_id):
        get_info_query = """SELECT * FROM comment WHERE id = ?"""
        self.cursor.execute(get_info_query, (comment_id,))
        self.comment_info = self.cursor.fetchall()[0]
        self.comment_text = self.comment_info[1]

        get_commenter_query = f"""SELECT username FROM user WHERE id = {self.comment_info[2]}"""
        self.cursor.execute(get_commenter_query)
        self.commenter = self.cursor.fetchall()[0]

