class Playlist:
    def __init__(self, songs):
        self._songs = songs
        self._cursor = 0

    def __iter__(self):
        self._cursor = 0
        return self

    def __next__(self):
        if self._cursor >= len(self._songs):
            raise StopIteration
        song = self._songs[self._cursor]
        self._cursor += 1
        return song

    def add_song(self, song):
        self._songs.append(song)

    def shuffle(self):
        import random
        random.shuffle(self._songs)


class MusicLibrary:
    def __init__(self, songs):
        self._playlist = Playlist(songs)

    def play(self):
        for song in self._playlist:
            print(f"Playing: {song}")


if __name__ == "__main__":
    songs = ["Bohemian Rhapsody", "Hotel California", "Stairway to Heaven"]
    library = MusicLibrary(songs)
    library.play()