import json


class FileUtility:
    @staticmethod
    def save_chunks_to_json(chunks, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_chunks_from_json(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def format_srt_timestamp(seconds):
        hrs, remainder = divmod(seconds, 3600)
        mins, secs = divmod(remainder, 60)
        millis = int((secs - int(secs)) * 1000)
        return f"{int(hrs):02}:{int(mins):02}:{int(secs):02},{millis:03}"

    @staticmethod
    def generate_srt_file(chunks, output_filename="output.srt"):
        with open(output_filename, "w", encoding="utf-8") as file:
            for i, chunk in enumerate(chunks, start=1):
                start_time = FileUtility.format_srt_timestamp(chunk['timestamp'][0])
                # Adjust the end time to match the start of the next chunk or keep as is if last chunk
                if i < len(chunks):
                    next_start_time = chunks[i]['timestamp'][0]
                    # Only adjust if next subtitle starts after the current ends
                    if next_start_time > chunk['timestamp'][1]:
                        end_time = FileUtility.format_srt_timestamp(next_start_time)
                    else:
                        end_time = FileUtility.format_srt_timestamp(chunk['timestamp'][1])
                else:
                    end_time = FileUtility.format_srt_timestamp(chunk['timestamp'][1])

                text = chunk['text']
                file.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")
