from sqlalchemy import Column, Integer, String, Table, UniqueConstraint, ForeignKey, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

likes = Table('likes',
              Base.metadata,
              Column('id', Integer, primary_key=True),
              Column('user_id', ForeignKey('user.id')),
              Column('track_id', ForeignKey('track.id')),
              UniqueConstraint('user_id', 'track_id')
              )


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, unique=True, nullable=False)
    profile_picture = Column(BLOB, unique=False, nullable=True)

    liked_tracks = relationship("Track",
                                secondary=likes,
                                order_by='Track.title',
                                back_populates="liked_by_users")

    def __repr__(self):
        return f"<User({self.username})>"


class Track(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True, autoincrement=True)
    artist = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String, unique=False, nullable=False)
    genre = Column(String, unique=False, nullable=False)
    mood = Column(String, unique=False, nullable=False)
    instrument = Column(String, unique=False, nullable=False)
    sound_filepath = Column(String, unique=False, nullable=False)
    cover_filepath = Column(String, unique=False, default=r"GUI\images\testcover2.png")

    liked_by_users = relationship("User",
                                  secondary=likes,
                                  order_by='User.username',
                                  back_populates="liked_tracks")

    def __repr__(self):
        return f"<Track({self.title})>"


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, unique=False, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('track.id'), nullable=False)

    def __repr__(self):
        return f"<Comment({self.id})>"

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('track.id'), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'track_id', name='_user_track_uc'),
                      )

    def __repr__(self):
        return f"<Like({self.user_id}, {self.track_id})>"

class Playlist(Base):
    __tablename__ = 'playlist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    cover_filepath = Column(String, unique=False, nullable=False)

    def __repr__(self):
        return f"<Playlist({self.id})>"


class Playlist_Track(Base):
    __tablename__ = 'playlist_track'
    id = Column(Integer, primary_key=True, autoincrement=True)
    playlist_id = Column(Integer, ForeignKey('playlist.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('track.id'), nullable=False)

    def __repr__(self):
        return f"<Playlist_Track({self.id})>"

