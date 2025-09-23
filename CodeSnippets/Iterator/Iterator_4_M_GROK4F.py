class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

class Playlist:
    def __init__(self):
        self.songs = []

    def add_song(self, song):
        if song is not None:
            self.songs.append(song)
        else:
            raise ValueError("Song cannot be None")

    def __iter__(self):
        return PlaylistWalker(self, reverse=False)

    def get_reverse_walker(self):
        return PlaylistWalker(self, reverse=True)

class PlaylistWalker:
    def __init__(self, playlist, reverse=False):
        self.playlist = playlist
        self.reverse = reverse
        if reverse:
            self.position = len(playlist.songs)
        else:
            self.position = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.reverse:
            if self.position <= 0:
                raise StopIteration
            song = self.playlist.songs[self.position - 1]
            self.position -= 1
        else:
            if self.position >= len(self.playlist.songs):
                raise StopIteration
            song = self.playlist.songs[self.position]
            self.position += 1
        return song

if __name__ == "__main__":
    playlist = Playlist()
    try:
        playlist.add_song(Song("Song1", "Artist1"))
        playlist.add_song(Song("Song2", "Artist2"))
        print("Forward:")
        for song in playlist:
            print(f"{song.title} by {song.artist}")
        print("Reverse:")
        reverse_walker = playlist.get_reverse_walker()
        for song in reverse_walker:
            print(f"{song.title} by {song.artist}")
    except ValueError as e:
        print(f"Error: {e}")