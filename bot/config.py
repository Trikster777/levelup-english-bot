from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def load_dotenv(dotenv_path: str = ".env") -> None:
    path = Path(dotenv_path)
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


@dataclass(slots=True)
class Settings:
    telegram_bot_token: str
    database_path: str
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"


def get_settings() -> Settings:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    return Settings(
        telegram_bot_token=token,
        database_path=os.getenv("DATABASE_PATH", "data/levelup.sqlite3"),
        openai_api_key=os.getenv("OPENAI_API_KEY") or None,
        gemini_api_key=os.getenv("GEMINI_API_KEY") or None,
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    )
