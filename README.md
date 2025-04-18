# Subwhisperer – Generate subtitles from any video using OpenAI Whisper

Subwhisperer extracts audio from a video, transcribes it with OpenAI Whisper and
generates **SRT** subtitles plus a **plain‑text transcript**.

---

## ✨ Features

* **Audio extraction** – pulls the audio track out of any video that FFmpeg can
  decode.
* **Speech recognition** – runs Whisper *large* locally (GPU or CPU) with
  word‑level timestamps.
* **Smart chunking** – splits long videos on silence then merges chunks so that
  every subtitle line is comfortably readable.
* **Multiple outputs** – `*.srt`, `*.txt`, per‑segment JSON files.

---

## 📋 Requirements

* **Python 3.10+**
* **FFmpeg & FFprobe** – install via your package manager (`sudo apt install ffmpeg`) or [ffbinaries](https://github.com/ffbinaries/ffbinaries-node).
* **Torch + CUDA (optional)** – if you have an NVIDIA GPU you’ll want the GPU
  wheels (see below).

---

## 🚀 Installation

### Dev instalation:
```bash
# 1 Clone the repo (only if you want to run from source)
git clone https://github.com/Smarandii/subwhisperer.git
cd subwhisperer

# 2 Install the Python requirements
#    – GPU users: match the cuXXX part to your CUDA version
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt

#    – CPU‑only users can skip the first line and simply run:
# pip install -r requirements.txt

# 3 (Dev mode) Install the package into your environment
pip install -e .
```

### Regular user installation:

#### GPU users
```bash
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu126
pip install subwhisperer
```
#### CPU users
```bash
pip install subwhisperer
```

---

## 🔧 Usage

From anywhere:

```bash
subwhisperer /path/to/video.mp4 \
             --output_dir outputs/            # optional
             --audio_file custom/audio.mp3    # optional
             --subtitle_file custom/subs.srt  # optional
             --transcription_file out.txt     # optional
```

You can also invoke it directly:

```bash
python -m subwhisperer.cli /path/to/video.mp4
```

The command will:

1. Extract `/output_dir/video.mp3` (or reuse it if it already exists)
2. Split it on silence > 5 s (configurable inside `AudioExtractor`)
3. Transcribe each chunk with Whisper
4. Merge the chunks and write
   * `video.srt` – ready for any player/editor
   * `video.txt` – the plain transcript
   * `*_chunks.json` – raw Whisper output before/after merging

---

## 🗂️ Project layout (important bits)

```
subwhisperer/
├─ src/
│  └─ subwhisperer/
│     ├─ cli.py               # entry‑point / argument parsing
│     └─ core/                # building blocks
│         ├─ audio_extractor.py
│         ├─ whisper_transcriber.py
│         ├─ text_merger.py
│         └─ ...
└─ tests/
   └─ test_process_video.py   # quick smoke test
```

---

## 🆘 Troubleshooting

* *CUDA not detected* – make sure you installed the **matching** Torch wheel and
  that `nvidia-smi` shows your GPU.
* *Subtitles out of sync* – adjust `max_length`, `threshold` or the silence
  parameters in `TextMerger` / `AudioExtractor`.
* *Whisper is slow on CPU* – try `--device cuda` (automatic if CUDA is
  available) or down‑grade to a smaller Whisper model.

---

## 🤝 Contributing

Pull requests and feature ideas are welcome. Please open an issue first if you
plan a large change.

---

## 📄 License

MIT © Smarandii 2024–present

---

### 🙏 Special thanks

Huge thanks to [@arturtur](https://github.com/aturtur) for the After Effects
script that imports SRT files – bundled here as
*Import SRT into Adobe After Effects.jsx*.

---

This tool was developed as personal tool for creating fast subtitles and importing them to AE.
