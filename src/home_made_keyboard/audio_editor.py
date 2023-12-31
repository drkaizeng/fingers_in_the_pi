# The audio files are visualised using a free online audio editor
# https://audiomass.co/
# The section with the most stable sound is chosen and is repeated to check whether there are audible glitches.

import threading
import time

import sounddevice as sd  # type: ignore
import soundfile as sf  # type: ignore

import numpy

assert numpy


source_file = "/Users/kaiz/tmp/ti_1.flac"
start = 1.2  # seconds
end = 2.7  # seconds

data, fs = sf.read(source_file, dtype="float32", always_2d=True)

# trim data
start_frame = int(start * fs)
end_frame = int(end * fs)
data = data[start_frame:end_frame]

# data = numpy.vstack((data, data, data, data, data))
# sd.play(data, fs, blocking=True)

current_frame = 0
event = threading.Event()


def callback(outdata, frames, time, status):
    if event.is_set():
        raise sd.CallbackStop()
    global current_frame
    remaining = len(data) - current_frame
    if remaining >= frames:
        outdata[:frames] = data[current_frame : (current_frame + frames)]
        current_frame += frames
    else:
        outdata[:remaining] = data[current_frame : (current_frame + remaining)]
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

stream.start()
time.sleep(5)
event.set()
stream.abort()
