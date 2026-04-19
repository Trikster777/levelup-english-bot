from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Task:
    id: str
    prompt: str
    options: tuple[str, ...]
    correct_index: int
    explanation: str
    skill: str


@dataclass(frozen=True, slots=True)
class Mission:
    id: str
    title: str
    description: str
    xp_reward: int
    tasks: tuple[Task, ...]


@dataclass(frozen=True, slots=True)
class Boss:
    id: str
    title: str
    description: str
    xp_reward: int
    tasks: tuple[Task, ...]


@dataclass(frozen=True, slots=True)
class Chapter:
    id: str
    title: str
    description: str
    missions: tuple[Mission, ...]
    boss: Boss


PLACEMENT_TASKS: tuple[Task, ...] = (
    Task("placement_1", "Выбери правильный вариант:", ("She go to school every day.", "She goes to school every day.", "She going to school every day."), 1, "С `she / he / it` в Present Simple нужен глагол с `-s`.", "placement"),
    Task("placement_2", "Как правильно сказать: `Я делаю домашку после школы`?", ("I do my homework after school.", "I am do homework after school.", "I doing homework after school."), 0, "Базовый правильный вариант: `I do my homework after school.`", "placement"),
    Task("placement_3", "Выбери правильный вопрос:", ("Does he like English?", "Does he likes English?", "Do he like English?"), 0, "Правильно: `Does he like English?`", "placement"),
    Task("placement_4", "Что значит `rarely`?", ("редко", "громко", "быстро"), 0, "`rarely` — это `редко`.", "placement"),
    Task("placement_5", "Что звучит правильно?", ("I usually get up at seven.", "I usually gets up at seven.", "I am usually get up at seven."), 0, "С `I` нужен обычный глагол без `-s`.", "placement"),
    Task("placement_6", "Выбери нормальный короткий ответ:", ("Yes, I do.", "Yes, I am do.", "Yes, I does."), 0, "Для Present Simple короткий ответ: `Yes, I do.`", "placement"),
    Task("placement_7", "Как переводится `have breakfast`?", ("делать завтрак", "завтракать", "готовить ужин"), 1, "`have breakfast` — это `завтракать`.", "placement"),
    Task("placement_8", "Что звучит правильно?", ("He doesn't like maths.", "He don't like maths.", "He doesn't likes maths."), 0, "После `doesn't` глагол идет в базовой форме.", "placement"),
    Task("placement_9", "Выбери правильный порядок слов:", ("I sometimes play games after school.", "I play sometimes games after school.", "Sometimes I play after school games."), 0, "Так предложение звучит естественно и грамотно.", "placement"),
    Task("placement_10", "Какой вопрос составлен правильно?", ("What time do you get home?", "What time you do get home?", "What time does you get home?"), 0, "Правильно: `What time do you get home?`", "placement"),
)


