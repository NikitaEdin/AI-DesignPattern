class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

class Playlist:
    def __init__(self):
        self._songs = []

    def add_song(self, song):
        if not isinstance(song, Song):
            raise ValueError("Must provide a valid Song object")
        self._songs.append(song)

    def __len__(self):
        return len(self._songs)

    def __iter__(self):
        return PlaylistNavigator(self._songs)

class PlaylistNavigator:
    def __init__(self, songs):
        self._songs = songs
        self._position = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._position >= len(self._songs):
            raise StopIteration
        current_song = self._songs[self._position]
        self._position += 1
        return current_song

if __name__ == "__main__":
    playlist = Playlist()
    playlist.add_song(Song("Bohemian Rhapsody", "Queen"))
    playlist.add_song(Song("Stairway to Heaven", "Led Zeppelin"))
    playlist.add_song(Song("Hotel California", "Eagles"))

    print("Playlist songs:")
    for song in playlist:
        print(f"{song.title} by {song.artist}")
    print(f"Total songs: {len(playlist)}")