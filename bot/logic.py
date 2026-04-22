from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date, datetime
from html import escape

from .content import CHAPTERS, Boss, Chapter, Mission, Task, get_chapter, get_next_chapter_after, get_placement_tasks, iter_all_tasks


@dataclass(slots=True)
class SessionState:
    mode: str
    chapter_id: str
    content_id: str
    task_index: int = 0
    correct_answers: int = 0


def ensure_user(connection: sqlite3.Connection, telegram_user_id: int, first_name: str) -> None:
    connection.execute(
        """
        INSERT INTO users (telegram_user_id, first_name)
        VALUES (?, ?)
        ON CONFLICT(telegram_user_id) DO UPDATE SET first_name = excluded.first_name
        """,
        (telegram_user_id, first_name),
    )
    connection.commit()


def update_streak(connection: sqlite3.Connection, telegram_user_id: int) -> None:
    row = connection.execute(
        "SELECT streak_days, last_active_date FROM users WHERE telegram_user_id = ?",
        (telegram_user_id,),
    ).fetchone()
    if row is None:
        return

    today = date.today()
    last_active_raw = row["last_active_date"]
    streak = int(row["streak_days"])

    if not last_active_raw:
        new_streak = 1
    else:
        last_active = date.fromisoformat(last_active_raw)
        delta = (today - last_active).days
        if delta == 0:
            return
        new_streak = streak + 1 if delta == 1 else 1

    connection.execute(
        "UPDATE users SET streak_days = ?, last_active_date = ? WHERE telegram_user_id = ?",
        (new_streak, today.isoformat(), telegram_user_id),
    )
    connection.commit()


def get_user_profile(connection: sqlite3.Connection, telegram_user_id: int) -> sqlite3.Row | None:
    return connection.execute(
        "SELECT * FROM users WHERE telegram_user_id = ?",
        (telegram_user_id,),
    ).fetchone()


def get_user_level(connection: sqlite3.Connection, telegram_user_id: int) -> str:
    row = get_user_profile(connection, telegram_user_id)
    if row is None:
        return "A2"
    return row["estimated_level"] or "A2"


def is_placement_completed(connection: sqlite3.Connection, telegram_user_id: int) -> bool:
    row = get_user_profile(connection, telegram_user_id)
    return bool(row and row["placement_completed"])


def complete_placement(connection: sqlite3.Connection, telegram_user_id: int, correct_answers: int) -> str:
    if correct_answers <= 3:
        level = "A1-A2"
    elif correct_answers <= 6:
        level = "A2"
    elif correct_answers <= 8:
        level = "A2+"
    else:
        level = "A2-B1"

    connection.execute(
        """
        UPDATE users
        SET placement_completed = 1,
            estimated_level = ?
        WHERE telegram_user_id = ?
        """,
        (level, telegram_user_id),
    )
    connection.commit()
    return level


def apply_level_routing(connection: sqlite3.Connection, telegram_user_id: int, level: str) -> None:
    skipped_missions: list[str] = []

    if level == "A2+":
        skipped_missions = ["routine_words"]
    elif level == "A2-B1":
        skipped_missions = ["routine_words", "present_simple"]

    if not skipped_missions:
        return

    for mission_id in skipped_missions:
        connection.execute(
            """
            INSERT INTO mission_progress (telegram_user_id, mission_id, is_completed, best_score, completed_at)
            VALUES (?, ?, 1, 100, ?)
            ON CONFLICT(telegram_user_id, mission_id) DO UPDATE SET
                is_completed = 1,
                best_score = MAX(best_score, excluded.best_score),
                completed_at = excluded.completed_at
            """,
            (telegram_user_id, mission_id, datetime.utcnow().isoformat()),
        )

    connection.commit()


def reset_learning_progress(connection: sqlite3.Connection, telegram_user_id: int) -> None:
    connection.execute("DELETE FROM mission_progress WHERE telegram_user_id = ?", (telegram_user_id,))
    connection.execute("DELETE FROM boss_progress WHERE telegram_user_id = ?", (telegram_user_id,))
    connection.execute("DELETE FROM review_queue WHERE telegram_user_id = ?", (telegram_user_id,))
    connection.execute(
        """
        UPDATE users
        SET xp = 0,
            current_chapter_id = 'daily_routine'
        WHERE telegram_user_id = ?
        """,
        (telegram_user_id,),
    )
    connection.commit()