MISSION_1_TASKS: tuple[Task, ...] = (
    Task("rw_1", "Как переводится `wake up`?", ("ложиться спать", "просыпаться", "одеваться"), 1, "`wake up` — это `просыпаться`.", "vocabulary"),
    Task("rw_2", "Как переводится `get dressed`?", ("одеваться", "умываться", "опаздывать"), 0, "`get dressed` — это `одеваться`.", "vocabulary"),
    Task("rw_3", "Как переводится `go to bed`?", ("идти домой", "ложиться спать", "идти в школу"), 1, "`go to bed` — это `ложиться спать`.", "vocabulary"),
    Task("rw_4", "Что значит `after school`?", ("после школы", "перед школой", "в школе"), 0, "`after school` — это `после школы`.", "vocabulary"),
    Task("rw_5", "Что значит `usually`?", ("обычно", "никогда", "вчера"), 0, "`usually` — это `обычно`.", "vocabulary"),
    Task("rw_6", "Что значит `sometimes`?", ("всегда", "иногда", "редко"), 1, "`sometimes` — это `иногда`.", "vocabulary"),
    Task("rw_7", "Как переводится `do homework`?", ("писать письмо", "делать домашку", "играть в игру"), 1, "`do homework` — это `делать домашку`.", "vocabulary"),
    Task("rw_8", "Как переводится `free time`?", ("свободное время", "время урока", "домашнее задание"), 0, "`free time` — это `свободное время`.", "vocabulary"),
    Task("rw_9", "Как переводится `before dinner`?", ("до ужина", "после ужина", "во время урока"), 0, "`before dinner` — это `до ужина`.", "vocabulary"),
    Task("rw_10", "Как правильно: `Он завтракает в семь`?", ("He has breakfast at seven.", "He have breakfast at seven.", "He breakfasts at seven."), 0, "Самый естественный вариант: `He has breakfast at seven.`", "vocabulary"),
    Task("rw_11", "Выбери верный перевод: `Я прихожу домой в четыре`", ("I get home at four.", "I come to home in four.", "I home get at four."), 0, "Нормально звучит `I get home at four.`", "vocabulary"),
    Task("rw_12", "Как перевести `I hang out with friends after school`?", ("Я спорю с друзьями после школы", "Я тусуюсь с друзьями после школы", "Я учу друзей после школы"), 1, "`hang out` — это `тусоваться / проводить время`.", "vocabulary"),
    Task("rw_13", "Что звучит естественно?", ("We have dinner in the evening.", "We do dinner in the evening.", "We are dinner in the evening."), 0, "О еде обычно говорим `have dinner`.", "vocabulary"),
    Task("rw_14", "Что звучит естественно?", ("She walks to school.", "She go walk to school.", "She walking to school."), 0, "Естественно: `She walks to school.`", "vocabulary"),
    Task("rw_15", "Как правильно сказать: `Я обычно делаю домашку после школы`?", ("I usually do my homework after school.", "I do usually my homework after school.", "Usually I after school do homework."), 0, "Нормальный порядок слов: subject + adverb + verb + object.", "vocabulary"),
)


MISSION_2_TASKS: tuple[Task, ...] = (
    Task("ps_1", "Выбери правильное предложение:", ("He go to school every day.", "He goes to school every day.", "He going to school every day."), 1, "С `he / she / it` нужен глагол с `-s / -es`.", "grammar"),
    Task("ps_2", "Какой вопрос составлен правильно?", ("Do she play football?", "Does she plays football?", "Does she play football?"), 2, "В вопросе используем `Does + base verb`.", "grammar"),
    Task("ps_3", "Что звучит правильно?", ("I plays games every evening.", "I play games every evening.", "I am play games every evening."), 1, "С `I` нужен обычный глагол без `-s`.", "grammar"),
    Task("ps_4", "Выбери правильное отрицание:", ("He doesn't like maths.", "He don't like maths.", "He doesn't likes maths."), 0, "После `doesn't` глагол идет в базовой форме.", "grammar"),
    Task("ps_5", "Что звучит правильно?", ("Do you usually get up early?", "Does you usually get up early?", "Are you usually get up early?"), 0, "Вопрос с `you`: `Do you ... ?`", "grammar"),
    Task("ps_6", "Выбери правильный вариант:", ("My sister study English.", "My sister studies English.", "My sister studying English."), 1, "С `my sister` нужен глагол `studies`.", "grammar"),
    Task("ps_7", "Что звучит правильно?", ("We doesn't go home late.", "We don't go home late.", "We aren't go home late."), 1, "С `we` используем `don't`.", "grammar"),
    Task("ps_8", "Какой вопрос нормальный?", ("What time do you go to bed?", "What time you go to bed?", "What time does you go to bed?"), 0, "Правильно: `What time do you go to bed?`", "grammar"),
    Task("ps_9", "Выбери верный вариант:", ("She usually watch videos at night.", "She usually watches videos at night.", "She usually watching videos at night."), 1, "С `she` нужен `watches`.", "grammar"),
    Task("ps_10", "Что звучит правильно?", ("Do they have lunch at school?", "Does they have lunch at school?", "Do they has lunch at school?"), 0, "С `they` используем `Do`.", "grammar"),
    Task("ps_11", "Какое предложение правильное?", ("My friends lives near school.", "My friends live near school.", "My friends living near school."), 1, "С `friends` глагол без `-s`.", "grammar"),
    Task("ps_12", "Выбери правильный вопрос:", ("Does your brother play basketball?", "Does your brother plays basketball?", "Do your brother play basketball?"), 0, "С `brother` нужен `Does + play`.", "grammar"),
    Task("ps_13", "Что звучит правильно?", ("I don't like getting up early.", "I doesn't like getting up early.", "I not like getting up early."), 0, "С `I` используем `don't`.", "grammar"),
    Task("ps_14", "Какой вариант нормальный?", ("She doesn't get home late.", "She don't get home late.", "She doesn't gets home late."), 0, "После `doesn't` — базовый глагол.", "grammar"),
    Task("ps_15", "Выбери правильное предложение:", ("We usually finish school at two.", "We usually finishes school at two.", "We are usually finish school at two."), 0, "С `we` — обычный глагол без `-s`.", "grammar"),
)


