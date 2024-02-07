from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import User, Track, Comment, Like, Playlist, Playlist_Track

users = [User(username="evernowbeats", password_hash="86654d079cddef5e6cfba21ac6e39c6d5e2409556eae2577b46515062a138f33"),
         User(username="calvinharris", password_hash="1bac7f7261147f9d8bc935c823d1a40ba439a60e6593b6875ca2218a52ea23bf"),
         User(username="will.is.love", password_hash="33cc47b3f5939d7a88fb35fa2fe014cb01e3deadf2971830648028ded4d54c56"),
         User(username="peachpit", password_hash="497f36b53160eb8904f87389667e883b0cd06a520060e58b9c52fbc775ed78c1"),
         User(username="rahhbeats", password_hash="5a5617c22af86eea0e3eed87cab7e08d65bdd0320d9ff4427d91a89e7b4c56a6"),
         User(username="samgellaitry", password_hash="3df701b1e5b876b215d9ccdc7219d51151063b291cb9b40205151ad87f27af07"),
         User(username="metroboomin", password_hash="8a091f17c8ed00a2e0e623a35dc091419ff19aa382fefa34b0bde7e9207e583d"),
         User(username="michaelabels", password_hash="ca3704aa0b06f5954c79ee837faa152d84d6b2d42838f0637a15eda8337dbdce"),
         User(username="babykeem", password_hash="3d9f93899cb52eb3b1e585959c74db3be4d3eb6397f6f83a6d560f6ab83ce06b"),
         User(username="chrisjones", password_hash="1dad61de33265e5b0752864b857ddaab3653c962f5c276045709109cb6c777a2"),
         User(username="tricoteuse", password_hash="4eeaa32dde86bae21e1cca55c7de2de8afe3760f8073e2b5fb1600d0fc8194f2"),
         User(username="zahara_c", password_hash="df4db5918d4e74c75a494a67a167692e39601a340d4fb6c0da2ef643b9029bd3"),
         User(username="christ+mallards", password_hash="82a4eda9cf6a2ac129a99b34b185ca125305862b9e72f4d8ab8a7d2d8518986f"),
         User(username="geoblu", password_hash="4822284397a3de29b34481d100bc8ac363816263d9489901bf90cb9fa68b0fc3"),
         User(username="davidarcade", password_hash="8f570581e11727e79e027312b0fd31ee69c2ff8a0a2ce2def9038131638b6ce4"),
         User(username="veggi", password_hash="14930a90c71a8711f252995b5c0118e0b41d73f6a2156b9d7b7d46bf79ac16ff"),
         User(username="trndytrndy", password_hash="a972ba1ca9b98011e6ce419f66689a16f2cb72756426230ff6fbb9de0e3fcbd5"),
         User(username="caustonTracks", password_hash="81853435eafa7982268e3071a0b7cc3934996185db070374f4023b395ed65ffe"),
         User(username="adisub0910", password_hash="352165e8f503083d32d160084b9463c3f184dcd2a76c3b445ca458862f8ff0c0")]

