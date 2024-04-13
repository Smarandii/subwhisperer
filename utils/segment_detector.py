class SegmentDetector:
    def __init__(self, video_file):
        self.video_file = video_file

    def detect_json_transcriptions(self):
        json_transcriptions = []
        segment_index = 0
        while True:
            segment_file = f"{self.video_file}_segment_{segment_index}.wav.json"
            json_transcriptions.append(segment_file)
            segment_index += 1
            if segment_index > 6:
                break
        return json_transcriptions

    def detect_audio_segments(self):
        audio_segments = []
        segment_index = 0
        while True:
            segment_file = f"{self.video_file}_segment_{segment_index}.wav"
            audio_segments.append(segment_file)
            segment_index += 1
            if segment_index > 6:
                break
        return audio_segments
