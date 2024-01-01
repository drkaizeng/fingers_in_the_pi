import sys
import threading
import time
from dataclasses import dataclass
from multiprocessing import Process
from pathlib import Path
from signal import pause
from typing import Final, Union

import numpy
import soundfile as sf  # type: ignore
from gpiozero import Button  # type: ignore


class MusicButton:
    EVENT_LATENCY: Final[float] = 0.1
    SOUND_LEN_MULTIPLE: Final[int] = 5

    def __init__(self, pin_num: int, sound_file_path: Union[Path, str]) -> None:
        self.button = Button(pin=pin_num, hold_time=0)
        self.button.when_held = self.when_held
        self.button.when_released = self.when_released

        self.sound_data, fs = sf.read(sound_file_path, dtype="float32", always_2d=True)
        self.sound_data = numpy.vstack((self.sound_data,) * MusicButton.SOUND_LEN_MULTIPLE)  # type: ignore

        self.current_frame = 0

        # sounddevice idiosyncrasy: import within the subprocess as opposed to at the top of the file
        import sounddevice as sd  # type: ignore

        self.stream = sd.OutputStream(
            samplerate=fs,
            channels=self.sound_data.shape[1],
            dtype=self.sound_data.dtype,
            callback=self.callback,
            latency=0,
        )

        self.is_held = threading.Event()

    def when_held(self) -> None:
        self.is_held.set()
        self.stream.start()
        while True:
            if not self.is_held.is_set():
                break
            time.sleep(MusicButton.EVENT_LATENCY)

    def callback(self, outdata, frames, time_, status) -> None:
        remaining = len(self.sound_data) - self.current_frame
        if remaining >= frames:
            outdata[:frames] = self.sound_data[self.current_frame : (self.current_frame + frames)]
            self.current_frame += frames
        else:
            outdata[:remaining] = self.sound_data[self.current_frame :]
            diff = frames - remaining
            outdata[remaining:frames] = self.sound_data[0:diff]
            self.current_frame = diff

    def when_released(self):
        self.is_held.clear()
        self.stream.stop()
        self.current_frame = 0


@dataclass
class MusicButtonParams:
    pin_num: int
    sound_file_path: Union[Path, str]


def music_button(params: MusicButtonParams) -> None:
    MusicButton(params.pin_num, params.sound_file_path)
    pause()


def main() -> int:
    root_path = Path("/home/kai/fingers_in_the_pi/fingers_in_the_pi_private_data/home_made_keyboard")
    note_pin_list = [
        ("fa", 26),
        ("so", 6),
        ("la", 5),
        ("ti", 11),
        ("do", 9),
        ("re", 22)
    ]
    procs = []
    for note, pin in note_pin_list:
        params = MusicButtonParams(pin, root_path / f"{note}_1_edit.flac")
        process = Process(target=music_button, args=(params,), daemon=True)
        process.start()
        procs.append(process)

    if input("Hit enter to quit") == "":
        for p in procs:
            p.terminate()

    return 0


if __name__ == "__main__":
    sys.exit(main())
