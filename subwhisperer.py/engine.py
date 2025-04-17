import os
import argparse

from subwhisperer.core import (
    TextMerger, FileUtility, AudioExtractor,
    SegmentDetector, WhisperTranscriber, TranscriptionProcessor
)


def setup_argument_parser():
    parser = argparse.ArgumentParser(description="Process video files for audio extraction and subtitle generation.")
    parser.add_argument("video_file", help="The path to the video file to process.")
    parser.add_argument("-a", "--audio_file", help="The path to save the extracted audio file.", required=False)
    parser.add_argument("-s", "--subtitle_file", help="The path to save the subtitle file.", required=False)
    parser.add_argument("-t", "--transcription_file", help="The path to save the transcription file.", required=False)
    parser.add_argument(
        "-o", "--output_dir",
        help="Directory where all generated files will be saved.",
        required=False
    )
    return parser


def process_video(
    video_file_full_path,
    audio_file_full_path=None,
    subtitle_file_full_path=None,
    txt_file_full_path=None,
    output_directory_full_path=None,
    device=None,
):
    # ensure output directory exists if provided
    if output_directory_full_path:
        os.makedirs(output_directory_full_path, exist_ok=True)

    # determine defaults for audio and subtitle paths
    base_name = os.path.splitext(os.path.basename(video_file_full_path))[0]

    if output_directory_full_path:
        if not audio_file_full_path:
            audio_file_full_path = os.path.join(output_directory_full_path, f"{base_name}.mp3")
        if not subtitle_file_full_path:
            subtitle_file_full_path = os.path.join(output_directory_full_path, f"{base_name}.srt")
        if not txt_file_full_path:
            txt_file_full_path = os.path.join(output_directory_full_path, f"{base_name}.txt")
        merged_json_file = os.path.join(output_directory_full_path, f"{base_name}_merged_chunks.json")
        unmerged_json_chunks_file = os.path.join(output_directory_full_path, f"{base_name}_unmerged_chunks.json")
    else:
        if not audio_file_full_path:
            audio_file_full_path = f"{base_name}.mp3"
        if not subtitle_file_full_path:
            subtitle_file_full_path = f"{base_name}.srt"
        if not txt_file_full_path:
            txt_file_full_path = f"{base_name}.txt"
        merged_json_file = f"{base_name}_merged_chunks.json"
        unmerged_json_chunks_file = f"{base_name}_unmerged_chunks.json"

    print(f"Starting processing of '{video_file_full_path}'...")

    ae = AudioExtractor(min_silence_len=5000, silence_thresh=-10)
    fu = FileUtility()
    sg = SegmentDetector(audio_file=audio_file_full_path)
    tm = TextMerger()

    segments = sg.detect_audio_segments()
    print(f"Found existing segments: {segments}")
    json_transcriptions = sg.detect_json_transcriptions()
    print(f"Found existing JSON transcriptions: {json_transcriptions}")

    if not segments:
        # extract audio and find pauses
        pauses, total_duration_ms = ae.extract_audio_and_find_pauses(
            video_file_full_path,
            audio_file_full_path
        )

        if pauses is None:
            segments = [audio_file_full_path]
            print(f"Audio duration {total_duration_ms}ms <= 180000ms; skipping split into segments.")
        else:
            # split based on silence
            segments = ae.split_audio_based_on_silence(
                audio_file_full_path,
                pauses,
                total_duration_ms
            )
            print(f"Split audio into segments: {segments}")

    if not json_transcriptions:
        wt = WhisperTranscriber()
        tp = TranscriptionProcessor(
            whisper_model=wt.transcribe,
            output_dir=output_directory_full_path
        )
        transcriptions = tp.transcribe_segments(segments)
    elif json_transcriptions and not os.path.exists(merged_json_file):
        transcriptions = []
        for transcription in json_transcriptions:
            t = fu.load_chunks_from_json(transcription)
            transcriptions.extend(t)
        fu.save_chunks_to_json(transcriptions, filename=unmerged_json_chunks_file)

    if not os.path.exists(merged_json_file):
        merged_chunks = tm.merge_chunks(transcriptions)
        fu.save_chunks_to_json(merged_chunks, filename=merged_json_file)
    else:
        merged_chunks = fu.load_chunks_from_json(merged_json_file)

    fu.generate_srt_file(merged_chunks, output_filename=subtitle_file_full_path)
    print(f"Generated subtitles: {subtitle_file_full_path}")

    fu.generate_txt_file(merged_chunks, output_filename=txt_file_full_path)
    print(f"Generated plain‑text transcript: {txt_file_full_path}")


def main():
    parser = setup_argument_parser()
    args = parser.parse_args()
    process_video(
        video_file_full_path=args.video_file,
        audio_file_full_path=args.audio_file,
        subtitle_file_full_path=args.subtitle_file,
        txt_file_full_path=args.transcription_file,
        output_directory_full_path=args.output_dir
    )
