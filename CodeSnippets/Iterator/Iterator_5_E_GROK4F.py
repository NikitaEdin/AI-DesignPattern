class ChannelCollection:
    def __init__(self):
        self._channels = ['CNN', 'BBC', 'ABC']

    def __iter__(self):
        return ChannelSelector(self._channels)

class ChannelSelector:
    def __init__(self, channels):
        self._channels = channels
        self._position = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._position >= len(self._channels):
            raise StopIteration
        channel = self._channels[self._position]
        self._position += 1
        return channel

if __name__ == "__main__":
    collection = ChannelCollection()
    for channel in collection:
        print(channel)