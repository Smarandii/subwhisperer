import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


class WhisperTranscriber:
    def __init__(self):

        # Determine the device to use (GPU if available, otherwise CPU)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if device == "cuda":
            print("CUDA is available. Running on GPU.")
        else:
            print("CUDA is not available. Running on CPU.")

        self.device = device

        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model_id = "openai/whisper-large-v3"
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_id, torch_dtype=self.torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        ).to(self.device)
        self.processor = AutoProcessor.from_pretrained(self.model_id)

    def get_whisper_pipe(self):
        return pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps="word",
            torch_dtype=self.torch_dtype,
            device=self.device,
        )


if __name__ == "__main__":
    audio_file = "test.mp3"
    whisper_transcriber = WhisperTranscriber()
    whisper_pipe = whisper_transcriber.get_whisper_pipe()
    result = whisper_pipe(audio_file)
    print(result)