tracks = [Track(title="domino.wav", artist=1, genre="hip-hop", mood="dark", instrument="synth", sound_filepath="database/tracks/domino.wav", cover_filepath="database/covers/WhatsApp Image 2023-05-07 at 13.17.32.jpg"),
         Track(title="weekend_remix.mp3", artist=2, genre="pop", mood="chill", instrument="piano", sound_filepath="database/tracks/the-weekend-funk-wav-remix-audio.mp3", cover_filepath="database/covers/R-13722927-1560758585-1493.jpg"),
         Track(title="16.mp3", artist=9, genre="pop", mood="sad", instrument="synth", sound_filepath="database/tracks/16-official-audio.mp3", cover_filepath="database/covers/untitled.jpeg"),
         Track(title="crosswords.mp3", artist=3, genre="edm", mood="dark", instrument="synth", sound_filepath="database/tracks/SpotifyMate.com - Crosswords - will.islove.mp3", cover_filepath="database/covers/CROSSWORDSREDSTICKER.png"),
         Track(title="tommys_party.mp3", artist=4, genre="rock", mood="chill", instrument="guitar", sound_filepath="database/tracks/tommys-party.mp3", cover_filepath="database/covers/22927a8e14101437686b56ce1103e624.1000x1000x1.jpg"),
         Track(title="shubz.mp3", artist=5, genre="edm", mood="chill", instrument="synth", sound_filepath="database/tracks/Jorja Smith x Lzee x AJ Tracey Type Beat - Shubz Summer UK Garage Type Beat 2023.mp3", cover_filepath="database/covers/artworks-AFrsyDcOOpaTLuy0-HlrKuA-t500x500.jpg"),
         Track(title="leave_me.wav", artist=1, genre="hip-hop", mood="sad", instrument="strings", sound_filepath="database/tracks/leaveme.wav", cover_filepath="database/covers/FRAGMENTS.png"),
         Track(title="assumptions.mp3", artist=6, genre="edm", mood="upbeat", instrument="synth", sound_filepath="database/tracks/assumptions-official-visualiser.mp3", cover_filepath="database/covers/artworks-xhoDmsYktkbS-0-t500x500.jpg"),
         Track(title="birthday.mp3", artist=5, genre="hip-hop", mood="chill", instrument="piano", sound_filepath="database/tracks/Potter Payper x Dave Type Beat - Birthday UK Rap Instrumental 2022 (Prod. Rahh Beats).mp3", cover_filepath="database/covers/artworks-SyKvrxsj8nDB7y2P-zy81Xg-t240x240.jpg"),
         Track(title="hummingbird.mp3", artist=7, genre="hip-hop", mood="chill", instrument="drums", sound_filepath="database/tracks/hummingbird-visualizer.mp3", cover_filepath="database/covers/spider-man-across-the-spider-verse-soundtrack-1685634511.jpg"),
         Track(title="serotonin.mp3", artist=4, genre="pop", mood="chill", instrument="guitar", sound_filepath="database/tracks/serotonin-official-visualiser.mp3", cover_filepath="database/covers/artworks-B3ccNPfH9y5V-0-t500x500.jpg"),
         Track(title="a_hero_falls.mp3", artist=8, genre="cinematic", mood="epic", instrument="strings", sound_filepath="database/tracks/a-hero-falls.mp3", cover_filepath="database/covers/ab67616d0000b273c5c223ca9d87d5bf9bd73c5f.jpeg"),
         Track(title="cloud_nine.wav", artist=1, genre="pop", mood="chill", instrument="synth", sound_filepath="database/tracks/cloud nine.wav", cover_filepath="database/covers/dodji-djibom-YPDFvqHFwRA-unsplash.jpg"),
         Track(title="slide.mp3", artist=2, genre="pop", mood="chill", instrument="piano", sound_filepath="database/tracks/slide-official-audio-ft-frank-ocean-migos.mp3", cover_filepath="database/covers/Calvin_Harris_ Slide _single_cover.jpg"),
         Track(title="devotion.wav", artist=1, genre="edm", mood="upbeat", instrument="piano", sound_filepath="database/tracks/devotion.wav", cover_filepath="database/covers/upal-patel-aBQQNHcQLu0-unsplash.jpg"),
         Track(title="north_faces.wav", artist=12, genre="hip-hop", mood="chill", instrument="piano", sound_filepath="database/tracks/NORTH FACES.wav", cover_filepath="database/covers/nikldn-t-6GW8T6Jsc-unsplash.jpg"),
         Track(title="am_i_dreaming.mp3", artist=7, genre="hip-hop", mood="chill", instrument="drums", sound_filepath="database/tracks/hummingbird-visualizer.mp3", cover_filepath="database/covers/spider-man-across-the-spider-verse-soundtrack-1685634511.jpg"),
         Track(title="philanthropy.wav", artist=13, genre="alternative", mood="chill", instrument="guitar", sound_filepath="database/tracks/PHILANTHROPHY.wav", cover_filepath="database/covers/pexels-hanna-yurouskaya-10915190.jpg"),
         Track(title="im_trying.wav", artist=13, genre="pop", mood="dark", instrument="guitar", sound_filepath="database/tracks/imtrying2.wav", cover_filepath="database/covers/testcover2.png"),
         Track(title="loylecarner.wav", artist=13, genre="hip-hop", mood="chill", instrument="drums", sound_filepath="database/tracks/loylecarner.wav", cover_filepath="database/covers/max-letek-4inn20RqF4k-unsplash.jpg"),
         Track(title="mynameisayden.mp3", artist=13, genre="hip-hop", mood="hype", instrument="bass", sound_filepath="database/tracks/mynameisayden.wav", cover_filepath="database/covers/annie-spratt-rAvMLaxQv2M-unsplash.jpg"),
         Track(title="range_brothers.mp3", artist=9, genre="hip-hop", mood="hype", instrument="bass", sound_filepath="database/tracks/range-brothers-official-audio.mp3", cover_filepath="database/covers/Untitled.jpeg"),
         Track(title="family_ties.mp3", artist=9, genre="hip-hop", mood="hype", instrument="strings", sound_filepath="database/tracks/family-ties-official-video.mp3", cover_filepath="database/covers/Untitled.jpeg"),
         Track(title="whispering.mp3", artist=14, genre="hip-hop", mood="chill", instrument="vocal", sound_filepath="database/tracks/GEOBLU - WHISPERING-vocals-Eb major-84bpm(1).mp3", cover_filepath="database/covers/i-am_nah--S4OsO0c6Ts-unsplash.jpg"),
         Track(title="ladlow_trio.wav", artist=13, genre="classical", mood="chill", instrument="piano", sound_filepath="database/tracks/dojojazz.wav", cover_filepath="database/covers/testcover2.png"),
         Track(title="exceptional.mp3", artist=16, genre="edm", mood="chill", instrument="vocal", sound_filepath="database/tracks/exceptional.mp3", cover_filepath="database/covers/artworks-mDRAmgdCe6cKSPcK-sQzzfA-t500x500.jpg"),
         Track(title="snakes_riff.mp3", artist=3, genre="pop", mood="upbeat", instrument="guitar", sound_filepath="database/tracks/snakes_riff.mp3", cover_filepath="database/covers/yQL17qew.png"),
         Track(title="if_u_dont_know.mp3", artist=3, genre="edm", mood="upbeat", instrument="vocal", sound_filepath="database/tracks/if_u_dont_know.mp3", cover_filepath="database/covers/CROSSWORDS.png"),
         Track(title="tours.wav", artist=1, genre="hip-hop", mood="hype", instrument="guitar", sound_filepath="database/tracks/tours.wav", cover_filepath="database/covers/FRAGMENTS 2.png"),
         Track(title="sahara.wav", artist=1, genre="pop", mood="chill", instrument="bass", sound_filepath="database/tracks/sahara.wav", cover_filepath="database/covers/FRAGMENTS 2.png"),
         Track(title="problem.wav", artist=1, genre="alternative", mood="chill", instrument="piano", sound_filepath="database/tracks/problem.wav", cover_filepath="database/covers/FRAGMENTS 2.png"),
         Track(title="remedy.mp3", artist=14, genre="pop", mood="upbeat", instrument="synth", sound_filepath="database/tracks/remedy.wav", cover_filepath="database/covers/testcover2.png"),
         Track(title="Hotel Room", artist=17, genre="alternative", mood="chill", instrument="vocal", sound_filepath="database/tracks/hotel_room.mp3", cover_filepath="database/covers/a3465669682_5.jpg")]

