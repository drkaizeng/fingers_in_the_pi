###############################################################
# Implement the following by using a subprocess:
#   Play sound when using the button and stop playback when button is released

from dataclasses import dataclass
from gpiozero import Button  # type: ignore
from signal import pause
import threading
import soundfile as sf  # type: ignore
import numpy
import time
from pathlib import Path
from typing import Final, Union
from multiprocessing import Pool, Process


class MusicButton:
    EVENT_LATENCY: Final[float] = 0.15
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


params = [
    MusicButtonParams(2, "/home/kai/fingers_in_the_pi/fingers_in_the_pi_private_data/home_made_keyboard/do_1_edit.flac")
]
# with Pool(1) as pool:
#     # for _ in pool.imap_unordered(music_button, params):
#     #     ...
#     pool.map_async(music_button, params)
#     print("ok")


process = Process(target=music_button, args=(params[0],), daemon=True)
process.start()

if input("Hit enter to quit") == "":
    process.terminate()



###############################################################
# Play sound when using the button and stop playback when button is released

# from gpiozero import Button  # type: ignore
# from signal import pause
# import threading
# import sounddevice as sd  # type: ignore
# import soundfile as sf  # type: ignore
# import numpy
# import time

# sound_file_path = "/home/kai/fingers_in_the_pi/fingers_in_the_pi_private_data/home_made_keyboard/do_1_edit.flac"
# data, fs = sf.read(sound_file_path, dtype="float32", always_2d=True)
# data = numpy.vstack((data, data, data, data, data))
# do_playback = threading.Event()
# current_frame = 0


# def callback(outdata, frames, time_, status):
#     if not do_playback.is_set():
#         raise sd.CallbackStop()
#     global current_frame
#     remaining = len(data) - current_frame
#     if remaining >= frames:
#         outdata[:frames] = data[current_frame : (current_frame + frames)]
#         current_frame += frames
#     else:
#         outdata[:remaining] = data[current_frame:]
#         diff = frames - remaining
#         outdata[remaining:frames] = data[0:diff]
#         current_frame = diff


# stream = sd.OutputStream(
#     samplerate=fs,
#     channels=data.shape[1],
#     dtype=data.dtype,
#     callback=callback,
#     latency=0,
# )

# is_held = threading.Event()


# def held():
#     do_playback.set()
#     is_held.set()
#     stream.start()
#     while True:
#         if not is_held.is_set():
#             break
#         time.sleep(0.15)


# def released():
#     do_playback.clear()
#     is_held.clear()
#     stream.stop()
#     global current_frame
#     current_frame = 0


# button = Button(pin=2, hold_time=0)
# button.when_held = held
# button.when_released = released

# pause()


###############################################################
# from gpiozero import Button  # type: ignore
# import time
# from signal import pause
# import threading


# is_held = threading.Event()


# def held():
#     print(f"held thread id = {threading.get_ident()}")
#     is_held.set()
#     while True:
#         if not is_held.is_set():
#             break
#         else:
#             time.sleep(0.1)
#             print("held")


# def released():
#     print(f"released thread id = {threading.get_ident()}")
#     is_held.clear()
#     print("released")


# button = Button(pin=2, hold_time=0)
# button.when_held = held
# button.when_released = released

# pause()


###############################################################
# from gpiozero import Button  # type: ignore

# button = Button(24)

# while True:
#     if button.is_pressed:
#         print("Button is pressed")
#     else:
#         print("Button is not pressed")


###############################################################
# from gpiozero import Button  # type: ignore
# from signal import pause
# import time


# def say_hello():
#     end_time = time.time() + 10
#     while time.time() < end_time:
#         print("Hello!")
#     print("done")


# button = Button(2)

# button.when_pressed = say_hello

# pause()
