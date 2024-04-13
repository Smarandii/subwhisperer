class TextMerger:
    def __init__(self, max_length=76, threshold=6):
        self.max_length = max_length
        self.threshold = threshold

    @staticmethod
    def should_start_new_group(current_group):
        """Determines if a new group should start based on punctuation."""
        return current_group[-1]['text'].strip().endswith(('.', '!', '?'))

    @staticmethod
    def should_merge_without_space(last_text, next_text):
        """Determines if space should be skipped when merging texts."""
        return last_text.endswith('-') or next_text.startswith('-')

    def split_text_properly(self, text):
        """Splits text based on punctuation or by half, ensuring each part does not exceed the maximum length."""
        if len(text) <= self.max_length:
            return [text]

        punctuations = '.;:!?'
        best_pos = max((pos for pos in (text.rfind(punct, 0, self.max_length) for punct in punctuations) if pos != -1),
                       default=None)

        if best_pos and best_pos + 1 < len(text):
            return [text[:best_pos + 1].strip(), text[best_pos + 1:].strip()]

        words = text.split()
        mid_point = len(words) // 2
        return [' '.join(words[:mid_point]).strip(), ' '.join(words[mid_point:]).strip()]

    def add_group_to_merged_chunks(self, merged_chunks, current_group, group_start_time, group_end_time):
        merged_text = " ".join(c['text'].strip() for c in current_group)
        if len(merged_text) > self.max_length:
            split_texts = self.split_text_properly(merged_text)
            total_length = len(merged_text)
            cumulative_start_time = group_start_time

            for i, text in enumerate(split_texts):
                portion_length = len(text)
                if i < len(split_texts) - 1:  # Not the last item
                    portion_duration = (portion_length / total_length) * (group_end_time - group_start_time)
                    chunk_end_time = cumulative_start_time + portion_duration
                else:
                    chunk_end_time = group_end_time  # Last item takes the remainder

                merged_chunks.append({'text': text, 'timestamp': (cumulative_start_time, chunk_end_time)})
                cumulative_start_time = chunk_end_time  # Next chunk starts where the last one ended
        else:
            merged_chunks.append({'text': merged_text, 'timestamp': (group_start_time, group_end_time)})

    def merge_chunks(self, chunks):
        """Merges chunks into groups based on the total duration threshold and text length."""
        merged_chunks = []
        current_group = []
        group_start_time = None
        group_end_time = None

        for chunk in chunks:
            if chunk['timestamp'][0] is None or chunk['timestamp'][1] is None:
                continue

            if not current_group or self.should_start_new_group(current_group):
                if current_group:
                    self.add_group_to_merged_chunks(merged_chunks, current_group, group_start_time, group_end_time)
                current_group = [chunk]
                group_start_time = chunk['timestamp'][0]
                group_end_time = chunk['timestamp'][1]
            else:
                potential_end_time = chunk['timestamp'][1]
                group_duration = potential_end_time - group_start_time

                if group_duration <= self.threshold:
                    if current_group and self.should_merge_without_space(current_group[-1]['text'], chunk['text']):
                        current_group[-1]['text'] += chunk['text'].strip()
                    else:
                        current_group.append(chunk)
                    group_end_time = potential_end_time
                else:
                    self.add_group_to_merged_chunks(merged_chunks, current_group, group_start_time, group_end_time)
                    current_group = [chunk]
                    group_start_time = chunk['timestamp'][0]
                    group_end_time = chunk['timestamp'][1]

        if current_group:
            self.add_group_to_merged_chunks(merged_chunks, current_group, group_start_time, group_end_time)

        return merged_chunks
