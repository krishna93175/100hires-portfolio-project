import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found.")

channels_dir = Path("data/raw/youtube/channels")
videos_dir = Path("data/raw/youtube/videos")

videos_dir.mkdir(parents=True, exist_ok=True)

channel_files = list(channels_dir.glob("*.json"))

print(f"Found {len(channel_files)} channel file(s).\n")

for channel_file in channel_files:

    print(f"Processing {channel_file.name}")

    with open(channel_file, "r", encoding="utf-8") as f:
        channel_data = json.load(f)

    if not channel_data.get("items"):
        print("No channel found.\n")
        continue

    channel_id = channel_data["items"][0]["id"]["channelId"]

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "channelId": channel_id,
        "order": "date",
        "type": "video",
        "maxResults": 20,
        "key": API_KEY
    }

    response = requests.get(url, params=params)

    print("Status:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        continue

    video_data = response.json()

    output_name = channel_file.stem + "_videos.json"

    with open(videos_dir / output_name, "w", encoding="utf-8") as outfile:
        json.dump(video_data, outfile, indent=4)

    print(f"Saved {output_name}\n")

print("Finished.")