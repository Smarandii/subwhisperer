import os
import ffmpeg
from pydub import AudioSegment
from pydub.silence import detect_nonsilent


class AudioExtractor:
    def __init__(self, min_silence_len=1000, silence_thresh=-60, min_length=30000, max_length=60000):
        self.min_silence_len = min_silence_len
        self.silence_thresh = silence_thresh
        self.min_length = min_length
        self.max_length = max_length

    def extract_audio_and_find_pauses(self, video_file, audio_file='audio.mp3'):
        if not os.path.exists(audio_file):
            ffmpeg.input(video_file).output(audio_file).run()
        sound = AudioSegment.from_file(audio_file)
        nonsilent_parts = detect_nonsilent(sound, min_silence_len=self.min_silence_len, silence_thresh=self.silence_thresh, seek_step=1)
        total_duration_ms = len(sound)
        return nonsilent_parts, total_duration_ms

    def split_audio_based_on_silence(self, audio_file, nonsilent_parts, total_duration_ms):
        segments = []
        last_split_point = 0
        for start, end in nonsilent_parts:
            if start - last_split_point > self.max_length:
                segment_duration = start - last_split_point
            elif end - last_split_point > self.min_length:
                segment_duration = end - last_split_point
            else:
                continue
            segment_file = f"{audio_file}_segment_{len(segments)}.wav"
            ffmpeg.input(audio_file, ss=last_split_point / 1000, t=segment_duration / 1000).output(segment_file).run()
            segments.append(segment_file)
            last_split_point = end
        if last_split_point < total_duration_ms:
            remaining_duration = total_duration_ms - last_split_point
            if remaining_duration > self.min_length:
                segment_file = f"{audio_file}_segment_{len(segments)}.wav"
                ffmpeg.input(audio_file, ss=last_split_point / 1000, t=remaining_duration / 1000).output(segment_file).run()
                segments.append(segment_file)
        return segments
