"""Shared paths and constants for the data pipeline."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
METADATA = DATA / "metadata"
REPORTS = ROOT / "research"

PLATFORM_CANONICAL = {
    "shopee": "Shopee",
    "tokopedia": "Tokopedia",
    "lazada": "Lazada",
    "bukalapak": "Bukalapak",
    "blibli": "Blibli",
    "tiktok shop": "TikTok Shop",
    "tiktokshop": "TikTok Shop",
    "tokopedia + tiktok shop": "Tokopedia + TikTok Shop",
    "tokopedia+tiktok shop": "Tokopedia + TikTok Shop",
    "goto": "GoTo",
    "gojek": "Gojek",
}
