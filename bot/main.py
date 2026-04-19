from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from .config import get_settings
from .content import Task, get_boss, get_boss_tasks, get_mission_tasks
from .db import create_connection
from .gemini import GeminiClient, build_summary_prompt, build_tutor_prompt
from .logic import (
    SessionState,
    add_review_item,
    apply_level_routing,
    build_boss_intro,
    build_boss_result,
    build_chapter_complete_text,
    build_checkpoint_feedback,
    build_mission_feedback,
    build_mission_intro,
    build_mission_result_detailed,
    build_next_mission_text,
    build_placement_intro,
    build_placement_result,
    complete_boss,
    complete_mission,
    complete_placement,
    ensure_user,
    get_chapter_summary,
    get_current_chapter,
    get_next_mission,
    get_placement_items,
    get_profile_text,
    get_review_count,
    get_review_tasks,
    get_task_prompt,
    get_user_level,
    has_review_tasks,
    is_boss_completed,
    is_boss_unlocked,
    is_placement_completed,
    remove_review_item,
    reset_learning_progress,
    update_streak,
)


settings = get_settings()
connection = create_connection(settings.database_path)
bot = Bot(token=settings.telegram_bot_token, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
gemini_client = GeminiClient(settings.gemini_api_key, settings.gemini_model) if settings.gemini_api_key else None

session_store: dict[int, SessionState] = {}
review_task_store: dict[int, list[Task]] = {}


async def generate_ai_summary(kind: str, title: str, score_text: str) -> str | None:
    if gemini_client is None:
        return None
    return await asyncio.to_thread(gemini_client.generate_text, build_summary_prompt(kind, score_text, title))


async def ask_tutor(question: str) -> str | None:
    if gemini_client is None:
        return None
    return await asyncio.to_thread(gemini_client.generate_text, build_tutor_prompt(question))


def local_tutor_fallback(question: str) -> str | None:
    q = question.lower().strip()

    if "present simple" in q and "present continuous" in q:
        return (
            "<b>Коротко:</b> Present Simple — это про то, что обычно, регулярно или вообще является фактом. "
            "Present Continuous — про то, что происходит прямо сейчас или временно в этот период.\n\n"
            "Например: <i>I go to school every day.</i> — это привычка, значит Present Simple. "
            "<i>I am doing my homework right now.</i> — это действие прямо сейчас, значит Present Continuous."
        )

    if "do и does" in q or "do and does" in q or ("do" in q and "does" in q and "разниц" in q):
        return (
            "<b>Смотри:</b> <i>do</i> используем с <i>I / you / we / they</i>, а <i>does</i> — с <i>he / she / it</i>.\n\n"
            "То есть: <i>Do you like music?</i> и <i>Does she like music?</i>. "
            "Главная мысль простая: <i>does</i> — это форма для третьего лица в единственном числе."
        )

    if "past simple" in q:
        return (
            "<b>Past Simple</b> нужен, когда говоришь о завершенном действии в прошлом.\n\n"
            "Например: <i>I watched a film yesterday.</i> или <i>She went to school last week.</i>. "
            "Сигналы часто такие: <i>yesterday, last week, ago</i>."
        )

    if "артикл" in q or "a an the" in q or "a / an / the" in q:
        return (
            "<b>Очень грубо так:</b> <i>a / an</i> — когда говорим о чем-то в целом, впервые и не уточняем. "
            "<i>the</i> — когда уже понятно, о чем именно речь.\n\n"
            "Например: <i>I saw a dog.</i> — просто какую-то собаку. "
            "<i>The dog was very big.</i> — уже ту самую собаку."
        )

    if "present simple" in q:
        return (
            "<b>Present Simple</b> — это про привычки, регулярность, факты и расписания.\n\n"
            "Пример: <i>I play football every weekend.</i> "
            "Если коротко: это не про 'прямо сейчас', а про 'обычно'."
        )

    if "present continuous" in q:
        return (
            "<b>Present Continuous</b> — это про действие прямо сейчас или временную ситуацию.\n\n"
            "Пример: <i>I am studying now.</i> "
            "Если коротко: это про 'сейчас' или 'в данный период'."
        )

    return None


def action_keyboard(start_callback: str, text: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=start_callback)]])


