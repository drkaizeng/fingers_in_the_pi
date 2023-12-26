import threading
import time

import sounddevice as sd  # type: ignore
import soundfile as sf  # type: ignore

import numpy as np  # type: ignore

assert np


event = threading.Event()

data, fs = sf.read(
    "/home/kai/fingers_in_the_pi/fingers_in_the_pi_private_data/home_made_keyboard/CantinaBand3.wav",
    always_2d=True,
)

current_frame = 0


# def callback(outdata, frames, time, status):
#     global current_frame
#     if status:
#         print(status)
#     chunksize = min(len(data) - current_frame, frames)
#     outdata[:chunksize] = data[current_frame : current_frame + chunksize]
#     if chunksize < frames:
#         outdata[chunksize:] = 0
#         raise sd.CallbackStop()
#     current_frame += chunksize


# stream = sd.OutputStream(
#     samplerate=fs, device=0, channels=data.shape[1], callback=callback, finished_callback=event.set
# )
# with stream:
#     event.wait()  # Wait until playback is finished


##########################################
# Try to stop playback halfway
current_frame = 0
event.clear()


def interrupted_callback(outdata, frames, time, status):
    if event.is_set():
        raise sd.CallbackAbort()
    global current_frame
    if status:
        print(status)
    chunksize = min(len(data) - current_frame, frames)
    outdata[:chunksize] = data[current_frame : current_frame + chunksize]
    if chunksize < frames:
        outdata[chunksize:] = 0
        raise sd.CallbackStop()
    current_frame += chunksize


interrupted_stream = sd.OutputStream(
    samplerate=fs,
    device=0,
    channels=data.shape[1],
    callback=interrupted_callback,
    finished_callback=event.set,
    latency=0,
)

with interrupted_stream:
    time.sleep(5)
    event.set()
    event.wait()


##########################################
# Make playback repeat

current_frame = 0
event.clear()


def repeat_callback(outdata, frames, time, status):
    if event.is_set():
        raise sd.CallbackAbort()
    global current_frame
    if status:
        print(status)
    remaining = len(data) - current_frame
    if remaining >= frames:
        outdata[:frames] = data[current_frame : current_frame + frames]
        current_frame += frames
    else:
        outdata[:remaining] = data[current_frame : current_frame + remaining]
        diff = frames - remaining
        outdata[remaining:frames] = data[0:diff]
        current_frame = diff


interrupted_stream = sd.OutputStream(
    samplerate=fs,
    device=0,
    channels=data.shape[1],
    callback=repeat_callback,
    finished_callback=event.set,
    latency=0,
)

with interrupted_stream:
    time.sleep(20)
    event.set()
    event.wait()
