import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found.")

ROOT = Path(".")

DATA = ROOT / "data"

RAW = DATA / "raw"

YOUTUBE = RAW / "youtube"

CHANNELS = YOUTUBE / "channels"

VIDEOS = YOUTUBE / "videos"

TRANSCRIPTS = RAW / "transcripts"

CHANNELS.mkdir(parents=True, exist_ok=True)
VIDEOS.mkdir(parents=True, exist_ok=True)
TRANSCRIPTS.mkdir(parents=True, exist_ok=True)