
import subprocess
from pathlib import Path

SCENES_DIR = Path("assets/scenes")
AUDIO = Path("assets/narration.mp3")
OUTPUT_DIR = Path("output")
TEMP_DIR = Path("temp")

OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

OUTPUT = OUTPUT_DIR / "kickyplaytube_short.mp4"

def run(command):
    subprocess.run(command, check=True)

def main():
    scenes = sorted(
        p for p in SCENES_DIR.glob("*")
        if p.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
    )

    if not scenes:
        raise RuntimeError(
            "No images found. Add images to assets/scenes/"
        )

    if not AUDIO.exists():
        raise RuntimeError(
            "Narration missing. Add assets/narration.mp3"
        )

    clips = []

    print(f"Found {len(scenes)} scenes.")

    for index, scene in enumerate(scenes):
        clip = TEMP_DIR / f"scene_{index:03d}.mp4"

        command = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-framerate", "30",
            "-i", str(scene),
            "-t", "5",
            "-vf",
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            "zoompan=z='min(zoom+0.001,1.08)':"
            "d=150:s=1080x1920:fps=30,"
            "format=yuv420p",
            "-frames:v", "150",
            "-an",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            str(clip)
        ]

        run(command)
        clips.append(clip)

        print(f"Created scene {index + 1}")

    playlist = TEMP_DIR / "playlist.txt"

    with playlist.open("w") as file:
        for clip in clips:
            file.write(f"file '{clip.resolve()}'\n")

    slideshow = TEMP_DIR / "slideshow.mp4"

    run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(playlist),
        "-c", "copy",
        str(slideshow)
    ])

    # Loop the slideshow until narration finishes
    run([
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", str(slideshow),
        "-i", str(AUDIO),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(OUTPUT)
    ])

    print("\nSUCCESS!")
    print(f"Your video is ready: {OUTPUT}")

if __name__ == "__main__":
    main()
