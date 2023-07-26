from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import User, Track, Comment, Like

users = [User(username="evernowbeats"),
           User(username="will.is.love"),
           User(username="emmalevin_tracks"),
           User(username="rahhbeats"),
           User(username="peachpit")]

tracks = [Track(title="suite.wav", artist=1),
         Track(title="crosswords.mp3", artist=2),
         Track(title="victory_sfx.mp3", artist=3),
         Track(title="sunshine.wav", artist=4),
         Track(title="tommys_party.mp3", artist=5)
         ]

users[0].liked_tracks.append(tracks[0])
users[0].liked_tracks.append(tracks[3])
users[1].liked_tracks.append(tracks[1])
users[2].liked_tracks.append(tracks[2])
users[3].liked_tracks.append(tracks[4])
users[4].liked_tracks.append(tracks[4])

# Connect to the activities database
engine = create_engine('sqlite:///clippr.sqlite3', echo=True)

# Create a session and add the people to the database
with Session(engine) as sess:
    sess.add_all(tracks)
    sess.commit()