def get_rank(xp: int) -> str:
    if xp < 60:
        return "Rookie"
    if xp < 140:
        return "Explorer"
    if xp < 260:
        return "Challenger"
    if xp < 420:
        return "Fighter"
    return "B1 Runner"


def progress_bar(done: int, total: int, length: int = 6) -> str:
    if total <= 0:
        return "░" * length
    filled = round(done / total * length)
    filled = max(0, min(length, filled))
    return "█" * filled + "░" * (length - filled)


def get_current_chapter(connection: sqlite3.Connection, telegram_user_id: int) -> Chapter:
    profile = get_user_profile(connection, telegram_user_id)
    chapter_id = profile["current_chapter_id"] if profile else CHAPTERS[0].id
    return get_chapter(chapter_id)


def is_mission_completed(connection: sqlite3.Connection, telegram_user_id: int, mission_id: str) -> bool:
    row = connection.execute(
        """
        SELECT is_completed FROM mission_progress
        WHERE telegram_user_id = ? AND mission_id = ?
        """,
        (telegram_user_id, mission_id),
    ).fetchone()
    return bool(row and row["is_completed"])


def get_next_mission(connection: sqlite3.Connection, telegram_user_id: int) -> Mission | None:
    chapter = get_current_chapter(connection, telegram_user_id)
    for mission in chapter.missions:
        if not is_mission_completed(connection, telegram_user_id, mission.id):
            return mission
    return None


def is_boss_unlocked(connection: sqlite3.Connection, telegram_user_id: int, chapter_id: str) -> bool:
    chapter = get_chapter(chapter_id)
    return all(is_mission_completed(connection, telegram_user_id, mission.id) for mission in chapter.missions)


def is_boss_completed(connection: sqlite3.Connection, telegram_user_id: int, boss_id: str) -> bool:
    row = connection.execute(
        """
        SELECT is_completed FROM boss_progress
        WHERE telegram_user_id = ? AND boss_id = ?
        """,
        (telegram_user_id, boss_id),
    ).fetchone()
    return bool(row and row["is_completed"])


def complete_mission(connection: sqlite3.Connection, telegram_user_id: int, mission: Mission, correct_answers: int) -> None:
    score = round(correct_answers / len(mission.tasks) * 100)
    connection.execute(
        """
        INSERT INTO mission_progress (telegram_user_id, mission_id, is_completed, best_score, completed_at)
        VALUES (?, ?, 1, ?, ?)
        ON CONFLICT(telegram_user_id, mission_id) DO UPDATE SET
            is_completed = 1,
            best_score = MAX(best_score, excluded.best_score),
            completed_at = excluded.completed_at
        """,
        (telegram_user_id, mission.id, score, datetime.utcnow().isoformat()),
    )
    add_xp(connection, telegram_user_id, mission.xp_reward)
    connection.commit()


def complete_boss(
    connection: sqlite3.Connection,
    telegram_user_id: int,
    chapter_id: str,
    boss: Boss,
    correct_answers: int,
) -> Chapter | None:
    score = round(correct_answers / len(boss.tasks) * 100)
    connection.execute(
        """
        INSERT INTO boss_progress (telegram_user_id, boss_id, is_completed, best_score, completed_at)
        VALUES (?, ?, 1, ?, ?)
        ON CONFLICT(telegram_user_id, boss_id) DO UPDATE SET
            is_completed = 1,
            best_score = MAX(best_score, excluded.best_score),
            completed_at = excluded.completed_at
        """,
        (telegram_user_id, boss.id, score, datetime.utcnow().isoformat()),
    )
    add_xp(connection, telegram_user_id, boss.xp_reward)
    next_chapter = get_next_chapter_after(chapter_id)
    if next_chapter is not None:
        connection.execute(
            "UPDATE users SET current_chapter_id = ? WHERE telegram_user_id = ?",
            (next_chapter.id, telegram_user_id),
        )
    connection.commit()
    return next_chapter


def add_review_item(connection: sqlite3.Connection, telegram_user_id: int, task: Task, source_type: str) -> None:
    connection.execute(
        """
        INSERT INTO review_queue (telegram_user_id, task_id, source_type, wrong_answers)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(telegram_user_id, task_id) DO UPDATE SET
            wrong_answers = wrong_answers + 1
        """,
        (telegram_user_id, task.id, source_type),
    )
    connection.commit()


