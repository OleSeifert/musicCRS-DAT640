class Song:
    def __init__(self,  album_id=None, album_name=None, album_popularity=None, album_type=None,
                 artists=None, artist_0 = None, artist_1=None, artist_2=None, artist_3=None, artist_4=None,
                 artist_id=None, duration_sec=None, label=None, release_date=None, total_tracks=None, track_id=None,track_name = None,
                 track_number=None, artist_genres=None, artist_popularity=None,
                 followers=None, name=None, genre_0=None, genre_1=None, genre_2=None, genre_3=None, genre_4=None,
                 acousticness=None, analysis_url=None, danceability=None, duration_ms=None, energy=None,
                 instrumentalness=None, key=None, liveness=None, loudness=None, mode=None, speechiness=None, tempo=None,
                 time_signature=None, track_href=None, track_type=None, uri=None, valence=None, explicit=None,
                 track_popularity=None, release_year=None, release_month=None, rn=None):
        self.album_id = album_id
        self.album_name = album_name
        self.album_popularity = album_popularity
        self.album_type = album_type
        self.artists = artists
        self.artist_0 = artist_0
        self.artist_1 = artist_1
        self.artist_2 = artist_2
        self.artist_3 = artist_3
        self.artist_4 = artist_4
        self.artist_id = artist_id
        self.duration_sec = duration_sec
        self.label = label
        self.release_date = release_date
        self.total_tracks = total_tracks
        self.track_id = track_id
        self.track_name = track_name
        self.track_number = track_number
        self.artist_genres = artist_genres
        self.artist_popularity = artist_popularity
        self.followers = followers
        self.name = name
        self.genre_0 = genre_0
        self.genre_1 = genre_1
        self.genre_2 = genre_2
        self.genre_3 = genre_3
        self.genre_4 = genre_4
        self.acousticness = acousticness
        self.analysis_url = analysis_url
        self.danceability = danceability
        self.duration_ms = duration_ms
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.key = key
        self.liveness = liveness
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.tempo = tempo
        self.time_signature = time_signature
        self.track_href = track_href
        self.track_type = track_type
        self.uri = uri
        self.valence = valence
        self.explicit = explicit
        self.track_popularity = track_popularity
        self.release_year = release_year
        self.release_month = release_month
        self.rn = rn

    def serialize(self):
        return {
            'album_id': self.album_id,
            'album_name': self.album_name,
            'album_popularity': self.album_popularity,
            'album_type': self.album_type,
            'artists': self.artists,
            'artist_0': self.artist_0,
            'artist_1': self.artist_1,
            'artist_2': self.artist_2,
            'artist_3': self.artist_3,
            'artist_4': self.artist_4,
            'artist_id': self.artist_id,
            'duration_sec': self.duration_sec,
            'label': self.label,
            'release_date': self.release_date,
            'total_tracks': self.total_tracks,
            'track_id': self.track_id,
            'track_name': self.track_name,
            'track_number': self.track_number,
            'artist_genres': self.artist_genres,
            'artist_popularity': self.artist_popularity,
            'followers': self.followers,
            'name': self.name,
            'genre_0': self.genre_0,
            'genre_1': self.genre_1,
            'genre_2': self.genre_2,
            'genre_3': self.genre_3,
            'genre_4': self.genre_4,
            'acousticness': self.acousticness,
            'analysis_url': self.analysis_url,
            'danceability': self.danceability,
            'duration_ms': self.duration_ms,
            'energy': self.energy,
            'instrumentalness': self.instrumentalness,
            'key': self.key,
            'liveness': self.liveness,
            'loudness': self.loudness,
            'mode': self.mode,
            'speechiness': self.speechiness,
            'tempo': self.tempo,
            'time_signature': self.time_signature,
            'track_href': self.track_href,
            'type': self.track_type,
            'uri': self.uri,
            'valence': self.valence,
            'explicit': self.explicit,
            'track_popularity': self.track_popularity,
            'release_year': self.release_year,
            'release_month': self.release_month,
            'rn': self.rn
        }

    def __eq__(self, other):
        if not isinstance(other, Song):
            return False
        # Confrontiamo tutti gli attributi rilevanti
        return (
                self.album_id == other.album_id and
                self.album_name == other.album_name and
                self.album_popularity == other.album_popularity and
                self.album_type == other.album_type and
                self.artists == other.artists and
                self.artist_0 == other.artist_0 and
                self.artist_1 == other.artist_1 and
                self.artist_2 == other.artist_2 and
                self.artist_3 == other.artist_3 and
                self.artist_4 == other.artist_4 and
                self.artist_id == other.artist_id and
                self.duration_sec == other.duration_sec and
                self.label == other.label and
                self.release_date == other.release_date and
                self.total_tracks == other.total_tracks and
                self.track_id == other.track_id and
                self.track_name == other.track_name and
                self.track_number == other.track_number and
                self.artist_genres == other.artist_genres and
                self.artist_popularity == other.artist_popularity and
                self.followers == other.followers and
                self.name == other.name and
                self.genre_0 == other.genre_0 and
                self.genre_1 == other.genre_1 and
                self.genre_2 == other.genre_2 and
                self.genre_3 == other.genre_3 and
                self.genre_4 == other.genre_4 and
                self.acousticness == other.acousticness and
                self.analysis_url == other.analysis_url and
                self.danceability == other.danceability and
                self.duration_ms == other.duration_ms and
                self.energy == other.energy and
                self.instrumentalness == other.instrumentalness and
                self.key == other.key and
                self.liveness == other.liveness and
                self.loudness == other.loudness and
                self.mode == other.mode and
                self.speechiness == other.speechiness and
                self.tempo == other.tempo and
                self.time_signature == other.time_signature and
                self.track_href == other.track_href and
                self.track_type == other.track_type and
                self.uri == other.uri and
                self.valence == other.valence and
                self.explicit == other.explicit and
                self.track_popularity == other.track_popularity and
                self.release_year == other.release_year and
                self.release_month == other.release_month and
                self.rn == other.rn
        )

    def __hash__(self):
        # Hash basato su tutti gli attributi
        return hash((
            self.album_id, self.album_name, self.album_popularity, self.album_type, self.artists, self.artist_0,
            self.artist_1, self.artist_2, self.artist_3,
            self.artist_4, self.artist_id, self.duration_sec, self.label, self.release_date, self.total_tracks,
            self.track_id, self.track_name, self.track_number,
            self.artist_genres, self.artist_popularity, self.followers, self.name, self.genre_0, self.genre_1,
            self.genre_2, self.genre_3, self.genre_4,
            self.acousticness, self.analysis_url, self.danceability, self.duration_ms, self.energy,
            self.instrumentalness, self.key, self.liveness,
            self.loudness, self.mode, self.speechiness, self.tempo, self.time_signature, self.track_href,
            self.track_type, self.uri, self.valence, self.explicit,
            self.track_popularity, self.release_year, self.release_month, self.rn
        ))
    def __str__(self):
        # Creiamo una lista dinamica degli artisti
        artists = [self.artist_0, self.artist_1, self.artist_2, self.artist_3, self.artist_4]
        # Rimuoviamo i valori None o vuoti
        artists = [artist for artist in artists if artist]

        # Se esiste almeno un artista, creiamo la stringa
        if artists:
            artist_string = ", ".join(artists)
            return f"{self.track_name} by {artist_string}"
        else:
            return f"{self.track_name} by Unknown Artist"