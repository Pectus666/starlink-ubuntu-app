from __future__ import annotations

import logging
from pathlib import Path

from .config import STATE_DIR, ensure_dirs

LOG_FILE = STATE_DIR / "app.log"


def setup_logging() -> Path:
    ensure_dirs()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    return LOG_FILE
