import os
import json

import torch
import ffmpeg
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline
)


def process_chunks(chunks, srt_filename):
    """Process chunks to merge them and generate an SRT file."""
    print("Merging chunks...")
    merged_chunks = merge_chunks(chunks=chunks, threshold=3.5)
    print("We got merged chunks:")
    for chunk in merged_chunks:
        print("Chunk:", chunk)

    print("Generating srt file...")
    generate_srt_file(chunks=merged_chunks, output_filename=srt_filename)
    print(f"SRT file generated successfully: {srt_filename}")


def create_video_with_subtitles(video_file, srt_file, output_video_file):
    """Generate a video file with subtitles."""
    if os.path.exists(srt_file):
        print("Generating video with subtitles...")
        add_subtitles_to_video(
            input_video_file=video_file,
            subtitle_file=srt_file,
            output_file=output_video_file
        )
        print(f"Video generated: {output_video_file}")
    else:
        print("Subtitles not found!")


def extract_and_process_audio(audio_file, video_file):
    """Extract audio and process it if not already extracted."""
    if not os.path.exists(audio_file):
        extract_audio_from_video(input_video_file=video_file, output_audio_file=audio_file)
    if os.path.exists(audio_file):
        result = get_whisper_pipe()(audio_file)
        print("We got text from audio in chunks:")
        for chunk in result["chunks"]:
            print("Chunk:", chunk)
        return result['chunks']
    else:
        print("Input audio not found!")
        return []


def add_subtitles_to_video(input_video_file, subtitle_file, output_file):
    try:
        video_with_subtitles = ffmpeg.input(input_video_file).output(output_file,
                                                                     vf=f"subtitles='{subtitle_file}'", **{'c:a': 'copy'})
        ffmpeg.run(video_with_subtitles, overwrite_output=True)
        print(f"Video with subtitles saved to {output_file}")
    except ffmpeg.Error as e:
        error_message = e.stderr.decode() if e.stderr else 'No detailed error message available.'
        print(f"An error occurred: {error_message}")


def extract_audio_from_video(input_video_file, output_audio_file):
    ffmpeg.input(input_video_file).output(output_audio_file).run(overwrite_output=True)


def save_chunks_to_json(chunks, filename='chunks.json'):
    """Saves a list of dictionaries to a JSON file.

    Args:
        chunks (list): A list of dictionaries containing chunks.
        filename (str): Filename for the JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)


def load_chunks_from_json(filename='chunks.json'):
    """Loads a list of dictionaries from a JSON file.

    Args:
        filename (str): Filename of the JSON file to read from.

    Returns:
        list: A list of dictionaries read from the JSON file.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def merge_chunks(chunks, threshold=3.5):
    """Merges chunks into groups based on the total duration threshold."""
    merged_chunks = []
    current_group = []
    group_start_time = None
    group_end_time = None

    for chunk in chunks:
        if chunk['timestamp'][0] is None or chunk['timestamp'][1] is None:
            continue
        if not current_group:
            current_group.append(chunk)
            group_start_time = chunk['timestamp'][0]
            group_end_time = chunk['timestamp'][1]
        else:
            potential_end_time = chunk['timestamp'][1]
            group_duration = potential_end_time - group_start_time

            if group_duration <= threshold:
                current_group.append(chunk)
                group_end_time = potential_end_time
            else:
                merged_text = " ".join([c['text'].strip() for c in current_group])
                merged_chunks.append({'text': merged_text, 'timestamp': (group_start_time, group_end_time)})
                current_group = [chunk]
                group_start_time = chunk['timestamp'][0]
                group_end_time = chunk['timestamp'][1]

    if current_group:
        merged_text = " ".join([c['text'].strip() for c in current_group])
        merged_chunks.append({'text': merged_text, 'timestamp': (group_start_time, group_end_time)})

    return merged_chunks


def format_srt_timestamp(seconds):
    hrs, remainder = divmod(seconds, 3600)
    mins, secs = divmod(remainder, 60)
    hrs = int(hrs)
    mins = int(mins)
    millis = int((secs - int(secs)) * 1000)
    secs = int(secs)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"


def generate_srt_file(chunks, output_filename="output.srt"):
    with open(output_filename, "w", encoding="utf-8") as file:
        for i, chunk in enumerate(chunks, start=1):
            start_time = format_srt_timestamp(chunk['timestamp'][0])
            end_time = format_srt_timestamp(chunk['timestamp'][1])
            text = chunk['text']

            file.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")


def get_whisper_pipe():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    ).to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    return pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps="word",
        torch_dtype=torch_dtype,
        device=device,
    )
