import os


class SegmentDetector:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def detect_json_transcriptions(self):
        """
        Finds segment JSON files in the same directory as the audio.
        """
        json_transcriptions = []
        base, _ = os.path.splitext(self.audio_file)
        directory = os.path.dirname(base)
        stem = os.path.basename(base)
        index = 0
        while True:
            filename = f"{stem}_segment_{index}.wav.json"
            path = os.path.join(directory, filename) if directory else filename
            if os.path.exists(path):
                json_transcriptions.append(path)
            else:
                break
            index += 1
        return json_transcriptions

    def detect_audio_segments(self):
        """
        Finds segment WAV files in the same directory as the audio.
        """
        segments = []
        base, _ = os.path.splitext(self.audio_file)
        directory = os.path.dirname(base)
        stem = os.path.basename(base)
        index = 0
        while True:
            filename = f"{stem}_segment_{index}.wav"
            path = os.path.join(directory, filename) if directory else filename
            if os.path.exists(path):
                segments.append(path)
            else:
                break
            index += 1
        return segments