likes = [Like(user_id=1, track_id=3),
    Like(user_id=1, track_id=27),
    Like(user_id=1, track_id=4),
    Like(user_id=1, track_id=13),
    Like(user_id=1, track_id=14),
    Like(user_id=1, track_id=10),
    Like(user_id=10, track_id=25),
    Like(user_id=11, track_id=21),
    Like(user_id=1, track_id=28),
    Like(user_id=1, track_id=2),
    Like(user_id=18, track_id=1),
    Like(user_id=21, track_id=3),
    Like(user_id=1, track_id=7),
    Like(user_id=1, track_id=21),
    Like(user_id=5, track_id=2),
    Like(user_id=5, track_id=11),
    Like(user_id=5, track_id=13),
    Like(user_id=5, track_id=14),
    Like(user_id=5, track_id=30),
    Like(user_id=5, track_id=3),
    Like(user_id=5, track_id=6),
    Like(user_id=5, track_id=32),
    Like(user_id=5, track_id=1),
    Like(user_id=22, track_id=7),
    Like(user_id=22, track_id=3),
    Like(user_id=23, track_id=11),
    Like(user_id=23, track_id=2),
    Like(user_id=24, track_id=8),
    Like(user_id=24, track_id=35)]

comments = [Comment(text="this goes hard", user_id=1, track_id=4),
    Comment(text="i might empty my bank account", user_id=9, track_id=14),
    Comment(text="one last timeee", user_id=5, track_id=4),
    Comment(text="cross the words", user_id=3, track_id=4),
    Comment(text="this is good", user_id=10, track_id=25),
    Comment(text="banging", user_id=11, track_id=21),
    Comment(text="wheres the vocals", user_id=1, track_id=28),
    Comment(text="im 2 phone baby keem", user_id=9, track_id=3),
    Comment(text="i dont know :(", user_id=1, track_id=28),
    Comment(text="goofy ahh riff", user_id=1, track_id=27),
    Comment(text="im going to eaven", user_id=9, track_id=23),
    Comment(text="cold", user_id=5, track_id=9),
    Comment(text="amazing brother", user_id=1, track_id=23),
    Comment(text="bob", user_id=21, track_id=1),
    Comment(text="simon edwards", user_id=22, track_id=7),
    Comment(text="simonedwards650", user_id=22, track_id=23),
    Comment(text="music", user_id=24, track_id=8)]

playlists = [Playlist(id=1,name="six",user_id=1,cover_filepath="database/covers/WhatsApp Image 2023-05-07 at 13.17.32.jpg"),
             Playlist(id=2,name="seven",user_id=1,cover_filepath="database/covers/testcover2.png")]

playlist_tracks = [Playlist_Track(id=4, playlist_id=2, track_id=2),
             Playlist_Track(id=5, playlist_id=2, track_id=26)]
# Connect to the activities database
engine = create_engine('sqlite:///clippr.sqlite', echo=True)

# Create a session and add the people to the database
with Session(engine) as sess:
    sess.add_all(users)
    sess.add_all(tracks)
    sess.add_all(likes)
    sess.add_all(comments)
    sess.add_all(playlists)
    sess.add_all(playlist_tracks)
    sess.commit()
