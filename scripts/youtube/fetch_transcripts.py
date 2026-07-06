import json
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

videos_dir = Path("data/raw/youtube/videos")
output_root = Path("research/youtube-transcripts")

output_root.mkdir(parents=True, exist_ok=True)

video_files = list(videos_dir.glob("*_videos.json"))

print(f"Found {len(video_files)} video collections.\n")

for video_file in video_files:

    expert_name = video_file.stem.replace("_videos", "")
    expert_folder = output_root / expert_name
    expert_folder.mkdir(parents=True, exist_ok=True)

    with open(video_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data.get("items", [])

    print(f"{expert_name}: {len(items)} videos")

    for i, item in enumerate(items[:3], start=1):

        try:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]

            transcript = YouTubeTranscriptApi.get_transcript(video_id)

            filename = expert_folder / f"{i:02d}.md"

            with open(filename, "w", encoding="utf-8") as out:

                out.write(f"# {title}\n\n")
                out.write(f"Video ID: {video_id}\n\n")
                out.write("---\n\n")

                for line in transcript:
                    out.write(line["text"] + "\n")

            print(f"  ✓ {title}")

        except Exception as e:
            print(f"  ✗ {item['snippet']['title']}")
            print(f"    {e}")

print("\nFinished.")