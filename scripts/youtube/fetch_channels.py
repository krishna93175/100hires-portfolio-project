import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found.")

experts = [
    ("Ross Simmonds", "Foundation Marketing"),
    ("Rand Fishkin", "SparkToro"),
    ("Bernard Huang", "Clearscope"),
    ("Nathan Gotch", "Gotch SEO"),
    ("Matt Diggity", "Diggity Marketing"),
    ("Lily Ray", "Amsive"),
    ("Aleyda Solis", "Orainti"),
    ("Wil Reynolds", "Seer Interactive"),
    ("Marie Haynes", "Marie Haynes Consulting"),
    ("Julian Goldie", "Goldie Agency")
]

output_dir = Path("data/raw/youtube/channels")
output_dir.mkdir(parents=True, exist_ok=True)

for name, company in experts:

    query = f"{name} {company}"

    print(f"\nSearching: {query}")

    response = requests.get(
        "https://www.googleapis.com/youtube/v3/search",
        params={
            "part": "snippet",
            "q": query,
            "type": "channel",
            "maxResults": 1,
            "key": API_KEY
        }
    )

    print("Status Code:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        continue

    data = response.json()

    filename = name.lower().replace(" ", "_") + ".json"

    with open(output_dir / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Saved:", filename)

print("\nFinished.")