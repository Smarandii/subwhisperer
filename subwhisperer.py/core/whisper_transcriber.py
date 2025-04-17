import torch
import whisper


class WhisperTranscriber:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cuda":
            print("CUDA is available. Running on GPU.")
        else:
            print("CUDA is not available. Running on CPU.")
        # Load the Whisper model directly (using the OpenAI Whisper package)
        self.model = whisper.load_model("large", device=self.device)

    def transcribe(self, audio_file):
        # Transcribe with word-level timestamps enabled
        return self.model.transcribe(audio_file, word_timestamps=True)


if __name__ == "__main__":
    audio_file = "test.mp3"
    wt = WhisperTranscriber()
    result = wt.transcribe(audio_file)
    print(result)