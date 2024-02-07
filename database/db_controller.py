from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import Session
from database.models import User, Track, Comment, Like, Playlist, Playlist_Track
import random
import hashlib
import os
import shutil
from statistics import mean, stdev



class Controller:

    def __init__(self):
        self.current_id = None
        self.engine = create_engine('sqlite:///database/clippr.sqlite', echo=True)

        self.genre_options = ["pop",
                              "hip-hop",
                              "edm",
                              "rock",
                              "alternative",
                              "cinematic",
                              "classical"]

        self.mood_options = ["chill",
                             "hype",
                             "sad",
                             "dark",
                             "upbeat",
                             "epic"]

        self.instrument_options = ["piano",
                                   "drums",
                                   "bass",
                                   "synth",
                                   "guitar",
                                   "strings",
                                   "vocal"]

    def fetch_home_results(self):

        track_list = []
        boosted_tags = self.find_preference_outliers()



        random_set = self.generate_random_set()

        with Session(self.engine) as session:

            if len(boosted_tags[0]) != 0:
                track_list.append(random.choice([track_id[0] for track_id in session.query(Track.id).filter(Track.genre.in_(boosted_tags[0]))]))
            if len(boosted_tags[1]) != 0:
                track_list.append(random.choice([track_id[0] for track_id in session.query(Track.id).filter(Track.mood.in_(boosted_tags[1]))]))
            if len(boosted_tags[2]) != 0:
                track_list.append(random.choice([track_id[0] for track_id in session.query(Track.id).filter(Track.instrument.in_(boosted_tags[2]))]))
            track_list += random_set
            track_list = list(dict.fromkeys(track_list))
            print(track_list)
        return track_list

    def fetch_sounds_results(self):

        with Session(self.engine) as session:
            track_list = [track_id[0] for track_id in session.query(Track.id).filter_by(artist=self.current_id)]

        return track_list

    def fetch_liked_results(self):

        with Session(self.engine) as session:
            liked_subquery = session.query(Like.track_id).filter_by(user_id=self.current_id).subquery()
            track_list = [track_id[0] for track_id in session.query(Track.id).filter(Track.id.in_(liked_subquery))]

        return track_list

    def fetch_searched_results(self, search_term, genre_term, mood_term, instrument_term):

        with Session(self.engine) as session:

            query = (select(Track.id).where(or_(Track.title.ilike(f"%{search_term}%"),
                    Track.artist.in_(select(User.id).where(User.username.ilike(f"%{search_term}%")))
                ), Track.genre.in_(genre_term), Track.mood.in_(mood_term), Track.instrument.in_(instrument_term)))

            track_list = [row[0] for row in session.execute(query)]
            return track_list

    def fetch_playlists(self):
        with Session(self.engine) as session:
            playlist_list = [playlist_id[0] for playlist_id in session.query(Playlist.id).filter_by(user_id=self.current_id)]

        return playlist_list

    def fetch_playlist_names(self):
        with Session(self.engine) as session:
            playlist_list = [playlist_name[0] for playlist_name in session.query(Playlist.name).filter_by(user_id=self.current_id)]

        return playlist_list

    def add_track_to_playlist(self, track_id, playlist_id):
        with Session(self.engine) as session:
            new_pt = Playlist_Track(track_id=track_id, playlist_id=playlist_id)
            session.add(new_pt)
            session.commit()

    def remove_track_from_playlist(self, track_id, playlist_id):
        with Session(self.engine) as session:
            session.query(Playlist_Track).filter_by(track_id=track_id, playlist_id=playlist_id).delete()
            session.commit()

    def create_playlist(self, name, cover_file):

        cover_file = r"GUI\images\testcover2.png" if cover_file is None else cover_file

        shutil.copy(cover_file, r"database/covers")
        cover_file = r"database/covers/" + os.path.basename(cover_file)

        with Session(self.engine) as session:
            new_playlist = Playlist(name=name, user_id=self.current_id, cover_filepath=cover_file)
            session.add(new_playlist)
            session.commit()

    def delete_playlist(self, id):
        with Session(self.engine) as session:
            session.query(Playlist).filter_by(id=id).delete()
            session.commit()

    def fetch_playlist_info(self, id):
        with Session(self.engine) as session:
            playlist_object = [info for info in session.query(Playlist).filter_by(id=id)][0]
            playlist_info = [playlist_object.name, playlist_object.cover_filepath, len([track_id[0] for track_id in session.query(Playlist_Track.track_id).filter_by(playlist_id=id)])]
        return playlist_info

    def fetch_playlist_tracks(self, playlist_id):
        with Session(self.engine) as session:
            playlist_tracks = [track_id[0] for track_id in session.query(Playlist_Track.track_id).filter_by(playlist_id=playlist_id).order_by(Playlist_Track.id)]
        return playlist_tracks

    def generate_random_set(self):
        with Session(self.engine) as session:
            track_count = session.query(Track).count()
        return random.sample(range(1, track_count), 10)

    def sign_in(self, username, password):

        with Session(self.engine) as session:
            username_list = [username[0] for username in session.query(User.username).order_by(User.id)]
            password_list = [password[0] for password in session.query(User.password_hash).order_by(User.id)]

        password = self.hash_password(password)

        if username in username_list and password == password_list[username_list.index(username)]:
            with Session(self.engine) as session:
                self.current_id = [user_id for user_id in session.query(User.id).filter_by(username=username)][0][0]
                self.current_username = username
            return True
        else:
            return False

    def sign_up(self, username, password):

        with Session(self.engine) as session:
            if username in [name[0] for name in session.query(User.username)]:
                return "username in use"
            elif len(username) > 16:
                return "username too long"
            else:
                new_user = User(username=username, password_hash=self.hash_password(password))

                session.add(new_user)
                session.commit()

                self.current_id = [user_id for user_id in session.query(User.id).filter_by(username=username)][0][0]
                self.current_username = username

                return "success"

    def hash_password(self, password):
        hasher = hashlib.sha256()
        hasher.update(bytes(password, 'utf-8'))
        return hasher.hexdigest()

    def fetch_track_info(self, id):
        with Session(self.engine) as session:
            track_object = [info for info in session.query(Track).filter_by(id=id)][0]
            track_info = [track_object.artist, track_object.title, track_object.genre, track_object.mood,
                            track_object.instrument, track_object.sound_filepath, track_object.cover_filepath]
        return track_info

    def fetch_username(self, id):
        with Session(self.engine) as session:
            username = [name for name in session.query(User.username).filter_by(id=id)][0][0]
        return username

    def config_like(self, track_id, user_id):

        with Session(self.engine) as session:
            like_search = [like for like in session.query(Like).filter_by(track_id=track_id, user_id=user_id)]

        if len(like_search) == 0:
            return False
        else:
            return True

    def like_track(self, track_id, user_id):

        liked = self.config_like(track_id, user_id)

        if not liked:
            new_like = Like(track_id=track_id, user_id=user_id)

            with Session(self.engine) as session:
                session.add(new_like)
                session.commit()

        else:
            with Session(self.engine) as session:
                session.query(Like).filter_by(track_id=track_id, user_id=user_id).delete()
                session.commit()

    def post_track(self, title, genre, mood, instrument, track_file, cover_file=r"GUI\images\testcover2.png"):

        cover_file = r"GUI\images\testcover2.png" if cover_file is None else cover_file
        shutil.copy(cover_file, r"database/covers")
        shutil.copy(track_file, r"database/tracks")

        cover_file = r"database/covers/" + os.path.basename(cover_file)
        track_file = r"database/tracks/" + os.path.basename(track_file)

        title = self.add_filetype(title, track_file)

        new_track = Track(title=title, artist=self.current_id, genre=genre, mood=mood, instrument=instrument,
                          sound_filepath=track_file, cover_filepath=cover_file)

        with Session(self.engine) as session:
            session.add(new_track)
            session.commit()

    def add_filetype(self, string, track_file):

        string.replace(".mp3", "")
        string.replace(".wav", "")
        string.replace(".", "")
        string.replace(" ", "_")

        filetype = os.path.splitext(os.path.basename(track_file))[1]
        title = string + filetype

        return title

    def fetch_comments(self, track_id):

        with Session(self.engine) as session:
            comment_list = [comment[0] for comment in session.query(Comment.id).filter_by(track_id=track_id)]
        return comment_list

    def fetch_comment_info(self, comment_id):
        with Session(self.engine) as session:
            comment_object = [info for info in session.query(Comment).filter_by(id=comment_id)][0]
            commenter_username = [name for name in session.query(User.username).filter_by(id=comment_object.user_id)][0][0]
            comment_info = [comment_object.text, commenter_username]
        return comment_info

    def post_comment(self, track_id, text):
        new_comment = Comment(user_id=self.current_id, track_id=track_id, text=text)

        with Session(self.engine) as session:
            session.add(new_comment)
            session.commit()

    def construct_frequency_tables(self):

        genre_table = {"pop": 0,
                        "hip-hop": 0,
                        "edm": 0,
                        "rock": 0,
                        "alternative": 0,
                        "cinematic": 0,
                        "classical": 0}

        mood_table = {"chill": 0,
                             "hype": 0,
                             "sad": 0,
                             "dark": 0,
                             "upbeat": 0,
                             "epic": 0}

        instrument_table = {"piano": 0,
                            "drums": 0,
                            "bass": 0,
                            "synth": 0,
                            "guitar": 0,
                            "strings": 0,
                            "vocal": 0}



        with Session(self.engine) as session:
            likes = [like[0] for like in session.query(Like.track_id).filter_by(user_id=self.current_id)]
            track_objects = [info for info in session.query(Track).filter(Track.id.in_(likes)).all()]

            for track in track_objects:
                tags = [track.genre, track.mood, track.instrument]
                genre_table[tags[0]] += 1
                mood_table[tags[1]] += 1
                instrument_table[tags[2]] += 1

        return genre_table, mood_table, instrument_table

    def find_preference_outliers(self):

        genre_table, mood_table, instrument_table = self.construct_frequency_tables()

        preferred_genres = []
        preferred_moods = []
        preferred_instruments = []

        genre_frequencies = [genre_table[genre] for genre in genre_table]
        for genre in genre_table:
            if genre_table[genre] >= mean(genre_frequencies) + (1.5 * stdev(genre_frequencies)):
                preferred_genres.append(genre)

        mood_frequencies = [mood_table[mood] for mood in mood_table]
        for mood in mood_table:
            if mood_table[mood] >= mean(mood_frequencies) + (1.5 * stdev(mood_frequencies)):
                preferred_moods.append(mood)

        instrument_frequencies = [instrument_table[instrument] for instrument in instrument_table]
        for instrument in instrument_table:
            if instrument_table[instrument] >= mean(instrument_frequencies) + (1.5 * stdev(instrument_frequencies)):
                preferred_instruments.append(instrument)

        return preferred_genres, preferred_moods, preferred_instruments
