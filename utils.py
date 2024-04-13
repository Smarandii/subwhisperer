import subprocess

import torch
import ffmpeg
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline
)


def add_subtitles_to_video(input_video_file, subtitle_file, output_file):
    cmd = [
        'ffmpeg',
        '-i', input_video_file,
        '-vf', f"subtitles={subtitle_file}",
        '-c:a', 'copy',
        output_file
    ]
    process = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode != 0:
        print("FFmpeg failed with error code:", process.returncode)
        print("Output:", process.stdout)
        print("Error:", process.stderr)
    else:
        print(f"Video with subtitles saved to {output_file}")


def extract_audio_from_video(input_video_file, output_audio_file):
    ffmpeg.input(input_video_file).output(output_audio_file).run(overwrite_output=True)


def merge_chunks(chunks, threshold=3.5):
    """Merges chunks into groups based on the total duration threshold."""
    merged_chunks = []
    current_group = []
    group_start_time = None
    group_end_time = None

    for chunk in chunks:
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