def answer_keyboard(task: Task, prefix: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=option[:60], callback_data=f"{prefix}:{idx}")] for idx, option in enumerate(task.options)]
    )


def home_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="На миссию", callback_data="nav:mission"),
                InlineKeyboardButton(text="Профиль", callback_data="nav:profile"),
            ],
            [
                InlineKeyboardButton(text="Финальный чек", callback_data="nav:boss"),
            ],
            [InlineKeyboardButton(text="Сбросить прогресс", callback_data="nav:restart")],
        ]
    )


def mission_complete_keyboard(user_id: int, accuracy: int) -> InlineKeyboardMarkup:
    next_mission = get_next_mission(connection, user_id)
    buttons: list[list[InlineKeyboardButton]] = []

    if next_mission is not None:
        buttons.append([InlineKeyboardButton(text="Следующая миссия", callback_data=f"mission:start:{next_mission.id}")])
    elif has_review_tasks(connection, user_id):
        pending = get_review_count(connection, user_id)
        buttons.append([InlineKeyboardButton(text=f"Разобрать ошибки ({pending})", callback_data="review:start")])
    else:
        buttons.append([InlineKeyboardButton(text="К финальному чеку", callback_data="boss:start")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def bootstrap_user(user_id: int, first_name: str) -> None:
    ensure_user(connection, user_id, first_name or "Player")
    update_streak(connection, user_id)


async def show_start(chat_id: int, user_id: int, first_name: str) -> None:
    bootstrap_user(user_id, first_name)
    if not is_placement_completed(connection, user_id):
        session_store[user_id] = SessionState(mode="placement", chapter_id=get_current_chapter(connection, user_id).id, content_id="placement")
        await bot.send_message(
            chat_id,
            build_placement_intro(),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Запустить тест", callback_data="placement:start")],
                    [InlineKeyboardButton(text="Обнулить и начать заново", callback_data="restart:confirm")],
                ]
            ),
        )
        return

    await bot.send_message(
        chat_id,
        "<b>LevelUp English</b>\nЯ на связи.\nЕсли хочешь идти по миссиям, жми кнопки. Если хочешь просто спросить что-то по английскому, просто напиши вопрос сообщением.",
        reply_markup=home_keyboard(),
    )


async def show_mission(chat_id: int, user_id: int, first_name: str) -> None:
    bootstrap_user(user_id, first_name)
    if not is_placement_completed(connection, user_id):
        await bot.send_message(
            chat_id,
            "<b>Сначала нужен стартовый тест.</b>\n\nБез него я не понимаю, откуда тебя нормально запускать.",
            reply_markup=action_keyboard("placement:start", "Запустить тест"),
        )
        return

    next_mission = get_next_mission(connection, user_id)
    if next_mission is None:
        if has_review_tasks(connection, user_id):
            pending = get_review_count(connection, user_id)
            await bot.send_message(
                chat_id,
                build_chapter_complete_text(get_chapter_summary(connection, user_id))
                + f"\n\n<b>Перед финальным чеком:</b> добей {pending} ошибок, которые накопились по ходу главы.",
                reply_markup=action_keyboard("review:start", f"Разобрать ошибки ({pending})"),
            )
        else:
            await bot.send_message(
                chat_id,
                build_chapter_complete_text(get_chapter_summary(connection, user_id)),
                reply_markup=action_keyboard("boss:start", "Открыть финальный чек"),
            )
        return

    await bot.send_message(
        chat_id,
        build_mission_intro(next_mission),
        reply_markup=action_keyboard(f"mission:start:{next_mission.id}", "Открыть миссию"),
    )


async def show_profile(chat_id: int, user_id: int, first_name: str) -> None:
    bootstrap_user(user_id, first_name)
    await bot.send_message(chat_id, get_profile_text(connection, user_id), reply_markup=home_keyboard())


