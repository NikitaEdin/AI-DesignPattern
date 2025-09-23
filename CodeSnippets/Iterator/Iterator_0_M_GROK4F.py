class Song:
    def __init__(self, title):
        self.title = title

class Playlist:
    def __init__(self):
        self.songs = []

    def add_song(self, song):
        if not isinstance(song, Song):
            raise ValueError("Must be a Song object")
        self.songs.append(song)

    def __iter__(self):
        return SongPlayer(self.songs)

class SongPlayer:
    def __init__(self, songs):
        self.songs = songs
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.songs):
            raise StopIteration
        song = self.songs[self.index]
        self.index += 1
        return song

    def reset(self):
        self.index = 0

if __name__ == "__main__":
    playlist = Playlist()
    playlist.add_song(Song("Bohemian Rhapsody"))
    playlist.add_song(Song("Stairway to Heaven"))
    playlist.add_song(Song("Hotel California"))

    player = iter(playlist)
    print(next(player).title)
    print(next(player).title)

    player.reset()
    print("After reset:")
    for song in player:
        print(song.title)