import os
from utils import (
    load_chunks_from_json,
    save_chunks_to_json,
    process_chunks,
    extract_and_process_audio,
    create_video_with_subtitles
)


def main():
    audio_file = "audio.mp3"
    video_file = "input_video.mp4"
    subtitle_file = "output.srt"
    output_video_file = "output_video.mp4"
    chunks_file = 'chunks.json'

    if os.path.exists(chunks_file):
        print("Skipping extraction of audio, because we found chunks.json...")
        loaded_chunks = load_chunks_from_json(chunks_file)
        process_chunks(loaded_chunks, subtitle_file)
    else:
        chunks = extract_and_process_audio(audio_file, video_file)
        if chunks:
            save_chunks_to_json(chunks, chunks_file)
            process_chunks(chunks, subtitle_file)

    create_video_with_subtitles(video_file, subtitle_file, output_video_file)


if __name__ == "__main__":
    main()
