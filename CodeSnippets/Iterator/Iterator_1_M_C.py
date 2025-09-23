class BookCollection:
    def __init__(self):
        self._books = []
        self._current_index = 0
    
    def add_book(self, title, author):
        self._books.append({"title": title, "author": author})
    
    def __iter__(self):
        self._current_index = 0
        return self
    
    def __next__(self):
        if self._current_index >= len(self._books):
            raise StopIteration
        
        book = self._books[self._current_index]
        self._current_index += 1
        return book
    
    def has_next(self):
        return self._current_index < len(self._books)
    
    def reset(self):
        self._current_index = 0
    
    def count(self):
        return len(self._books)

class Playlist:
    def __init__(self, name):
        self.name = name
        self._songs = []
    
    def add_song(self, title, artist, duration):
        self._songs.append({"title": title, "artist": artist, "duration": duration})
    
    def get_traverser(self):
        return PlaylistTraverser(self._songs)

class PlaylistTraverser:
    def __init__(self, songs):
        self._songs = songs
        self._position = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._position >= len(self._songs):
            raise StopIteration
        
        song = self._songs[self._position]
        self._position += 1
        return song

if __name__ == "__main__":
    library = BookCollection()
    library.add_book("1984", "George Orwell")
    library.add_book("Dune", "Frank Herbert")
    library.add_book("Foundation", "Isaac Asimov")
    
    for book in library:
        print(f"{book['title']} by {book['author']}")
    
    my_playlist = Playlist("Favorites")
    my_playlist.add_song("Bohemian Rhapsody", "Queen", 355)
    my_playlist.add_song("Stairway to Heaven", "Led Zeppelin", 482)
    
    song_walker = my_playlist.get_traverser()
    for song in song_walker:
        print(f"{song['title']} - {song['artist']} ({song['duration']}s)")