def remove_review_item(connection: sqlite3.Connection, telegram_user_id: int, task_id: str) -> None:
    connection.execute(
        "DELETE FROM review_queue WHERE telegram_user_id = ? AND task_id = ?",
        (telegram_user_id, task_id),
    )
    connection.commit()


def get_review_tasks(connection: sqlite3.Connection, telegram_user_id: int) -> list[Task]:
    rows = connection.execute(
        """
        SELECT task_id FROM review_queue
        WHERE telegram_user_id = ?
        ORDER BY wrong_answers DESC, task_id ASC
        """,
        (telegram_user_id,),
    ).fetchall()

    tasks_by_id = {task.id: task for task in iter_all_tasks()}

    return [tasks_by_id[row["task_id"]] for row in rows if row["task_id"] in tasks_by_id]


def has_review_tasks(connection: sqlite3.Connection, telegram_user_id: int) -> bool:
    row = connection.execute(
        "SELECT 1 FROM review_queue WHERE telegram_user_id = ? LIMIT 1",
        (telegram_user_id,),
    ).fetchone()
    return row is not None


def get_review_count(connection: sqlite3.Connection, telegram_user_id: int) -> int:
    row = connection.execute(
        "SELECT COUNT(*) AS total FROM review_queue WHERE telegram_user_id = ?",
        (telegram_user_id,),
    ).fetchone()
    return int(row["total"]) if row else 0


def add_xp(connection: sqlite3.Connection, telegram_user_id: int, xp: int) -> None:
    connection.execute(
        "UPDATE users SET xp = xp + ? WHERE telegram_user_id = ?",
        (xp, telegram_user_id),
    )


def get_profile_text(connection: sqlite3.Connection, telegram_user_id: int) -> str:
    profile = get_user_profile(connection, telegram_user_id)
    if profile is None:
        return "<b>Профиль еще не создан</b>\n\nНажми /start, чтобы начать."

    xp = int(profile["xp"])
    chapter = get_current_chapter(connection, telegram_user_id)
    completed = sum(1 for mission in chapter.missions if is_mission_completed(connection, telegram_user_id, mission.id))
    review_count = get_review_count(connection, telegram_user_id)

    placement_state = "пройден" if profile["placement_completed"] else "не пройден"

    return "\n".join(
        [
            "<b>Профиль</b>",
            f"<b>Игрок:</b> {profile['first_name']}",
            f"<b>Уровень:</b> {profile['estimated_level']}",
            f"<b>Ранг:</b> {get_rank(xp)}",
            f"<b>XP:</b> {xp}",
            f"<b>Серия:</b> {profile['streak_days']} дн.",
            "",
            f"<b>Глава:</b> {chapter.title}",
            f"<b>Прогресс:</b> {progress_bar(completed, len(chapter.missions))} {completed}/{len(chapter.missions)}",
            f"<b>Реванш:</b> {review_count} карточек",
            f"<b>Стартовый тест:</b> {placement_state}",
        ]
    )


def get_chapter_summary(connection: sqlite3.Connection, telegram_user_id: int) -> str:
    chapter = get_current_chapter(connection, telegram_user_id)
    completed = sum(1 for mission in chapter.missions if is_mission_completed(connection, telegram_user_id, mission.id))
    total = len(chapter.missions)

    if is_boss_completed(connection, telegram_user_id, chapter.boss.id):
        boss_state = "пройден"
    elif completed == total and has_review_tasks(connection, telegram_user_id):
        boss_state = "ждет добивку ошибок"
    elif completed == total:
        boss_state = "открыт"
    else:
        boss_state = "закрыт"

    return "\n".join(
        [
            f"<b>{chapter.title}</b>",
            chapter.description,
            "",
            f"<b>Прогресс по миссиям:</b> {progress_bar(completed, total)} {completed}/{total}",
            f"<b>Босс:</b> {boss_state}",
        ]
    )


def get_task_prompt(task: Task, position: int, total: int, heading: str) -> str:
    option_marks = ("A", "B", "C", "D", "E", "F")
    option_lines = [f"<b>{option_marks[idx]}.</b> {escape(option)}" for idx, option in enumerate(task.options)]
    return "\n".join([f"<b>{heading}</b>", f"<b>Задание {position}/{total}</b>", "", task.prompt, "", *option_lines])