async def show_review(chat_id: int, user_id: int, first_name: str) -> None:
    bootstrap_user(user_id, first_name)
    if not is_placement_completed(connection, user_id):
        await bot.send_message(
            chat_id,
            "<b>Сначала нужен стартовый тест.</b>\n\nПотом уже откроем реванш по ошибкам.",
            reply_markup=action_keyboard("placement:start", "Запустить тест"),
        )
        return

    tasks = get_review_tasks(connection, user_id)
    if not tasks:
        await bot.send_message(
            chat_id,
            "<b>Добивка ошибок пока пустая.</b>\n\nСначала пройди миссии, чтобы появился материал для предфинального захода.",
            reply_markup=action_keyboard("nav:mission", "Вернуться к миссиям"),
        )
        return

    review_task_store[user_id] = tasks
    session_store[user_id] = SessionState(mode="review", chapter_id=get_current_chapter(connection, user_id).id, content_id="review")
    await bot.send_message(
        chat_id,
        f"<b>Предфинальный разбор</b>\n\nСейчас быстро добьем {len(tasks)} слабых мест и только потом выйдем на финальный чек.",
    )
    await send_next_task(chat_id, user_id)


async def show_boss(chat_id: int, user_id: int, first_name: str) -> None:
    bootstrap_user(user_id, first_name)
    if not is_placement_completed(connection, user_id):
        await bot.send_message(
            chat_id,
            "<b>Сначала нужен стартовый тест.</b>\n\nДо босса без базы не пускаю.",
            reply_markup=action_keyboard("placement:start", "Запустить тест"),
        )
        return

    chapter = get_current_chapter(connection, user_id)
    if is_boss_completed(connection, user_id, chapter.boss.id):
        await bot.send_message(chat_id, "<b>Этот босс уже закрыт.</b>", reply_markup=home_keyboard())
        return

    if not is_boss_unlocked(connection, user_id, chapter.id):
        await bot.send_message(chat_id, get_chapter_summary(connection, user_id), reply_markup=home_keyboard())
        return

    if has_review_tasks(connection, user_id):
        pending = get_review_count(connection, user_id)
        await bot.send_message(
            chat_id,
            f"<b>Финальный чек пока не открыт.</b>\n\nПеред ним нужно добить накопившиеся ошибки: {pending} вопросов.",
            reply_markup=action_keyboard("review:start", f"Разобрать ошибки ({pending})"),
        )
        return

    await bot.send_message(chat_id, build_boss_intro(chapter.boss), reply_markup=action_keyboard("boss:start", "Открыть финальный чек"))


async def send_next_task(chat_id: int, user_id: int) -> None:
    state = session_store[user_id]

    if state.mode == "mission":
        mission = next(mission for mission in get_current_chapter(connection, user_id).missions if mission.id == state.content_id)
        mission_tasks = get_mission_tasks(state.chapter_id, mission.id, get_user_level(connection, user_id))
        task = mission_tasks[state.task_index]
        await bot.send_message(chat_id, get_task_prompt(task, state.task_index + 1, len(mission_tasks), mission.title), reply_markup=answer_keyboard(task, "mission_answer"))
        return

    if state.mode == "boss":
        boss = get_boss(state.chapter_id)
        boss_tasks = get_boss_tasks(state.chapter_id, get_user_level(connection, user_id))
        task = boss_tasks[state.task_index]
        await bot.send_message(chat_id, get_task_prompt(task, state.task_index + 1, len(boss_tasks), boss.title), reply_markup=answer_keyboard(task, "boss_answer"))
        return

    if state.mode == "placement":
        tasks = get_placement_items()
        task = tasks[state.task_index]
        await bot.send_message(chat_id, get_task_prompt(task, state.task_index + 1, len(tasks), "Стартовый тест"), reply_markup=answer_keyboard(task, "placement_answer"))
        return

    if state.mode == "review":
        tasks = review_task_store.get(user_id, [])
        if not tasks:
            session_store.pop(user_id, None)
            await bot.send_message(chat_id, "<b>Разбор ошибок закрыт.</b>", reply_markup=action_keyboard("boss:start", "Открыть финальный чек"))
            return
        task = tasks[state.task_index]
        await bot.send_message(chat_id, get_task_prompt(task, state.task_index + 1, len(tasks), "Разбор ошибок"), reply_markup=answer_keyboard(task, "review_answer"))


