import time
import sounddevice as sd  # type: ignore
import soundfile as sf  # type: ignore


while True:
    prefix = input("Enter file name prefix to start recording: ")
    if len(prefix) > 0:
        break

fs = 44100
duration = 5  # seconds
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()

print("finished recording\n")
time.sleep(1)

print("playing\n")
sd.play(myrecording, fs)
sd.wait()

print("writing\n")
sf.write(
    f"/home/kai/fingers_in_the_pi/fingers_in_the_pi_private_data/home_made_keyboard/{prefix}.flac",
    myrecording,
    samplerate=fs,
)
