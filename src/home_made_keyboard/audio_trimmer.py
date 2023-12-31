from pathlib import Path

import soundfile as sf  # type: ignore


# All the timings are obtained by audio_editor.py

edits = [
    ["do_1.flac", 0.3, 1.3],
    ["fa_1.flac", 0.3, 1.3],
    ["la_1.flac", 0.2, 1.3],
    ["re_1.flac", 0.1, 1.35],
    ["so_1.flac", 0.1, 1.2],
    ["ti_1.flac", 1.2, 2.7],
]

for file_name, start, end in edits:
    file_path = f"/Users/kaiz/tmp/{file_name}"
    data, fs = sf.read(file_path, dtype="float32", always_2d=True)
    start_frame = int(start * fs)
    end_frame = int(end * fs)
    data = data[start_frame:end_frame]
    out_file_path = Path(file_path)
    out_file_path = out_file_path.with_suffix("")
    out_file_path = Path(str(out_file_path.resolve()) + "_edit.flac")
    sf.write(out_file_path, data, fs)
