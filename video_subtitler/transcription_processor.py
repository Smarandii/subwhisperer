from . import FileUtility


class TranscriptionProcessor:
    def __init__(self, whisper_model):
        self.whisper_model = whisper_model

    def transcribe_segments(self, segments):
        transcriptions = []
        cumulative_time = 0
        for segment in segments:
            result = self.whisper_model(segment)
            current_segment = []
            segment_path = f"{segment}.json"
            for chunk in result['segments']:
                if chunk['start'] is None or chunk['end'] is None:
                    continue
                adjusted_start_time = round(chunk['start'] + cumulative_time, 2)
                adjusted_end_time = round(chunk['end'] + cumulative_time, 2)
                adjusted_chunk = {'text': chunk['text'], 'timestamp': (adjusted_start_time, adjusted_end_time)}
                current_segment.append(adjusted_chunk)
            if current_segment:
                cumulative_time = current_segment[-1]['timestamp'][1]
            transcriptions.extend(current_segment)
            FileUtility.save_chunks_to_json(current_segment, filename=segment_path)
        return transcriptions