MISSION_3_TASKS: tuple[Task, ...] = (
    Task("sd_1", "Friend: `What time do you get home?` Как ответить лучше всего?", ("I get home at about four.", "I home at four get.", "At four home I."), 0, "Естественный ответ: `I get home at about four.`", "dialogue"),
    Task("sd_2", "Teacher: `Do you usually have lunch at school?`", ("Yes, I usually do.", "Yes, I usually have.", "Yes, usually lunch."), 0, "Короткий и естественный ответ: `Yes, I usually do.`", "dialogue"),
    Task("sd_3", "Friend: `Do you like English?`", ("Yeah, I do. It's fun.", "Yeah, I am like English.", "Yeah, like."), 0, "Коротко и естественно: `Yeah, I do. It's fun.`", "dialogue"),
    Task("sd_4", "Teacher: `Are you late again?`", ("No, I'm on time.", "No, I late.", "No, I am time."), 0, "Естественно: `No, I'm on time.`", "dialogue"),
    Task("sd_5", "Friend: `What do you do after school?`", ("I usually go home and chill a bit.", "I usually home and chill.", "Usually go home and chill I."), 0, "Нормальный разговорный ответ.", "dialogue"),
    Task("sd_6", "Classmate: `Can you help me with homework?`", ("Sure, no problem.", "Yes, I can helping.", "Sure, I help you now maybe yes."), 0, "Коротко и нормально: `Sure, no problem.`", "dialogue"),
    Task("sd_7", "Friend: `Do you play games in the evening?`", ("Sometimes, yeah.", "Sometimes I am.", "Yes, I play games in evening sometimes am."), 0, "Простой естественный ответ: `Sometimes, yeah.`", "dialogue"),
    Task("sd_8", "Teacher: `Why are you tired today?`", ("I go to bed late.", "I late bed go.", "I am go bed late."), 0, "Правильно: `I go to bed late.`", "dialogue"),
    Task("sd_9", "Friend: `Wanna hang out after school?`", ("Yeah, sounds good.", "Yes, I am hang out.", "I sounds good yes hang out."), 0, "Естественная реакция: `Yeah, sounds good.`", "dialogue"),
    Task("sd_10", "Teacher: `Do you understand this exercise?`", ("Not really. Can you explain it again?", "No really understand.", "Can again explain you?"), 0, "Так звучит живо и грамотно.", "dialogue"),
    Task("sd_11", "Friend: `What's your favorite subject?`", ("Probably English.", "Favorite subject probably is.", "I subject favorite English."), 0, "Короткий естественный ответ.", "dialogue"),
    Task("sd_12", "Classmate: `Do you have plans tonight?`", ("Yeah, I need to finish homework.", "Yeah, I am finish homework.", "Need finish homework yes I."), 0, "Нормально: `Yeah, I need to finish homework.`", "dialogue"),
    Task("sd_13", "Teacher: `Do you usually read in English?`", ("A little, but not every day.", "A little, but not every day I am.", "Little not every day."), 0, "Живой и понятный ответ.", "dialogue"),
    Task("sd_14", "Friend: `How do you get to school?`", ("I usually walk.", "I usually by walk.", "Usually I am walk."), 0, "Простой правильный ответ: `I usually walk.`", "dialogue"),
    Task("sd_15", "Friend: `Are you free this evening?`", ("Maybe a bit later.", "Maybe I am free later a bit.", "Later maybe bit."), 0, "Коротко и естественно: `Maybe a bit later.`", "dialogue"),
)


