from typing import List, Optional
import logging

class Amplifier:
    def on(self) -> None: logging.info("Amp on")
    def off(self) -> None: logging.info("Amp off")
    def set_volume(self, level: int) -> None:
        if not 0 <= level <= 100: raise ValueError("Volume 0-100")
        logging.info(f"Amp volume {level}")

class Tuner:
    def on(self) -> None: logging.info("Tuner on")
    def off(self) -> None: logging.info("Tuner off")
    def set_frequency(self, freq: float) -> None: logging.info(f"Tuner {freq}MHz")

class Streamer:
    def on(self) -> None: logging.info("Streamer on")
    def off(self) -> None: logging.info("Streamer off")
    def play(self, track: str) -> None: logging.info(f"Playing {track}")

class Lights:
    def dim(self, level: int) -> None:
        if not 0 <= level <= 100: raise ValueError("Lights 0-100")
        logging.info(f"Lights dimmed to {level}%")
    def off(self) -> None: logging.info("Lights off")

class HomeTheaterController:
    def __init__(self):
        self._amp = Amplifier()
        self._tuner = Tuner()
        self._streamer = Streamer()
        self._lights = Lights()
        self._current_track: Optional[str] = None

    def watch_movie(self, title: str) -> None:
        logging.info("Get ready to watch...")
        self._lights.dim(10)
        self._amp.on()
        self._amp.set_volume(30)
        self._streamer.on()
        self._streamer.play(title)
        self._current_track = title

    def listen_to_radio(self, station: float) -> None:
        logging.info("Tuning to radio...")
        self._lights.dim(50)
        self._tuner.on()
        self._tuner.set_frequency(station)
        self._amp.on()
        self._amp.set_volume(20)

    def end_session(self) -> None:
        logging.info("Shutting down...")
        self._streamer.off()
        self._tuner.off()
        self._amp.off()
        self._lights.off()
        self._current_track = None

    def get_status(self) -> str:
        return f"Currently playing: {self._current_track or 'Nothing'}"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    system = HomeTheaterController()
    system.watch_movie("Inception")
    print(system.get_status())
    system.end_session()
    system.listen_to_radio(102.5)
    system.end_session()