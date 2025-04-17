import os


class SegmentDetector:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def detect_json_transcriptions(self):
        """
        Finds segment JSON files by directly matching the audio_file + suffix.
        """
        json_transcriptions = []
        index = 0
        while True:
            path = f"{self.audio_file}_segment_{index}.wav.json"
            if os.path.exists(path):
                json_transcriptions.append(path)
            else:
                break
            index += 1
        return json_transcriptions

    def detect_audio_segments(self):
        """
        Finds segment WAV files by directly matching the audio_file + suffix.
        """
        segments = []
        index = 0
        while True:
            path = f"{self.audio_file}_segment_{index}.wav"
            if os.path.exists(path):
                segments.append(path)
            else:
                break
            index += 1
        return segments
