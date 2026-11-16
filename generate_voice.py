
import subprocess
from pathlib import Path

STORY = Path("story.txt")
ASSETS = Path("assets")
OUTPUT = ASSETS / "narration.wav"

def main():
    if not STORY.exists():
        raise FileNotFoundError("story.txt not found")

    text = STORY.read_text(encoding="utf-8").strip()

    if not text:
        raise ValueError("Story file is empty")

    ASSETS.mkdir(parents=True, exist_ok=True)

    print("Generating AI narration...")

    subprocess.run(
        [
            "piper",
            "--model", "en_US-lessac-medium",
            "--output_file", str(OUTPUT)
        ],
        input=text,
        text=True,
        check=True
    )

    print("Voice generation successful!")
    print(f"Audio saved to: {OUTPUT}")

if __name__ == "__main__":
    main()
  