DAILY_ROUTINE_CHAPTER = Chapter(
    id="daily_routine",
    title="Глава 1. База без паники",
    description="Без суеты собираем фундамент: обычный день, школа, ритм жизни и базовые фразы, чтобы дальше не сыпаться на каждом шаге.",
    missions=(
        Mission("routine_words", "Миссия 1. Разогрев", "Спокойно собираем словарь на тему обычного дня. Тут без жести, просто входим в ритм.", 40, MISSION_1_TASKS),
        Mission("present_simple", "Миссия 2. Грамматика без духоты", "Подкручиваем Present Simple, чтобы фразы держались ровно и не разваливались.", 45, MISSION_2_TASKS),
        Mission("school_dialogue", "Миссия 3. Живые ответы", "Учимся звучать живо: короткие ответы, диалоги и нормальная речь без робота в голове.", 50, MISSION_3_TASKS),
    ),
    boss=Boss(
        id="daily_routine_boss",
        title="Босс главы. Первый заход",
        description="Собираем все вместе. Не спешим, просто проверяем, насколько база уже держится.",
        xp_reward=80,
        tasks=(
            Task("boss_1", "Выбери правильное предложение:", ("She usually walk to school.", "She usually walks to school.", "She walk usually to school."), 1, "С `she` нужен глагол с `-s`.", "grammar"),
            Task("boss_2", "Что значит `rarely`?", ("часто", "редко", "сразу"), 1, "`rarely` — это `редко`.", "vocabulary"),
            Task("boss_3", "Какой короткий ответ звучит нормально?", ("Yes, I usually do.", "Yes, I usually am.", "Yes, I usually doing."), 0, "Нормальный короткий ответ: `Yes, I usually do.`", "dialogue"),
            Task("boss_4", "Что звучит правильно?", ("My brother studies English.", "My brother study English.", "My brother studying English."), 0, "С `my brother` нужен `studies`.", "grammar"),
            Task("boss_5", "Как переводится `after school`?", ("после школы", "до школы", "в школе"), 0, "`after school` — это `после школы`.", "vocabulary"),
            Task("boss_6", "Friend: `What do you do after school?`", ("I usually go home and rest a bit.", "I usually home rest.", "Go home usually I."), 0, "Естественный ответ: `I usually go home and rest a bit.`", "dialogue"),
        ),
    ),
)


CHAPTERS: tuple[Chapter, ...] = (DAILY_ROUTINE_CHAPTER,)


def get_chapter(chapter_id: str) -> Chapter:
    for chapter in CHAPTERS:
        if chapter.id == chapter_id:
            return chapter
    raise KeyError(f"Unknown chapter id: {chapter_id}")


def get_mission(chapter_id: str, mission_id: str) -> Mission:
    chapter = get_chapter(chapter_id)
    for mission in chapter.missions:
        if mission.id == mission_id:
            return mission
    raise KeyError(f"Unknown mission id: {mission_id}")


def get_boss(chapter_id: str) -> Boss:
    return get_chapter(chapter_id).boss


def get_placement_tasks() -> tuple[Task, ...]:
    return PLACEMENT_TASKS
