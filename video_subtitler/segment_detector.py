import os.path


class SegmentDetector:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def detect_json_transcriptions(self):
        json_transcriptions = []
        segment_index = 0
        while True:
            segment_file = f"{self.audio_file}_segment_{segment_index}.wav.json"
            if os.path.exists(segment_file):
                json_transcriptions.append(segment_file)
            segment_index += 1
            if segment_index > 6:
                break
        return json_transcriptions

    def detect_audio_segments(self):
        audio_segments = []
        segment_index = 0
        while True:
            segment_file = f"{self.audio_file}_segment_{segment_index}.wav"
            if os.path.exists(segment_file):
                audio_segments.append(segment_file)
            segment_index += 1
            if segment_index > 6:
                break
        return audio_segments
