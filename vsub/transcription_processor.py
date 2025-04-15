from vsub.file_utility import FileUtility


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
            for chunk in result['chunks']:
                if chunk['timestamp'][0] is None or chunk['timestamp'][1] is None:
                    continue
                adjusted_start_time = round(chunk['timestamp'][0] + cumulative_time, 2)
                adjusted_end_time = round(chunk['timestamp'][1] + cumulative_time, 2)
                adjusted_chunk = {'text': chunk['text'], 'timestamp': (adjusted_start_time, adjusted_end_time)}
                current_segment.append(adjusted_chunk)
            if current_segment:
                cumulative_time = current_segment[-1]['timestamp'][1]
            transcriptions.extend(current_segment)
            FileUtility.save_chunks_to_json(current_segment, filename=segment_path)
        return transcriptions
