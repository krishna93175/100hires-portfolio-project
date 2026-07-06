import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load API Key
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found.")

# Read channel information
channel_file = Path("data/raw/youtube/ross_simmonds.json")

with open(channel_file, "r", encoding="utf-8") as f:
    channel_data = json.load(f)

channel_id = channel_data["items"][0]["id"]["channelId"]

print(f"Channel ID: {channel_id}")

# Search latest videos
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

print("Status Code:", response.status_code)

if response.status_code != 200:
    print(response.text)
    exit()

video_data = response.json()

# Create output folder
output_folder = Path("data/raw/youtube/videos")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "ross_simmonds_videos.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(video_data, f, indent=4)

print(f"Saved to {output_file}")