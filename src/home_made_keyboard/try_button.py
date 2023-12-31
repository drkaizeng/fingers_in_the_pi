###############################################################
from gpiozero import Button  # type: ignore
from signal import pause
import threading
import sounddevice as sd  # type: ignore
import soundfile as sf  # type: ignore
import numpy
import time

sound_file_path = "/home/kai/fingers_in_the_pi/fingers_in_the_pi_private_data/home_made_keyboard/do_1_edit.flac"
data, fs = sf.read(sound_file_path, dtype="float32", always_2d=True)
data = numpy.vstack((data, data, data, data, data))
do_playback = threading.Event()
current_frame = 0


def callback(outdata, frames, time_, status):
    if not do_playback.is_set():
        raise sd.CallbackStop()
    global current_frame
    remaining = len(data) - current_frame
    if remaining >= frames:
        outdata[:frames] = data[current_frame : (current_frame + frames)]
        current_frame += frames
    else:
        outdata[:remaining] = data[current_frame:]
        diff = frames - remaining
        outdata[remaining:frames] = data[0:diff]
        current_frame = diff


stream = sd.OutputStream(
    samplerate=fs,
    channels=data.shape[1],
    dtype=data.dtype,
    callback=callback,
    latency=0,
)

is_held = threading.Event()


def held():
    do_playback.set()
    is_held.set()
    stream = sd.OutputStream(
        samplerate=fs,
        channels=data.shape[1],
        dtype=data.dtype,
        callback=callback,
        latency=0,
    )
    stream.start()
    while True:
        if not is_held.is_set():
            break
        time.sleep(0.1)


def released():
    do_playback.clear()
    is_held.clear()
    stream.close()


button = Button(pin=2, hold_time=0)
button.when_held = held
button.when_released = released

pause()


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
