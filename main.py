import os
from utils import (
    extract_audio_from_video,
    merge_chunks,
    get_whisper_pipe,
    generate_srt_file,
    add_subtitles_to_video
)

audio_file = "audio.mp3"
video_file = "input_video.mp4"
subtitle_file = "output.srt"
output_video_file = "output_video.mp4"
pipe = get_whisper_pipe()

if os.path.exists(video_file):
    extract_audio_from_video(
        input_video_file=video_file,
        output_audio_file=audio_file
    )

if os.path.exists(audio_file):
    result = pipe(audio_file)

    print("We got text from audio in chunks:")
    for chunk in result["chunks"]:
        print("Chunk:", chunk)
    print("Merging chunks...")
    merged_chunks = merge_chunks(
        chunks=result["chunks"],
        threshold=3.5
    )
    print("We got merged chunks:")
    for chunk in merged_chunks:
        print("Chunk:", chunk)

    print("Generating srt file...")
    generate_srt_file(
        chunks=merged_chunks,
        output_filename=subtitle_file
    )
    print(f"SRT file generated successfully: {subtitle_file}")

    if os.path.exists(subtitle_file):
        print("Generating video with subtitles...")
        add_subtitles_to_video(
            input_video_file=video_file,
            subtitle_file=subtitle_file,
            output_file=output_video_file
        )
        print(f"Video generated: {output_video_file}")
    else:
        print("Subtitles not found!")
else:
    print("Input audio not found!")
