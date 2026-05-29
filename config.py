import json
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent
_CONFIG_PATH = _PROJECT_ROOT / "config.json"


def load_config():
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)