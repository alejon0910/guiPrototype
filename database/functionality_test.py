from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import User, Track, Comment, Like
import sqlite3

engine = create_engine('sqlite:///clippr.sqlite3', echo=True)
conn = sqlite3.connect("../clippr.sqlite3")
cursor = conn.cursor()


def create_user(name):
    new_user = User(username=name)

    with Session(engine) as sess:
        sess.add(new_user)
        sess.commit()

def post_track(user_id, title, genre, mood, instrument, sound_filepath, cover_filepath=None):
    new_track = Track(title=title, artist=user_id, genre=genre, mood=mood, instrument=instrument, sound_filepath=sound_filepath, cover_filepath=cover_filepath)

    with Session(engine) as sess:
        sess.add(new_track)
        sess.commit()

def like_track(user_id, track_id):
    new_like = Like(user_id=user_id, track_id=track_id)

    with Session(engine) as sess:
        sess.add(new_like)
        sess.commit()


def post_comment(user_id, track_id, text):
    new_comment = Comment(user_id=user_id, track_id=track_id, text=text)

    with Session(engine) as sess:
        sess.add(new_comment)
        sess.commit()

def find_liked(user_id):

    find_liked_query = f"""
    SELECT track_id FROM like WHERE user_id = {user_id}
    """

    cursor.execute(find_liked_query)
    print(cursor.fetchall())

def count_likes(track_id):

    count_likes_query = f"""
    SELECT user_id FROM like WHERE track_id = {track_id}
    """

    cursor.execute(count_likes_query)
    print(len(cursor.fetchall()))

def object_from_id(track_id):

    get_info_query = f"""
    SELECT * FROM track WHERE id = {track_id}
    """

    cursor.execute(get_info_query)
    return cursor.fetchall()[0]

create_user("evernowbeats")
create_user("will.is.love")
create_user("emmalevin_tracks")
create_user("rahhbeats")
create_user("peachpit")
post_track(1, "suite.wav", "house", "chill", "synth", r"database/tracks/suite.wav", r"database/covers/cover1.png")
post_track(2, "crosswords.mp3", "dnb", "dark", "synth", r"database/tracks/lets get lifted.wav", r"database/covers/crosswords.png")
post_track(3, "victory_sfx.mp3", "sfx", "upbeat", "piano", r"database/tracks/wowbeautiful.wav")
post_track(4, "sunshine.wav", "hip-hop", "chill", "guitar", r"database/tracks/handinhand.wav", r"database/covers/davecover.png")
post_track(5, "tommys_party.wav", "rock", "chill", "guitar", r"database/tracks/tommys-party.mp3", r"database/covers/beingsonormal.png")
#like_track(1, 1)
#like_track(1, 3)
#like_track(1, 4)
#like_track(1, 5)
#like_track(2, 2)
#like_track(3, 3)
#like_track(3, 4)
#like_track(3, 5)
#like_track(4, 1)
#like_track(4, 2)
#like_track(4, 4)
#like_track(4, 5)
#like_track(5, 1)
#post_comment(1, 5, "this goes hard")
#post_comment(4, 2, "woahhh")
