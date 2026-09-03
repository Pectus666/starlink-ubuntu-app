from __future__ import annotations

import json
from pathlib import Path
from typing import Any

APP_NAME = "starlink-ubuntu-app"
CONFIG_DIR = Path.home() / ".config" / APP_NAME
STATE_DIR = Path.home() / ".local" / "state" / APP_NAME
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG: dict[str, Any] = {
    "subscription": "Residential",
    "billing_email": "",
    "wifi_ssid": "Starlink",
    "wifi_password": "",
    "bypass_mode": False,
    "last_firmware_action": "",
}


def ensure_dirs() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict[str, Any]:
    ensure_dirs()
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)

    data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    merged = dict(DEFAULT_CONFIG)
    merged.update(data)
    return merged


def save_config(config: dict[str, Any]) -> None:
    ensure_dirs()
    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")
