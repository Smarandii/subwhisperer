import whisper
import torch

# Determine the device to use (GPU if available, otherwise CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cuda":
    print("CUDA is available. Running on GPU.")
else:
    print("CUDA is not available. Running on CPU.")

# Load a higher-quality model (for example, "medium" or "large")
model = whisper.load_model("large", device="cuda")

# Transcribe the audio file
result = model.transcribe("output.mp3")
transcription = result["text"]

# Print the transcription
print(transcription)

# Save the transcription to a file
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(transcription)