async def send_next_mission_offer(chat_id: int, user_id: int) -> None:
    next_mission = get_next_mission(connection, user_id)
    if next_mission is None:
        if has_review_tasks(connection, user_id):
            pending = get_review_count(connection, user_id)
            await bot.send_message(
                chat_id,
                build_chapter_complete_text(get_chapter_summary(connection, user_id))
                + f"\n\n<b>Следующий шаг:</b> добить {pending} ошибок перед финальным чеком.",
                reply_markup=action_keyboard("review:start", f"Разобрать ошибки ({pending})"),
            )
        else:
            await bot.send_message(chat_id, build_chapter_complete_text(get_chapter_summary(connection, user_id)), reply_markup=action_keyboard("boss:start", "Открыть финальный чек"))
        return
    await bot.send_message(chat_id, build_next_mission_text(next_mission), reply_markup=action_keyboard(f"mission:start:{next_mission.id}", "Идти дальше"))


async def start_next_mission(chat_id: int, user_id: int, first_name: str) -> None:
    bootstrap_user(user_id, first_name)
    next_mission = get_next_mission(connection, user_id)
    if next_mission is None:
        if has_review_tasks(connection, user_id):
            pending = get_review_count(connection, user_id)
            await bot.send_message(
                chat_id,
                build_chapter_complete_text(get_chapter_summary(connection, user_id))
                + f"\n\n<b>Дальше по сценарию:</b> разбираем {pending} ошибок и только потом идем в финальный чек.",
                reply_markup=action_keyboard("review:start", f"Разобрать ошибки ({pending})"),
            )
        else:
            await bot.send_message(chat_id, build_chapter_complete_text(get_chapter_summary(connection, user_id)), reply_markup=action_keyboard("boss:start", "Открыть финальный чек"))
        return
    session_store[user_id] = SessionState(
        mode="mission",
        chapter_id=get_current_chapter(connection, user_id).id,
        content_id=next_mission.id,
    )
    await bot.send_message(chat_id, "<b>Переходим к первой миссии.</b>\n\nБез лишних остановок.")
    await send_next_task(chat_id, user_id)


async def recover_lost_session(callback: CallbackQuery, prefix: str) -> None:
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name or "Player"
    bootstrap_user(user_id, first_name)

    if prefix == "placement_answer":
        reset_learning_progress(connection, user_id)
        session_store[user_id] = SessionState(mode="placement", chapter_id=get_current_chapter(connection, user_id).id, content_id="placement")
        await callback.message.answer(
            "<b>Сессия развалилась.</b>\n\nНо не страшно. Я уже собрал все обратно и готов перезапустить тест.",
            reply_markup=action_keyboard("placement:start", "Запустить тест заново"),
        )
        await callback.answer()
        return

    if prefix == "mission_answer":
        await callback.message.answer(
            "<b>Миссия слетела.</b>\n\nПоднимаю тебя обратно к текущему заходу.",
            reply_markup=action_keyboard("nav:mission", "Вернуться к миссии"),
        )
        await callback.answer()
        return

    if prefix == "boss_answer":
        await callback.message.answer(
            "<b>Схватка с боссом слетела.</b>\n\nВозвращаю тебя ко входу.",
            reply_markup=action_keyboard("nav:boss", "Вернуться к боссу"),
        )
        await callback.answer()
        return

    if prefix == "review_answer":
        await callback.message.answer(
            "<b>Разбор ошибок слетел.</b>\n\nСобираю его заново.",
            reply_markup=action_keyboard("review:start", "Вернуться к разбору"),
        )
        await callback.answer()
        return


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await show_start(message.chat.id, message.from_user.id, message.from_user.first_name or "Player")


@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    bootstrap_user(message.from_user.id, message.from_user.first_name or "Player")
    await message.answer(
        "<b>Как это устроено</b>\n1. Сначала проходишь стартовый тест.\n2. Потом идешь по миссиям одну за другой.\n3. Ошибки копятся по ходу главы и потом выходят в отдельный разбор.\n4. После разбора выходишь на финальный чек.\n\nЕсли хочешь просто спросить что-то по английскому, пиши вопрос прямо сюда.",
        reply_markup=home_keyboard(),
    )


@dp.message(Command("mission"))
async def cmd_mission(message: Message) -> None:
    await show_mission(message.chat.id, message.from_user.id, message.from_user.first_name or "Player")


@dp.message(Command("profile"))
async def cmd_profile(message: Message) -> None:
    await show_profile(message.chat.id, message.from_user.id, message.from_user.first_name or "Player")


@dp.message(Command("review"))
async def cmd_review(message: Message) -> None:
    await show_review(message.chat.id, message.from_user.id, message.from_user.first_name or "Player")


