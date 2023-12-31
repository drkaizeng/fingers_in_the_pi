import soundfile as sf


data, fs = sf.read("/Users/kaiz/tmp/do_1.flac")
sf.write("/Users/kaiz/tmp/do_1.wav", data, fs)
