import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in .env")

# Load experts
with open("config/experts.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Output folder
output_dir = Path("data/raw/youtube")
output_dir.mkdir(parents=True, exist_ok=True)

for expert in config["experts"]:

    query = f"{expert['name']} {expert['company']}"

    print(f"\nSearching: {query}")

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "channel",
        "maxResults": 1,
        "key": API_KEY
    }

    response = requests.get(url, params=params)

    print("Status Code:", response.status_code)

    data = response.json()

    filename = expert["name"].lower().replace(" ", "_") + ".json"

    with open(output_dir / filename, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4)

    print("Saved:", filename)

print("\nDone.")