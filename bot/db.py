from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    telegram_user_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    xp INTEGER NOT NULL DEFAULT 0,
    streak_days INTEGER NOT NULL DEFAULT 0,
    last_active_date TEXT,
    current_chapter_id TEXT NOT NULL DEFAULT 'daily_routine',
    estimated_level TEXT NOT NULL DEFAULT 'unknown',
    placement_completed INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mission_progress (
    telegram_user_id INTEGER NOT NULL,
    mission_id TEXT NOT NULL,
    is_completed INTEGER NOT NULL DEFAULT 0,
    best_score INTEGER NOT NULL DEFAULT 0,
    completed_at TEXT,
    PRIMARY KEY (telegram_user_id, mission_id)
);

CREATE TABLE IF NOT EXISTS boss_progress (
    telegram_user_id INTEGER NOT NULL,
    boss_id TEXT NOT NULL,
    is_completed INTEGER NOT NULL DEFAULT 0,
    best_score INTEGER NOT NULL DEFAULT 0,
    completed_at TEXT,
    PRIMARY KEY (telegram_user_id, boss_id)
);

CREATE TABLE IF NOT EXISTS review_queue (
    telegram_user_id INTEGER NOT NULL,
    task_id TEXT NOT NULL,
    source_type TEXT NOT NULL,
    wrong_answers INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (telegram_user_id, task_id)
);
"""


def _ensure_column(connection: sqlite3.Connection, table_name: str, column_name: str, column_def: str) -> None:
    columns = {
        row["name"]
        for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    }
    if column_name in columns:
        return
    connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_def}")


def create_connection(database_path: str) -> sqlite3.Connection:
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    _ensure_column(connection, "users", "estimated_level", "TEXT NOT NULL DEFAULT 'unknown'")
    _ensure_column(connection, "users", "placement_completed", "INTEGER NOT NULL DEFAULT 0")
    connection.commit()
    return connection