@dp.message(Command("boss"))
async def cmd_boss(message: Message) -> None:
    await show_boss(message.chat.id, message.from_user.id, message.from_user.first_name or "Player")


@dp.callback_query(F.data == "nav:mission")
async def nav_mission(callback: CallbackQuery) -> None:
    await show_mission(callback.message.chat.id, callback.from_user.id, callback.from_user.first_name or "Player")
    await callback.answer()


@dp.callback_query(F.data == "nav:profile")
async def nav_profile(callback: CallbackQuery) -> None:
    await show_profile(callback.message.chat.id, callback.from_user.id, callback.from_user.first_name or "Player")
    await callback.answer()


@dp.callback_query(F.data == "nav:review")
async def nav_review(callback: CallbackQuery) -> None:
    await show_review(callback.message.chat.id, callback.from_user.id, callback.from_user.first_name or "Player")
    await callback.answer()


@dp.callback_query(F.data == "review:start")
async def review_start(callback: CallbackQuery) -> None:
    await show_review(callback.message.chat.id, callback.from_user.id, callback.from_user.first_name or "Player")
    await callback.answer()


@dp.callback_query(F.data == "nav:boss")
async def nav_boss(callback: CallbackQuery) -> None:
    await show_boss(callback.message.chat.id, callback.from_user.id, callback.from_user.first_name or "Player")
    await callback.answer()


@dp.callback_query(F.data == "nav:restart")
async def nav_restart(callback: CallbackQuery) -> None:
    await callback.message.answer(
        "<b>Точно хочешь снести прогресс?</b>\n\nЭто обнулит XP, миссии, реванш и стартовый тест.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Да, обнулить все", callback_data="restart:confirm")],
                [InlineKeyboardButton(text="Не, отмена", callback_data="restart:cancel")],
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(F.data == "restart:cancel")
async def restart_cancel(callback: CallbackQuery) -> None:
    await callback.message.answer("<b>Окей, ничего не трогаю.</b>", reply_markup=home_keyboard())
    await callback.answer()


