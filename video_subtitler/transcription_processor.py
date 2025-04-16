import os
from . import FileUtility


class TranscriptionProcessor:
    def __init__(self, whisper_model, output_dir=None):
        self.whisper_model = whisper_model
        self.output_dir = output_dir

    def transcribe_segments(self, segments):
        transcriptions = []
        cumulative_time = 0.0
        for segment in segments:
            result = self.whisper_model(segment)
            current_segment = []

            # determine where to save this segment's JSON
            if self.output_dir:
                stem = os.path.basename(segment)
                json_name = stem + ".json"
                segment_path = os.path.join(self.output_dir, json_name)
                os.makedirs(os.path.dirname(segment_path), exist_ok=True)
            else:
                segment_path = f"{segment}.json"

            for chunk in result['segments']:
                if chunk.get('start') is None or chunk.get('end') is None:
                    continue
                start = round(chunk['start'] + cumulative_time, 2)
                end = round(chunk['end'] + cumulative_time, 2)
                current_segment.append({'text': chunk['text'], 'timestamp': (start, end)})

            if current_segment:
                cumulative_time = current_segment[-1]['timestamp'][1]

            transcriptions.extend(current_segment)
            FileUtility.save_chunks_to_json(current_segment, filename=segment_path)

        return transcriptions