def build_mission_intro(mission: Mission) -> str:
    return "\n".join(
        [
            f"<b>{mission.title}</b>",
            mission.description,
            "",
            f"<b>Награда:</b> {mission.xp_reward} XP",
            f"<b>Заданий:</b> {len(mission.tasks)}",
        ]
    )


def build_boss_intro(boss: Boss) -> str:
    return "\n".join(
        [
            f"<b>{boss.title}</b>",
            boss.description,
            "",
            f"<b>Награда:</b> {boss.xp_reward} XP",
            f"<b>Заданий:</b> {len(boss.tasks)}",
        ]
    )


def build_placement_intro() -> str:
    return "\n".join(
        [
            "<b>Стартовый тест</b>",
            "Сейчас спокойно поймем, с какой точки тебе лучше стартовать.",
            "Тут 10 вопросов, так что получится нормальный срез, а не угадайка на скорую руку.",
        ]
    )


def build_feedback(is_correct: bool, task: Task) -> str:
    if is_correct:
        return "<b>Норм.</b>\n\nИдем дальше без спешки."
    return f"<b>Не засчитано.</b>\n\n{explanation}"


def build_feedback_detailed(is_correct: bool, task: Task) -> str:
    if is_correct:
        return build_feedback(True, task)

    correct_answer = task.options[task.correct_index]
    return "\n".join(
        [
            "<b>Не засчитано.</b>",
            "",
            f"<b>Правильный вариант:</b> {correct_answer}",
            "",
            f"<b>Почему так:</b> {task.explanation}",
            "",
            "Запомни этот ход и поехали дальше.",
        ]
    )


def build_mission_success_feedback(task: Task) -> str:
    correct_answer = task.options[task.correct_index]
    return "\n".join(
        [
            "<b>Засчитано.</b>",
            "",
            f"<b>Правильный вариант:</b> {correct_answer}",
            "",
            "Всё, молодец. Двигаемся дальше.",
        ]
    )


def build_mission_feedback(is_correct: bool, task: Task) -> str:
    if is_correct:
        return build_mission_success_feedback(task)
    return build_feedback_detailed(False, task)


def build_checkpoint_feedback(is_correct: bool, task: Task) -> str | None:
    if is_correct:
        return None
    return build_feedback_detailed(False, task)


def build_mission_result(correct_answers: int, total: int, xp_reward: int) -> str:
    return "\n".join(
        [
            "<b>Миссия закрыта</b>",
            f"<b>Результат:</b> {correct_answers}/{total}",
            f"<b>Награда:</b> +{xp_reward} XP",
            "Нормальный проход. Можно двигаться дальше.",
        ]
    )


def build_boss_result(correct_answers: int, total: int, xp_reward: int) -> str:
    return "\n".join(
        [
            "<b>Босс закрыт</b>",
            f"<b>Результат:</b> {correct_answers}/{total}",
            f"<b>Награда:</b> +{xp_reward} XP",
            "Уже видно, что база начинает держаться.",
        ]
    )


def build_placement_result(correct_answers: int, total: int, level: str) -> str:
    return "\n".join(
        [
            "<b>Стартовый тест завершен</b>",
            f"<b>Результат:</b> {correct_answers}/{total}",
            f"<b>Стартовый уровень:</b> {level}",
            "Теперь у нас есть внятная точка старта.",
        ]
    )


def build_next_mission_text(mission: Mission) -> str:
    return "<b>Следующая миссия открыта</b>\n\n" + build_mission_intro(mission)


def build_chapter_complete_text(summary: str) -> str:
    return "<b>Миссии главы закрыты</b>\n\n" + summary


def build_mission_result_detailed(correct_answers: int, total: int, xp_reward: int) -> str:
    accuracy = round(correct_answers / total * 100) if total else 0
    return "\n".join(
        [
            "<b>Миссия закрыта</b>",
            f"<b>Результат:</b> {correct_answers}/{total}",
            f"<b>Точность:</b> {accuracy}%",
            f"<b>Награда:</b> +{xp_reward} XP",
            "Если где-то просело, это нормально: слабые места уже можно добить реваншем.",
        ]
    )


def get_placement_items() -> tuple[Task, ...]:
    return get_placement_tasks()
