# Video Subtitler with Whisper

This repository contains a Python application that extracts audio from a video file, transcribes it using OpenAI's Whisper model, generates subtitles in SRT format, and then overlays these subtitles onto the original video.

## Features

- **Audio Extraction**: Extracts audio from a video file.
- **Speech Recognition**: Transcribes audio to text using OpenAI's Whisper model.
- **Subtitle Generation**: Converts transcribed text into SRT format.
- **Video Processing**: Embeds the generated subtitles into the video.

## Requirements

- Python 3.x
- FFmpeg
- Various Python libraries listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Smarandii/video_subtitler.git
   cd video-subtitler
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure FFmpeg is installed on your system. Visit the [FFmpeg download page](https://ffmpeg.org/download.html) for installation instructions.

## Usage

1. Place your video file named `input_video.mp4` in the root directory of this project.

2. Run the main script:
   ```bash
   python main.py
   ```

3. The script will perform the following actions:
   - Extract audio from the video.
   - Transcribe the audio to text.
   - Generate an SRT file with the transcriptions.
   - Embed the SRT file as subtitles in a new video file named `output_video.mp4`.

## Files Description

- `main.py`: The main Python script that orchestrates the extraction, transcription, and video processing.
- `utils.py`: Contains helper functions for audio extraction, transcription, subtitle generation, and video processing.
- `requirements.txt`: A list of Python libraries required to run the application.

## Troubleshooting

If you encounter any issues with the transcription or video processing:
- Ensure that your FFmpeg installation is up to date.
- Check that the paths and filenames in the scripts are correct.
- Verify that the audio and video files are not corrupted and are in a format supported by FFmpeg.

## Contributing

Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.

## License

This project is open-sourced under the MIT License. See the LICENSE file for more details.