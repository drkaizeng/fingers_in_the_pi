import time
import sounddevice as sd  # type: ignore
import soundfile as sf  # type: ignore


while True:
    prefix = input("Enter file name prefix to start recording: ")
    if len(prefix) > 0:
        break

fs = 44100
duration = 3  # seconds
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, blocking=True)

print("finished recording\n")
time.sleep(1)

print("playing\n")
sd.play(myrecording, fs, blocking=True)

print("writing\n")
sf.write(
    f"/Users/kaiz/tmp/{prefix}.flac",
    myrecording,
    samplerate=fs,
)

print("all done")
