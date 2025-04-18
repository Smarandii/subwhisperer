from pathlib import Path
from subwhisperer.cli import process_video

if __name__ == "__main__":
    process_video(Path("test.mp4").absolute())
