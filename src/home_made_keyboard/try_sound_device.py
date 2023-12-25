import threading

import sounddevice as sd  # type: ignore
import soundfile as sf  # type: ignore

import sys
sys.path.append('/usr/lib/python3/dist-packages')

import numpy as np
assert np


event = threading.Event()

data, fs = sf.read(
    "/home/kai/fingers_in_the_pi/fingers_in_the_pi_private_data/home_made_keyboard/CantinaBand3.wav",
    always_2d=True,
)

current_frame = 0


def callback(outdata, frames, time, status):
    global current_frame
    if status:
        print(status)
    chunksize = min(len(data) - current_frame, frames)
    outdata[:chunksize] = data[current_frame : current_frame + chunksize]
    if chunksize < frames:
        outdata[chunksize:] = 0
        raise sd.CallbackStop()
    current_frame += chunksize


stream = sd.OutputStream(
    samplerate=fs, device=0, channels=data.shape[1], callback=callback, finished_callback=event.set
)
with stream:
    event.wait()  # Wait until playback is finished