@dp.callback_query(F.data == "restart:confirm")
async def restart_confirm(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name or "Player"
    bootstrap_user(user_id, first_name)
    reset_learning_progress(connection, user_id)
    connection.execute(
        """
        UPDATE users
        SET placement_completed = 0,
            estimated_level = 'unknown'
        WHERE telegram_user_id = ?
        """,
        (user_id,),
    )
    connection.commit()
    session_store.pop(user_id, None)
    review_task_store.pop(user_id, None)
    await callback.message.answer(
        "<b>Все, прогресс обнулен.</b>\n\nТеперь можно стартовать заново и пройти тест с чистого листа.",
        reply_markup=action_keyboard("placement:start", "Запустить тест"),
    )
    await callback.answer()


@dp.callback_query(F.data == "placement:start")
async def placement_start(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name or "Player"
    bootstrap_user(user_id, first_name)
    reset_learning_progress(connection, user_id)
    session_store[user_id] = SessionState(mode="placement", chapter_id=get_current_chapter(connection, user_id).id, content_id="placement")
    await callback.message.answer("<b>Погнали.</b>\n\nСейчас спокойно снимем базовый срез, а потом уже пойдем по миссиям.")
    await send_next_task(callback.message.chat.id, user_id)
    await callback.answer()


@dp.callback_query(F.data.startswith("mission:start:"))
async def mission_start(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name or "Player"
    bootstrap_user(user_id, first_name)
    mission_id = callback.data.split(":")[-1]
    session_store[user_id] = SessionState(mode="mission", chapter_id=get_current_chapter(connection, user_id).id, content_id=mission_id)
    await callback.message.answer("<b>Заходим в миссию.</b>")
    await send_next_task(callback.message.chat.id, user_id)
    await callback.answer()


@dp.callback_query(F.data == "boss:start")
async def boss_start(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name or "Player"
    bootstrap_user(user_id, first_name)
    chapter = get_current_chapter(connection, user_id)
    if not is_boss_unlocked(connection, user_id, chapter.id):
        await callback.message.answer("<b>Босс пока закрыт.</b>\n\nСначала добей все миссии этой главы.", reply_markup=home_keyboard())
        await callback.answer()
        return
    if has_review_tasks(connection, user_id):
        pending = get_review_count(connection, user_id)
        await callback.message.answer(
            f"<b>Рано в финальный чек.</b>\n\nСначала разберем {pending} накопившихся ошибок, чтобы не тащить их в финал.",
            reply_markup=action_keyboard("review:start", f"Разобрать ошибки ({pending})"),
        )
        await callback.answer()
        return
    session_store[user_id] = SessionState(mode="boss", chapter_id=chapter.id, content_id=chapter.boss.id)
    await callback.message.answer("<b>Окей. Врубаем финальный чек.</b>")
    await send_next_task(callback.message.chat.id, user_id)
    await callback.answer()


async def handle_answer(callback: CallbackQuery, prefix: str) -> None:
    state = session_store.get(callback.from_user.id)
    if state is None:
        await recover_lost_session(callback, prefix)
        return

    answer_index = int(callback.data.split(":")[-1])
    callback_notice = ""

    if prefix == "placement_answer":
        tasks = get_placement_items()
        task = tasks[state.task_index]
        is_correct = answer_index == task.correct_index
        if is_correct:
            state.correct_answers += 1
        state.task_index += 1
        if state.task_index >= len(tasks):
            level = complete_placement(connection, callback.from_user.id, state.correct_answers)
            apply_level_routing(connection, callback.from_user.id, level)
            session_store.pop(callback.from_user.id, None)
            await callback.message.answer(build_placement_result(state.correct_answers, len(tasks), level))
            ai_summary = await generate_ai_summary("placement", "Стартовый тест", f"{state.correct_answers}/{len(tasks)}, уровень {level}")
            if ai_summary:
                await callback.message.answer(ai_summary)
            await start_next_mission(callback.message.chat.id, callback.from_user.id, callback.from_user.first_name or "Player")
        else:
            callback_notice = "Ответ принят"
            await send_next_task(callback.message.chat.id, callback.from_user.id)

    elif prefix == "mission_answer":
        mission = next(mission for mission in get_current_chapter(connection, callback.from_user.id).missions if mission.id == state.content_id)
        mission_tasks = get_mission_tasks(state.chapter_id, mission.id, get_user_level(connection, callback.from_user.id))
        task = mission_tasks[state.task_index]
        is_correct = answer_index == task.correct_index
        await callback.message.answer(build_mission_feedback(is_correct, task))
        if is_correct:
            state.correct_answers += 1
        else:
            add_review_item(connection, callback.from_user.id, task, "mission")
        state.task_index += 1
        if state.task_index >= len(mission_tasks):
            complete_mission(connection, callback.from_user.id, mission, state.correct_answers)
            session_store.pop(callback.from_user.id, None)
            accuracy = round(state.correct_answers / len(mission_tasks) * 100) if mission_tasks else 0
            await callback.message.answer(
                build_mission_result_detailed(state.correct_answers, len(mission_tasks), mission.xp_reward),
                reply_markup=mission_complete_keyboard(callback.from_user.id, accuracy),
            )
            ai_summary = await generate_ai_summary("mission", mission.title, f"{state.correct_answers}/{len(mission_tasks)}, награда {mission.xp_reward} XP")
            if ai_summary:
                await callback.message.answer(ai_summary)
        else:
            await send_next_task(callback.message.chat.id, callback.from_user.id)

    elif prefix == "boss_answer":
        boss = get_boss(state.chapter_id)
        boss_tasks = get_boss_tasks(state.chapter_id, get_user_level(connection, callback.from_user.id))
        task = boss_tasks[state.task_index]
        is_correct = answer_index == task.correct_index
        checkpoint_feedback = build_checkpoint_feedback(is_correct, task)
        if checkpoint_feedback:
            await callback.message.answer(checkpoint_feedback)
        if is_correct:
            state.correct_answers += 1
            callback_notice = "Принято"
        else:
            add_review_item(connection, callback.from_user.id, task, "boss")
        state.task_index += 1
        if state.task_index >= len(boss_tasks):
            complete_boss(connection, callback.from_user.id, boss, state.correct_answers)
            session_store.pop(callback.from_user.id, None)
            await callback.message.answer(build_boss_result(state.correct_answers, len(boss_tasks), boss.xp_reward))
            ai_summary = await generate_ai_summary("boss", boss.title, f"{state.correct_answers}/{len(boss_tasks)}, награда {boss.xp_reward} XP")
            if ai_summary:
                await callback.message.answer(ai_summary)
            await bot.send_message(callback.message.chat.id, "Если хочешь, можешь теперь просто написать мне любой вопрос по английскому.")
        else:
            await send_next_task(callback.message.chat.id, callback.from_user.id)

    elif prefix == "review_answer":
        tasks = review_task_store.get(callback.from_user.id, [])
        if not tasks:
            session_store.pop(callback.from_user.id, None)
            await callback.message.answer("<b>Разбор ошибок уже закрыт.</b>", reply_markup=action_keyboard("boss:start", "Открыть финальный чек"))
            await callback.answer()
            return
        task = tasks[state.task_index]
        is_correct = answer_index == task.correct_index
        checkpoint_feedback = build_checkpoint_feedback(is_correct, task)
        if checkpoint_feedback:
            await callback.message.answer(checkpoint_feedback)
        if is_correct:
            remove_review_item(connection, callback.from_user.id, task.id)
            state.correct_answers += 1
            callback_notice = "Принято"
        state.task_index += 1
        if state.task_index >= len(tasks):
            review_task_store.pop(callback.from_user.id, None)
            session_store.pop(callback.from_user.id, None)
            await callback.message.answer(
                "<b>Разбор ошибок закрыт.</b>\n\nСлабые места добили. Теперь можно идти в финальный чек.",
                reply_markup=action_keyboard("boss:start", "Открыть финальный чек"),
            )
        else:
            await send_next_task(callback.message.chat.id, callback.from_user.id)

    await callback.answer(callback_notice)


@dp.callback_query(F.data.startswith("placement_answer:"))
async def placement_answer(callback: CallbackQuery) -> None:
    await handle_answer(callback, "placement_answer")


@dp.callback_query(F.data.startswith("mission_answer:"))
async def mission_answer(callback: CallbackQuery) -> None:
    await handle_answer(callback, "mission_answer")


@dp.callback_query(F.data.startswith("boss_answer:"))
async def boss_answer(callback: CallbackQuery) -> None:
    await handle_answer(callback, "boss_answer")


@dp.callback_query(F.data.startswith("review_answer:"))
async def review_answer(callback: CallbackQuery) -> None:
    await handle_answer(callback, "review_answer")


@dp.message()
async def fallback(message: Message) -> None:
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Player"
    bootstrap_user(user_id, first_name)

    local_answer = local_tutor_fallback(message.text or "")
    if local_answer:
        if user_id in session_store:
            await message.answer(
                local_answer + "\n\n<b>Текущий заход не слетел.</b> Можешь спокойно вернуться к миссии, когда захочешь.",
                reply_markup=home_keyboard(),
            )
        else:
            await message.answer(local_answer, reply_markup=home_keyboard())
        return

    answer = await ask_tutor(message.text or "")
    if answer:
        if user_id in session_store:
            await message.answer(
                answer + "\n\n<b>Текущий заход я не сбрасывал.</b> Когда захочешь, просто продолжай по кнопкам.",
                reply_markup=home_keyboard(),
            )
        else:
            await message.answer(answer, reply_markup=home_keyboard())
        return

    short_answer = await ask_tutor(f"Ответь очень коротко и просто без списков: {message.text or ''}")
    if short_answer:
        if user_id in session_store:
            await message.answer(
                short_answer + "\n\n<b>Текущий заход сохранен.</b> Можешь вернуться к нему в любой момент.",
                reply_markup=home_keyboard(),
            )
        else:
            await message.answer(short_answer, reply_markup=home_keyboard())
        return

    local_answer = local_tutor_fallback(message.text or "")
    if local_answer:
        if user_id in session_store:
            await message.answer(
                local_answer + "\n\n<b>Сценарий миссии не сброшен.</b> Можешь продолжить дальше, когда захочешь.",
                reply_markup=home_keyboard(),
            )
        else:
            await message.answer(local_answer, reply_markup=home_keyboard())
        return

    await message.answer(
        "<b>Я не завис, просто не смог нормально ответить.</b>\n\nПопробуй переформулировать вопрос попроще или нажми кнопки ниже.",
        reply_markup=home_keyboard(),
    )


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
