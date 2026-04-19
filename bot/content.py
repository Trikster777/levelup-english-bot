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


def _tasks(prefix: str, skill: str, rows: list[tuple[str, tuple[str, ...], int, str]]) -> tuple[Task, ...]:
    return tuple(
        Task(
            id=f"{prefix}_{index}",
            prompt=prompt,
            options=options,
            correct_index=correct_index,
            explanation=explanation,
            skill=skill,
        )
        for index, (prompt, options, correct_index, explanation) in enumerate(rows, start=1)
    )


PLACEMENT_TASKS: tuple[Task, ...] = _tasks(
    "placement",
    "placement",
    [
        ("Выбери правильный вариант:", ("She go to school every day.", "She goes to school every day.", "She going to school every day."), 1, "С `she / he / it` в Present Simple нужен глагол с `-s`."),
        ("Как правильно сказать: `Я делаю домашку после школы`?", ("I do my homework after school.", "I am do homework after school.", "I doing homework after school."), 0, "Правильно: `I do my homework after school.`"),
        ("Выбери правильный вопрос:", ("Does he like English?", "Does he likes English?", "Do he like English?"), 0, "Правильно: `Does he like English?`"),
        ("Что значит `rarely`?", ("редко", "громко", "быстро"), 0, "`rarely` — это `редко`."),
        ("Что звучит правильно?", ("I usually get up at seven.", "I usually gets up at seven.", "I am usually get up at seven."), 0, "С `I` нужен обычный глагол без `-s`."),
        ("Выбери нормальный короткий ответ:", ("Yes, I do.", "Yes, I am do.", "Yes, I does."), 0, "Для Present Simple короткий ответ: `Yes, I do.`"),
        ("Как переводится `have breakfast`?", ("делать завтрак", "завтракать", "готовить ужин"), 1, "`have breakfast` — это `завтракать`."),
        ("Что звучит правильно?", ("He doesn't like maths.", "He don't like maths.", "He doesn't likes maths."), 0, "После `doesn't` глагол идет в базовой форме."),
        ("Выбери правильный порядок слов:", ("I sometimes play games after school.", "I play sometimes games after school.", "Sometimes I play after school games."), 0, "Так предложение звучит естественно и грамотно."),
        ("Какой вопрос составлен правильно?", ("What time do you get home?", "What time you do get home?", "What time does you get home?"), 0, "Правильно: `What time do you get home?`"),
    ],
)


ROUTINE_A2 = _tasks(
    "routine_a2",
    "vocabulary",
    [
        ("Как переводится `wake up`?", ("ложиться спать", "просыпаться", "одеваться"), 1, "`wake up` — это `просыпаться`."),
        ("Как переводится `get dressed`?", ("одеваться", "умываться", "опаздывать"), 0, "`get dressed` — это `одеваться`."),
        ("Как переводится `go to bed`?", ("идти домой", "ложиться спать", "идти в школу"), 1, "`go to bed` — это `ложиться спать`."),
        ("Что значит `after school`?", ("после школы", "перед школой", "в школе"), 0, "`after school` — это `после школы`."),
        ("Что значит `before dinner`?", ("до ужина", "после ужина", "на уроке"), 0, "`before dinner` — это `до ужина`."),
        ("Что значит `usually`?", ("обычно", "никогда", "вчера"), 0, "`usually` — это `обычно`."),
        ("Что значит `sometimes`?", ("всегда", "иногда", "редко"), 1, "`sometimes` — это `иногда`."),
        ("Что значит `free time`?", ("свободное время", "урочное время", "контрольная"), 0, "`free time` — это `свободное время`."),
        ("Как переводится `do homework`?", ("делать домашку", "учить учителя", "играть в игру"), 0, "`do homework` — это `делать домашку`."),
        ("Как переводится `have dinner`?", ("ужинать", "готовить ужин", "мыть посуду"), 0, "`have dinner` — это `ужинать`."),
        ("Выбери правильный перевод: `Я прихожу домой в четыре`", ("I get home at four.", "I come to home in four.", "I home get at four."), 0, "Нормально: `I get home at four.`"),
        ("Выбери правильный вариант: `Он завтракает в семь`", ("He has breakfast at seven.", "He have breakfast at seven.", "He breakfast at seven."), 0, "Естественно: `He has breakfast at seven.`"),
        ("Что значит `hang out with friends`?", ("тусоваться с друзьями", "спорить с друзьями", "учить друзей"), 0, "`hang out with friends` — это `тусоваться с друзьями`."),
        ("Что значит `get home late`?", ("рано прийти домой", "поздно прийти домой", "уйти из дома"), 1, "`get home late` — это `поздно прийти домой`."),
        ("Что звучит правильно?", ("We have dinner in the evening.", "We do dinner in the evening.", "We are dinner in the evening."), 0, "О еде обычно говорим `have dinner`."),
        ("Что звучит правильно?", ("She walks to school.", "She go walk to school.", "She walking to school."), 0, "Естественно: `She walks to school.`"),
        ("Как сказать: `У меня мало свободного времени`?", ("I have little free time.", "I am little free time.", "I get little free time am."), 0, "Нормально: `I have little free time.`"),
        ("Что значит `take a shower`?", ("принимать душ", "чистить зубы", "ложиться спать"), 0, "`take a shower` — это `принимать душ`."),
        ("Что значит `on weekdays`?", ("по выходным", "по будням", "по вечерам"), 1, "`on weekdays` — это `по будням`."),
        ("Как правильно сказать: `Я обычно делаю домашку после школы`?", ("I usually do my homework after school.", "I do usually my homework after school.", "Usually I after school do homework."), 0, "Нормальный порядок слов: subject + adverb + verb + object."),
    ],
)


ROUTINE_PLUS = _tasks(
    "routine_plus",
    "vocabulary",
    [
        ("Как лучше перевести `I usually crash at around midnight`?", ("Я обычно просыпаюсь около полуночи", "Я обычно вырубаюсь около полуночи", "Я обычно ем в полночь"), 1, "`crash` в разговорном английском здесь значит `вырубаться / ложиться спать без сил`."),
        ("Что ближе по смыслу к `I scroll my phone before bed`?", ("Я заряжаю телефон перед сном", "Я листаю телефон перед сном", "Я выключаю телефон перед сном"), 1, "`scroll my phone` — это `листать телефон`."),
        ("Как естественно сказать: `По будням я редко опаздываю`?", ("On weekdays I rarely run late.", "On weekdays I rarely am late run.", "Weekdays I run rarely late."), 0, "`run late` — нормальный живой вариант для `опаздывать`."),
        ("Что лучше означает `grab breakfast on the go`?", ("спокойно завтракать дома", "быстро хватать завтрак на ходу", "готовить завтрак для друзей"), 1, "`on the go` — это `на ходу`."),
        ("Как перевести `I head home right after class`?", ("Я остаюсь дома после уроков", "Я сразу иду домой после уроков", "Я иду в класс после дома"), 1, "`head home` — это `направляться домой`."),
        ("Что ближе к `My routine falls apart on weekends`?", ("Мой распорядок разваливается по выходным", "Мой распорядок начинается по выходным", "Мой распорядок идет быстрее по выходным"), 0, "`falls apart` — это `разваливается`."),
        ("Как правильно сказать: `Я обычно зависаю с друзьями после тренировки`?", ("I usually hang out with friends after practice.", "I usually hang with friends after practice out.", "Usually I after practice hang out."), 0, "Нормально: `I usually hang out with friends after practice.`"),
        ("Что значит `I’m not much of a morning person`?", ("Я люблю утро", "Я не особо утренний человек", "Я просыпаюсь очень рано"), 1, "Эта фраза значит, что человеку тяжело утром."),
        ("Как перевести `I squeeze in homework before dinner`?", ("Я откладываю домашку до ужина", "Я втискиваю домашку до ужина", "Я успеваю втиснуть домашку до ужина"), 2, "`squeeze in` — это `с трудом успеть впихнуть в расписание`."),
        ("Что звучит естественно?", ("I waste too much time online at night.", "I spend waste too much time online at night.", "I too much waste time online."), 0, "Нормально: `I waste too much time online at night.`"),
        ("Что ближе по смыслу к `I’m running on very little sleep`?", ("Я бегаю и мало сплю", "Я держусь почти без сна", "Я люблю короткий сон"), 1, "`running on very little sleep` — это `функционировать почти без сна`."),
        ("Как сказать: `После школы я обычно немного перезагружаюсь`?", ("After school I usually reset a little.", "After school I usually recharge a bit.", "After school I usually reload a bit."), 1, "В живой речи лучше `recharge a bit`."),
        ("Что значит `My schedule is packed`?", ("У меня гибкий график", "Мой график забит под завязку", "Мой график пустой"), 1, "`packed` — это `забитый, плотный`."),
        ("Как правильно сказать: `Я стараюсь держать нормальный режим сна`?", ("I try to keep a decent sleep schedule.", "I try keep decent sleep schedule.", "I am try to keep sleep schedule."), 0, "Нормально: `I try to keep a decent sleep schedule.`"),
        ("Что лучше переводит `I zone out in class if I sleep too little`?", ("Я вырубаюсь на уроке, если мало сплю", "Я теряю концентрацию на уроке, если мало сплю", "Я ухожу с урока, если мало сплю"), 1, "`zone out` — это `отключаться вниманием`."),
        ("Что означает `I stay up way too late binge-watching stuff`?", ("Я ложусь слишком рано из-за сериалов", "Я слишком поздно не сплю, залипая в сериалы", "Я смотрю один фильм утром"), 1, "`stay up late` + `binge-watching` — это поздно не спать из-за сериалов."),
        ("Как естественно сказать: `По утрам я обычно не разговариваю до кофе`?", ("In the mornings I usually don't talk before coffee.", "In mornings I usually not talk before coffee.", "Usually I don't talk before coffee in the mornings."), 0, "Первый вариант звучит чище и естественнее."),
        ("Что значит `I’m trying to cut down on screen time`?", ("Я хочу увеличить экранное время", "Я пытаюсь сократить экранное время", "Я пытаюсь починить экран"), 1, "`cut down on` — это `сокращать`."),
        ("Как перевести `My evenings disappear way too fast`?", ("Мои вечера исчезают слишком быстро", "Мои вечера начинаются быстро", "Мои вечера скучные"), 0, "Здесь идея в том, что вечер очень быстро заканчивается."),
        ("Что звучит лучше?", ("I usually get my homework done before I chill.", "I usually get done my homework before I chill.", "Usually I get homework done before chill I."), 0, "Нормально: `I usually get my homework done before I chill.`"),
    ],
)


GRAMMAR_A2 = _tasks(
    "grammar_a2",
    "grammar",
    [
        ("Выбери правильное предложение:", ("He go to school every day.", "He goes to school every day.", "He going to school every day."), 1, "С `he / she / it` нужен глагол с `-s / -es`."),
        ("Какой вопрос составлен правильно?", ("Do she play football?", "Does she plays football?", "Does she play football?"), 2, "В вопросе используем `Does + base verb`."),
        ("Что звучит правильно?", ("I plays games every evening.", "I play games every evening.", "I am play games every evening."), 1, "С `I` нужен обычный глагол без `-s`."),
        ("Выбери правильное отрицание:", ("He doesn't like maths.", "He don't like maths.", "He doesn't likes maths."), 0, "После `doesn't` глагол идет в базовой форме."),
        ("Что звучит правильно?", ("Do you usually get up early?", "Does you usually get up early?", "Are you usually get up early?"), 0, "Вопрос с `you`: `Do you ... ?`"),
        ("Выбери правильный вариант:", ("My sister study English.", "My sister studies English.", "My sister studying English."), 1, "С `my sister` нужен глагол `studies`."),
        ("Что звучит правильно?", ("We doesn't go home late.", "We don't go home late.", "We aren't go home late."), 1, "С `we` используем `don't`."),
        ("Какой вопрос нормальный?", ("What time do you go to bed?", "What time you go to bed?", "What time does you go to bed?"), 0, "Правильно: `What time do you go to bed?`"),
        ("Выбери верный вариант:", ("She usually watch videos at night.", "She usually watches videos at night.", "She usually watching videos at night."), 1, "С `she` нужен `watches`."),
        ("Что звучит правильно?", ("Do they have lunch at school?", "Does they have lunch at school?", "Do they has lunch at school?"), 0, "С `they` используем `Do`."),
        ("Какое предложение правильное?", ("My friends lives near school.", "My friends live near school.", "My friends living near school."), 1, "С `friends` глагол без `-s`."),
        ("Выбери правильный вопрос:", ("Does your brother play basketball?", "Does your brother plays basketball?", "Do your brother play basketball?"), 0, "С `brother` нужен `Does + play`."),
        ("Что звучит правильно?", ("I don't like getting up early.", "I doesn't like getting up early.", "I not like getting up early."), 0, "С `I` используем `don't`."),
        ("Какой вариант нормальный?", ("She doesn't get home late.", "She don't get home late.", "She doesn't gets home late."), 0, "После `doesn't` — базовый глагол."),
        ("Выбери правильное предложение:", ("We usually finish school at two.", "We usually finishes school at two.", "We are usually finish school at two."), 0, "С `we` — обычный глагол без `-s`."),
        ("Что звучит правильно?", ("Does he do homework after school?", "Does he does homework after school?", "Do he do homework after school?"), 0, "С `he` нужен `Does`, а дальше базовый глагол."),
        ("Что звучит правильно?", ("My dad drives to work every day.", "My dad drive to work every day.", "My dad driving to work every day."), 0, "С `my dad` нужен `drives`."),
        ("Выбери правильный порядок слов:", ("She always gets up early.", "She gets always up early.", "Always she gets up early."), 0, "Наречие частоты обычно идет перед основным глаголом."),
        ("Что звучит правильно?", ("Do your parents work on weekends?", "Does your parents work on weekends?", "Do your parents works on weekends?"), 0, "С `parents` используем `Do`."),
        ("Что звучит правильно?", ("He rarely misses class.", "He rarely misses class.", "He rarely missing class."), 1, "Глагол `miss` с `he` превращается в `misses`."),
    ],
)


GRAMMAR_PLUS = _tasks(
    "grammar_plus",
    "grammar",
    [
        ("Что звучит естественнее?", ("He usually ends up doing homework late at night.", "He usually end up doing homework late at night.", "He usually ending up doing homework late at night."), 0, "С `he` нужен `ends up`."),
        ("Выбери лучший вопрос:", ("How often do you actually revise vocabulary?", "How often are you actually revise vocabulary?", "How often does you actually revise vocabulary?"), 0, "С `you` нужен `do`, а потом базовый глагол."),
        ("Что звучит правильно?", ("She doesn't really enjoy group projects.", "She don't really enjoy group projects.", "She doesn't really enjoys group projects."), 0, "После `doesn't` идет базовая форма `enjoy`."),
        ("Какой вариант лучше?", ("My brother hardly ever checks his messages in class.", "My brother hardly ever check his messages in class.", "My brother hardly ever checking his messages in class."), 0, "С `my brother` нужен `checks`."),
        ("Что звучит правильно?", ("Do you normally get things done on time?", "Are you normally get things done on time?", "Does you normally get things done on time?"), 0, "С `you` в Present Simple — `Do you ... ?`."),
        ("Какой вариант естественнее?", ("She usually puts things off until the last minute.", "She usually put things off until the last minute.", "She usually is putting things off until the last minute."), 0, "`puts` нужен из-за `she`."),
        ("Что лучше звучит?", ("I don't always stick to my routine.", "I doesn't always stick to my routine.", "I don't always sticks to my routine."), 0, "С `I` используем `don't`."),
        ("Выбери правильный вопрос:", ("Why does he keep missing the bus?", "Why do he keep missing the bus?", "Why does he keeps missing the bus?"), 0, "С `he` нужен `does`, а дальше базовая форма `keep`."),
        ("Что звучит грамотно?", ("My classmates often complain about early classes.", "My classmates often complains about early classes.", "My classmates often complaining about early classes."), 0, "С множественным числом — базовый глагол."),
        ("Какой вариант лучше?", ("Do your teachers expect too much homework sometimes?", "Does your teachers expect too much homework sometimes?", "Do your teachers expects too much homework sometimes?"), 0, "С `teachers` нужен `Do`."),
        ("Что правильно?", ("He never skips breakfast before exams.", "He never skip breakfast before exams.", "He never skipping breakfast before exams."), 0, "С `he` нужен `skips`."),
        ("Что звучит естественнее?", ("I usually need a while to wake up properly.", "I usually needs a while to wake up properly.", "I usually am need a while to wake up properly."), 0, "С `I` обычная форма `need`."),
        ("Какой вопрос составлен правильно?", ("What kind of music does she listen to while studying?", "What kind of music does she listens to while studying?", "What kind of music do she listen to while studying?"), 0, "После `does` глагол всегда в базовой форме."),
        ("Что лучше?", ("We rarely have enough time to finish everything in class.", "We rarely has enough time to finish everything in class.", "We rarely having enough time to finish everything in class."), 0, "С `we` используем обычную форму `have`."),
        ("Что звучит правильно?", ("My schedule looks fine on paper but falls apart by evening.", "My schedule look fine on paper but fall apart by evening.", "My schedule is look fine on paper but falls apart by evening."), 0, "С `schedule` нужен `looks`."),
        ("Какой вариант естественнее?", ("He usually works better under pressure than I do.", "He usually work better under pressure than I do.", "He usually is working better under pressure than I do."), 0, "С `he` — `works`."),
        ("Что звучит правильно?", ("Do you sometimes feel like the day just disappears?", "Does you sometimes feel like the day just disappears?", "Do you sometimes feels like the day just disappears?"), 0, "С `you` — `Do you feel ... ?`."),
        ("Выбери лучший вариант:", ("She often comes across as confident even when she's tired.", "She often come across as confident even when she's tired.", "She often coming across as confident even when she's tired."), 0, "С `she` нужен `comes`."),
        ("Что лучше звучит?", ("My friends usually back me up when school gets rough.", "My friends usually backs me up when school gets rough.", "My friends usually backing me up when school gets rough."), 0, "С `friends` — базовый глагол `back`."),
        ("Какой вариант грамотно собран?", ("He doesn't always realize how much time he wastes online.", "He doesn't always realizes how much time he wastes online.", "He don't always realize how much time he wastes online."), 0, "После `doesn't` — `realize`, без `-s`."),
    ],
)


DIALOGUE_A2 = _tasks(
    "dialogue_a2",
    "dialogue",
    [
        ("Friend: `What time do you get home?` Как ответить лучше всего?", ("I get home at about four.", "I home at four get.", "At four home I."), 0, "Естественный ответ: `I get home at about four.`"),
        ("Teacher: `Do you usually have lunch at school?`", ("Yes, I usually do.", "Yes, I usually have.", "Yes, usually lunch."), 0, "Короткий и естественный ответ: `Yes, I usually do.`"),
        ("Friend: `Do you like English?`", ("Yeah, I do. It's fun.", "Yeah, I am like English.", "Yeah, like."), 0, "Коротко и естественно: `Yeah, I do. It's fun.`"),
        ("Teacher: `Are you late again?`", ("No, I'm on time.", "No, I late.", "No, I am time."), 0, "Естественно: `No, I'm on time.`"),
        ("Friend: `What do you do after school?`", ("I usually go home and chill a bit.", "I usually home and chill.", "Usually go home and chill I."), 0, "Нормальный разговорный ответ."),
        ("Classmate: `Can you help me with homework?`", ("Sure, no problem.", "Yes, I can helping.", "Sure, I help you now maybe yes."), 0, "Коротко и нормально: `Sure, no problem.`"),
        ("Friend: `Do you play games in the evening?`", ("Sometimes, yeah.", "Sometimes I am.", "Yes, I play games in evening sometimes am."), 0, "Простой естественный ответ: `Sometimes, yeah.`"),
        ("Teacher: `Why are you tired today?`", ("I go to bed late.", "I late bed go.", "I am go bed late."), 0, "Правильно: `I go to bed late.`"),
        ("Friend: `Wanna hang out after school?`", ("Yeah, sounds good.", "Yes, I am hang out.", "I sounds good yes hang out."), 0, "Естественная реакция: `Yeah, sounds good.`"),
        ("Teacher: `Do you understand this exercise?`", ("Not really. Can you explain it again?", "No really understand.", "Can again explain you?"), 0, "Так звучит живо и грамотно."),
        ("Friend: `What's your favorite subject?`", ("Probably English.", "Favorite subject probably is.", "I subject favorite English."), 0, "Короткий естественный ответ."),
        ("Classmate: `Do you have plans tonight?`", ("Yeah, I need to finish homework.", "Yeah, I am finish homework.", "Need finish homework yes I."), 0, "Нормально: `Yeah, I need to finish homework.`"),
        ("Teacher: `Do you usually read in English?`", ("A little, but not every day.", "A little, but not every day I am.", "Little not every day."), 0, "Живой и понятный ответ."),
        ("Friend: `How do you get to school?`", ("I usually walk.", "I usually by walk.", "Usually I am walk."), 0, "Простой правильный ответ: `I usually walk.`"),
        ("Friend: `Are you free this evening?`", ("Maybe a bit later.", "Maybe I am free later a bit.", "Later maybe bit."), 0, "Коротко и естественно: `Maybe a bit later.`"),
        ("Teacher: `Why didn't you answer the question?`", ("I wasn't sure, sorry.", "I not sure, sorry.", "I wasn't sure am sorry."), 0, "Нормальный ответ: `I wasn't sure, sorry.`"),
        ("Friend: `Do you want to study together?`", ("Yeah, that could help.", "Yeah, that can helps.", "Yeah, help could that."), 0, "Нормально: `Yeah, that could help.`"),
        ("Teacher: `Can you say that again in English?`", ("Give me a second.", "Give me second a.", "I give a second me."), 0, "Естественно: `Give me a second.`"),
        ("Friend: `How was school today?`", ("Pretty normal, just a bit tiring.", "Pretty normal, just tiring bit a.", "School was pretty normal a bit tiring."), 0, "Живой короткий ответ."),
        ("Classmate: `You look stressed.`", ("Yeah, I've got a lot to do.", "Yeah, I got lot to do.", "Yeah, a lot to do I've got."), 0, "Нормально: `Yeah, I've got a lot to do.`"),
    ],
)


DIALOGUE_PLUS = _tasks(
    "dialogue_plus",
    "dialogue",
    [
        ("Friend: `How do you keep up with school and everything else?`", ("I try not to fall behind and plan things out.", "I try not fall behind and plan things out.", "I am try not to fall behind."), 0, "Нормально: `I try not to fall behind and plan things out.`"),
        ("Teacher: `Why do you think this topic matters?`", ("Because it actually shows how people use language in real life.", "Because it actually show how people use language in real life.", "Because it showing real life language."), 0, "С `it` нужен `shows`."),
        ("Friend: `Do you ever feel like you're just memorizing stuff?`", ("Yeah, sometimes, and that's when I stop understanding the point.", "Yeah, sometimes, and that's when I stops understanding the point.", "Yeah, sometimes and I stop understand point."), 0, "Первый вариант звучит и живо, и грамотно."),
        ("Teacher: `Can you explain your answer?`", ("Sure. I chose it because the tense matches a regular action.", "Sure. I chose it because the tense match a regular action.", "Sure because tense regular action."), 0, "Нормальный развернутый ответ."),
        ("Friend: `Why are you so into improving your English now?`", ("Because I want it to sound natural, not textbook-ish.", "Because I want it sound natural, not textbook-ish.", "Because natural not textbook I want."), 0, "Первый вариант естественнее."),
        ("Classmate: `That task looked brutal. You okay?`", ("Yeah, it was rough, but I got through it.", "Yeah, it was rough, but I got through.", "Yeah, rough but I got through it was."), 0, "`I got through it` — естественный вариант."),
        ("Teacher: `What's the difference between these two forms?`", ("One sounds like a routine, and the other feels more temporary.", "One sound like a routine, and the other feels more temporary.", "One is routine other temporary feels."), 0, "С `one` нужен `sounds`."),
        ("Friend: `Do you actually use English outside class?`", ("Yeah, mostly online, and that's where it starts to feel real.", "Yeah, mostly online, and that's where it start to feel real.", "Yeah mostly online and there it feel real."), 0, "Первый вариант звучит чище."),
        ("Teacher: `Why is this option wrong?`", ("Because after `doesn't` you need the base verb, not the `-s` form.", "Because after `doesn't` you needs the base verb, not the `-s` form.", "Because base verb after doesn't."), 0, "Здесь важна конструкция `you need`, не `you needs`."),
        ("Friend: `What part of English still gets on your nerves?`", ("Probably prepositions. They look random until they finally click.", "Probably prepositions. They looks random until they finally click.", "Probably prepositions they random until click."), 0, "С `they` нужен базовый глагол `look`."),
        ("Teacher: `Can you make your answer more precise?`", ("Yeah. It's not about the action itself, it's about when or how often it happens.", "Yeah. It's not about the action itself, it's about when or how often it happen.", "Yeah it about when or how often it happens."), 0, "С `it` нужен `happens`."),
        ("Friend: `Do you learn better by doing tasks or by reading theory?`", ("By doing, definitely. I remember things better when I use them.", "By doing, definitely. I remembers things better when I use them.", "By doing definitely I remember things better when use."), 0, "Первый вариант звучит естественно."),
        ("Classmate: `You sound way more confident now.`", ("Yeah, I think I'm finally starting to trust what I know.", "Yeah, I think I'm finally start to trust what I know.", "Yeah I finally starting trust what I know."), 0, "Нормально: `I'm finally starting to trust ...`"),
        ("Teacher: `What would you say instead?`", ("I'd probably make it shorter and more natural.", "I'd probably makes it shorter and more natural.", "I'd probably shorter and more natural."), 0, "После `I'd probably` нужен базовый глагол."),
        ("Friend: `Do you ever overthink grammar?`", ("All the time, and then I realize the simpler version is usually better.", "All the time, and then I realizes the simpler version is usually better.", "All time then simpler version better."), 0, "С `I` — `realize`, не `realizes`."),
        ("Teacher: `How can you tell this is a routine?`", ("Because the sentence talks about something that happens regularly.", "Because the sentence talk about something that happens regularly.", "Because it regular routine."), 0, "С `sentence` нужен `talks`."),
        ("Friend: `What helps you remember new words?`", ("Seeing them in context and then using them right away.", "Seeing them in context and then use them right away.", "Context and use right away."), 0, "Первый вариант полноценный и естественный."),
        ("Teacher: `Would you say this answer is formal or casual?`", ("More casual. It sounds like something a real person would actually say.", "More casual. It sound like something a real person would actually say.", "More casual because real person say."), 0, "С `it` нужен `sounds`."),
        ("Friend: `What's your plan for getting to B2?`", ("Keep building consistency, stop panicking, and actually speak more.", "Keep building consistency, stop panicking, and actually speaks more.", "Keep consistency and speak more actually."), 0, "После `keep / stop / speak` здесь нужны базовые формы."),
        ("Teacher: `Can you sum it up in one line?`", ("Sure: the grammar matters, but clarity matters more.", "Sure: the grammar matter, but clarity matters more.", "Sure grammar matters but clarity more."), 0, "С `grammar` и `clarity` нужен `matters`."),
    ],
)


MISTAKE_HUNT_A2 = _tasks(
    "mistake_hunt_a2",
    "grammar_control",
    [
        ("Найди правильную фразу:", ("He go to school every day.", "He goes to school every day.", "He going to school every day."), 1, "С `he / she / it` в Present Simple нужен глагол с `-s`."),
        ("Найди правильную фразу:", ("She don't like math.", "She doesn't like math.", "She doesn't likes math."), 1, "После `doesn't` глагол идет в базовой форме: `like`."),
        ("Найди правильный вопрос:", ("Do he play football?", "Does he play football?", "Does he plays football?"), 1, "С `he` нужен `does`, а смысловой глагол остается без `-s`."),
        ("Найди правильную фразу:", ("I doesn't get up late.", "I don't gets up late.", "I don't get up late."), 2, "С `I` берем `don't`, а дальше базовый глагол `get`."),
        ("Найди правильный вопрос:", ("What time do you get home?", "What time you get home?", "What time does you get home?"), 0, "Вопрос в Present Simple строится через `do/does` перед подлежащим."),
        ("Найди более естественный порядок слов:", ("She usually is tired after school.", "She is usually tired after school.", "Usually she tired after school."), 1, "Наречие частоты обычно ставится после `to be`: `is usually`."),
        ("Найди правильную фразу:", ("I go to school every day.", "I am go to school every day.", "I going to school every day."), 0, "Для регулярного действия здесь нужен обычный Present Simple."),
        ("Найди правильную фразу:", ("We plays games in the evening.", "We play games in the evening.", "We are play games in the evening."), 1, "С `we` глагол идет без `-s`: `play`."),
        ("Найди правильную фразу:", ("I have homework today.", "I have a homework today.", "I am having homework today."), 0, "`Homework` обычно неисчисляемое, без артикля `a`."),
        ("Найди правильную фразу:", ("She is good in English.", "She is good at English.", "She is good on English."), 1, "Устойчивая связка: `good at`."),
        ("Найди правильную фразу:", ("He watches videos at night.", "He watchs videos at night.", "He watching videos at night."), 0, "У `watch` в форме для `he` появляется `-es`: `watches`."),
        ("Найди правильную фразу:", ("They doesn't live here.", "They don't live here.", "They don't lives here."), 1, "С `they` нужен `don't`, дальше базовая форма `live`."),
        ("Найди правильную фразу:", ("My friend has a new phone.", "My friend have a new phone.", "My friend having a new phone."), 0, "С `my friend` как с `he/she`: `has`."),
        ("Найди более естественный порядок слов:", ("I am always late.", "I always am late.", "I late am always."), 0, "С `to be` наречие частоты ставится после формы `am/is/are`: `am always`."),
        ("Найди правильный вопрос:", ("Does they study English?", "Do they study English?", "Do they studies English?"), 1, "С `they` нужен `do`, а глагол остается `study`."),
        ("Найди правильную фразу:", ("She goes to bed at 11.", "She go to bed at 11.", "She going to bed at 11."), 0, "Для привычки с `she` нужен глагол `goes`."),
        ("Найди правильную фразу:", ("I listen music every day.", "I listen to music every day.", "I am listen to music every day."), 1, "С `listen` нужен предлог `to`: `listen to music`."),
        ("Найди правильную фразу:", ("He doesn't usually eat breakfast.", "He don't usually eat breakfast.", "He doesn't usually eats breakfast."), 0, "После `doesn't` — базовый глагол `eat`."),
        ("Найди правильную фразу:", ("We like this subject.", "We are like this subject.", "We likes this subject."), 0, "Здесь обычный глагол `like`, без `are`."),
        ("Найди правильный вопрос:", ("What does this word mean?", "What does mean this word?", "What do this word mean?"), 0, "Нормальный порядок: question word + does + subject + verb."),
    ],
)


MISTAKE_HUNT_PLUS = _tasks(
    "mistake_hunt_plus",
    "grammar_control",
    [
        ("Выбери грамотно собранную фразу:", ("She usually gets distracted when her phone keeps buzzing.", "She usually get distracted when her phone keeps buzzing.", "She usually gets distracted when her phone keep buzzing."), 0, "С `she` нужны формы `gets` и `keeps`."),
        ("Выбери правильную фразу:", ("He doesn't really get why this answer sounds unnatural.", "He doesn't really gets why this answer sounds unnatural.", "He don't really get why this answer sounds unnatural."), 0, "После `doesn't` нужен базовый глагол `get`."),
        ("Выбери правильный вопрос:", ("Why does this sentence sound more natural?", "Why do this sentence sound more natural?", "Why does this sentence sounds more natural?"), 0, "С `this sentence` нужен `does`, а `sound` остается базовым."),
        ("Выбери более естественный порядок слов:", ("I usually feel half-asleep during the first lesson.", "I feel usually half-asleep during the first lesson.", "Usually I feel half-asleep during the first lesson every always."), 0, "Наречие `usually` ставится перед смысловым глаголом."),
        ("Выбери правильную фразу:", ("My routine falls apart if I stay up too late.", "My routine fall apart if I stay up too late.", "My routine is fall apart if I stay up too late."), 0, "С `routine` нужен глагол `falls`."),
        ("Выбери правильную фразу:", ("I don't always manage to finish everything on time.", "I doesn't always manage to finish everything on time.", "I don't always manages to finish everything on time."), 0, "С `I` — `don't`, после него базовая форма `manage`."),
        ("Выбери правильную фразу:", ("She is usually more focused in the evening.", "She usually is more focused in the evening.", "She usually more focused in the evening is."), 0, "С `to be` звучит чище `is usually`."),
        ("Выбери правильный вопрос:", ("Do you ever feel like you're memorizing instead of understanding?", "Does you ever feel like you're memorizing instead of understanding?", "Do you ever feels like you're memorizing instead of understanding?"), 0, "С `you` нужен `do`, а глагол — `feel`."),
        ("Выбери правильную фразу:", ("He wastes too much time online before bed.", "He waste too much time online before bed.", "He is waste too much time online before bed."), 0, "С `he` нужен `wastes`."),
        ("Выбери правильную фразу:", ("This explanation actually makes sense.", "This explanation actually make sense.", "This explanation actually is make sense."), 0, "С `this explanation` нужен `makes`."),
        ("Выбери правильную фразу:", ("They don't always notice small grammar mistakes.", "They doesn't always notice small grammar mistakes.", "They don't always notices small grammar mistakes."), 0, "С `they` нужен `don't`, дальше `notice`."),
        ("Выбери правильный вопрос:", ("What helps you stay consistent with English?", "What help you stay consistent with English?", "What does helps you stay consistent with English?"), 0, "Подлежащее `what` здесь требует форму `helps`."),
        ("Выбери правильную фразу:", ("She says her answers sound too textbook-ish.", "She say her answers sound too textbook-ish.", "She says her answers sounds too textbook-ish."), 0, "С `she` — `says`, но `answers sound`, потому что `answers` во множественном числе."),
        ("Выбери более естественную фразу:", ("I keep forgetting prepositions even when I know the rule.", "I keep forget prepositions even when I know the rule.", "I forgetting prepositions even when I know the rule keep."), 0, "После `keep` здесь естественно звучит `forgetting`."),
        ("Выбери правильную фразу:", ("He doesn't usually speak much in the morning.", "He don't usually speak much in the morning.", "He doesn't usually speaks much in the morning."), 0, "После `doesn't` — базовый глагол `speak`."),
        ("Выбери правильную фразу:", ("This topic still feels confusing until you see it in context.", "This topic still feel confusing until you see it in context.", "This topic still is feel confusing until you see it in context."), 0, "С `this topic` нужен `feels`."),
        ("Выбери правильный вопрос:", ("How often do you actually revise vocabulary?", "How often are you actually revise vocabulary?", "How often does you actually revise vocabulary?"), 0, "Здесь нужен обычный вопрос через `do`."),
        ("Выбери правильную фразу:", ("My friend has trouble staying focused after lunch.", "My friend have trouble staying focused after lunch.", "My friend is have trouble staying focused after lunch."), 0, "С `my friend` нужна форма `has`."),
        ("Выбери правильную фразу:", ("I don't want my English to sound robotic.", "I doesn't want my English to sound robotic.", "I don't want my English sounds robotic."), 0, "После `don't want` идет инфинитив: `to sound`."),
        ("Выбери правильную фразу:", ("That answer works better because it actually fits the context.", "That answer work better because it actually fits the context.", "That answer works better because it actually fit the context."), 0, "С `that answer` — `works`, с `it` — `fits`."),
    ],
)


FAST_DIALOGUE_A2 = _tasks(
    "fast_dialogue_a2",
    "dialogue_reaction",
    [
        ("Friend: `How are you today?`", ("Pretty good, just a bit tired.", "I am pretty because tired.", "Goodly today tired."), 0, "Короткий живой ответ звучит естественно и по делу."),
        ("Classmate: `What time does your first lesson start?`", ("At eight thirty.", "In eight thirty.", "On eight thirty."), 0, "Про время начала — `at eight thirty`."),
        ("Friend: `Do you like this teacher?`", ("Yeah, she's strict but fair.", "Yeah, she strict but fair.", "Yeah, she is strict but fair teacherly."), 0, "Нормальный живой ответ с коротким пояснением звучит лучше."),
        ("Classmate: `Can you help me with this task?`", ("Sure, give me a second.", "Sure, give to me second.", "Sure, I help maybe task."), 0, "Так обычно и отвечают в живом диалоге."),
        ("Friend: `Why are you so quiet today?`", ("I'm just a bit sleepy.", "I just a bit sleepy.", "Just sleepy I am a bit."), 0, "С `I am` ответ звучит нормально и естественно."),
        ("Classmate: `What do you usually do after school?`", ("I usually go home, eat, and then do homework.", "I usually go home, eat, and then doing homework.", "Usually go home eat and homework."), 0, "Простой, но естественный распорядок в нормальном порядке слов."),
        ("Friend: `Are you coming with us?`", ("Maybe later, I need to finish this first.", "Maybe later, I need finish this first.", "Later maybe I finish first this."), 0, "Хороший разговорный ответ: коротко и с причиной."),
        ("Teacher: `Do you know the answer?`", ("I think so, but I'm not totally sure.", "I think so, but I'm not total sure.", "I think yes but not sure total."), 0, "Такой ответ звучит живо и честно."),
        ("Classmate: `What subject do you find hardest?`", ("Probably physics. It takes me the most time.", "Probably physics. It take me the most time.", "Probably physics because most time take."), 0, "Хороший вариант: короткий ответ плюс пояснение."),
        ("Friend: `Why are you late?`", ("The bus was slow and I missed the light.", "Bus was slow and I missed light.", "I late because the bus slow."), 0, "Первый вариант звучит полнее и естественнее."),
        ("Classmate: `Do you want to sit here?`", ("Yeah, that's fine.", "Yeah, this is sit fine.", "Fine here sit yeah."), 0, "Такой короткий ответ естественный для живого диалога."),
        ("Friend: `How often do you revise English?`", ("A few times a week, if I'm being honest.", "A few times in week, if I'm being honest.", "Few times week honest."), 0, "Здесь хорошо работает естественная фраза `a few times a week`."),
        ("Teacher: `What are you doing right now?`", ("I'm trying to finish the last question.", "I trying to finish the last question.", "Trying finish last question now."), 0, "Для действия сейчас нужен `I'm trying`."),
        ("Classmate: `Can I borrow your pen?`", ("Yeah, sure. Here you go.", "Yeah, sure. Take you go.", "Sure here go."), 0, "Готовая живая реплика без лишней тяжести."),
        ("Friend: `Did you do the homework?`", ("Yeah, I finished it last night.", "Yeah, I finish it last night.", "Yeah finished it last night."), 0, "Для вчерашнего результата нужен Past Simple: `finished`."),
        ("Classmate: `What do you think about online classes?`", ("They're okay, but I lose focus faster.", "They okay, but I lose focus faster.", "Okay but faster lose focus."), 0, "Хороший короткий ответ с мнением."),
        ("Friend: `Are you ready for the test?`", ("More or less. I revised, but I'm still nervous.", "More or less. I revised, but I still nervous.", "More less revised but nervous."), 0, "Такой ответ звучит естественно и по-человечески."),
        ("Classmate: `Do you prefer studying alone or with someone?`", ("Usually alone. I focus better that way.", "Usually alone. I focuses better that way.", "Usually alone because focus better."), 0, "С `I` нужен `focus`, не `focuses`."),
        ("Friend: `What are your plans for tonight?`", ("Probably just relax and get some sleep.", "Probably just relaxing and get some sleep.", "Probably relax and sleep some."), 0, "Первый вариант короче и звучит живее."),
        ("Teacher: `Why do you want to improve your English?`", ("Because I want to understand more and speak more freely.", "Because I want understand more and speak more freely.", "Because understand more and speak free."), 0, "После `want` нужен инфинитив: `to understand`, `to speak`."),
    ],
)


FAST_DIALOGUE_PLUS = _tasks(
    "fast_dialogue_plus",
    "dialogue_reaction",
    [
        ("Friend: `How's your energy today?`", ("Honestly, pretty low, but I'm still functioning.", "Honestly, pretty low, but I'm still function.", "Honestly low but still functioning I."), 0, "Такой ответ звучит живо и естественно."),
        ("Classmate: `Did that task make sense to you?`", ("Kind of, but I had to reread it twice.", "Kind of, but I had reread it twice.", "Kind of but reread twice."), 0, "Нормальный разговорный ответ с уточнением."),
        ("Friend: `Why do you sound more confident now?`", ("Because I'm starting to trust what I know.", "Because I'm starting trust what I know.", "Because start to trust what I know."), 0, "После `starting` нужен инфинитив `to trust`."),
        ("Teacher: `Can you explain your choice?`", ("Yeah. It matches a regular action, not something happening now.", "Yeah. It match a regular action, not something happening now.", "Yeah regular action not happening now."), 0, "С `it` нужен `matches`."),
        ("Friend: `Do you actually use English outside class?`", ("Mostly online, and that's where it starts feeling real.", "Mostly online, and that's where it start feeling real.", "Mostly online there it feeling real."), 0, "С `it` нужен `starts`."),
        ("Classmate: `What still messes with your head in grammar?`", ("Probably prepositions. They still feel random.", "Probably prepositions. They still feels random.", "Probably prepositions random still."), 0, "С `they` нужен базовый глагол `feel`."),
        ("Teacher: `What's the difference here?`", ("One sounds like a routine, the other feels temporary.", "One sound like a routine, the other feels temporary.", "One routine other temporary."), 0, "С `one` нужен `sounds`."),
        ("Friend: `How do you keep up with everything?`", ("I try not to panic and plan things out early.", "I try not panic and plan things out early.", "I not panic and plan early."), 0, "После `try` лучше звучит `to panic`, но весь первый вариант естественнее всего."),
        ("Teacher: `Can you make that answer stronger?`", ("Sure. I'd make it shorter and more natural.", "Sure. I'd makes it shorter and more natural.", "Sure shorter and more natural."), 0, "После `I'd` идет базовая форма `make`."),
        ("Friend: `Why are you suddenly taking English more seriously?`", ("Because I want it to sound real, not memorized.", "Because I want it sound real, not memorized.", "Because want sound real."), 0, "После `want` нужен инфинитив: `to sound`."),
        ("Classmate: `You looked lost in class. You okay?`", ("Yeah, I zoned out for a second, that's all.", "Yeah, I zone out for a second, that's all.", "Yeah zoned for second all."), 0, "Past Simple `zoned out` передает завершенное действие."),
        ("Teacher: `Why is this version better?`", ("Because it actually fits the context and sounds like real speech.", "Because it actually fit the context and sounds like real speech.", "Because fits context and real speech."), 0, "С `it` нужен `fits`."),
        ("Friend: `Do you overthink answers during tests?`", ("All the time, and then I realize the simpler one was fine.", "All the time, and then I realizes the simpler one was fine.", "All the time then realize simpler one."), 0, "С `I` нужен `realize`, не `realizes`."),
        ("Classmate: `What helps you remember new words?`", ("Seeing them in context and using them right away.", "Seeing them in context and use them right away.", "Context and use right away."), 0, "Параллельная конструкция `seeing ... and using ...` звучит естественно."),
        ("Teacher: `Can you sum it up in one line?`", ("Yeah: grammar matters, but clarity matters more.", "Yeah: grammar matter, but clarity matters more.", "Yeah grammar matters clarity more."), 0, "С `grammar` и `clarity` в этих фразах нужен `matters`."),
        ("Friend: `What throws you off in reading tasks?`", ("When I know the words but miss the actual point.", "When I know the words but miss the actual points.", "When know words but miss point."), 0, "Первый вариант точнее и естественнее."),
        ("Teacher: `What would you change here?`", ("I'd make the answer less stiff and more direct.", "I'd makes the answer less stiff and more direct.", "I'd less stiff and direct."), 0, "После `I'd` нужен базовый глагол `make`."),
        ("Classmate: `So what's your plan for B2?`", ("Keep showing up, stop panicking, and speak more.", "Keep showing up, stop panicking, and speaks more.", "Keep show up and speak more."), 0, "После `keep / stop / speak` здесь нужны базовые формы."),
        ("Friend: `Do you feel the difference now?`", ("Yeah, the answers sound less robotic than before.", "Yeah, the answers sounds less robotic than before.", "Yeah answers less robotic before."), 0, "С `answers` нужен `sound`, не `sounds`."),
        ("Teacher: `Why does this reply work well?`", ("Because it's clear, natural, and easy to say under pressure.", "Because it's clear, natural, and easy say under pressure.", "Because clear natural easy under pressure."), 0, "Связка `easy to say` делает ответ естественным."),
    ],
)


READING_A2 = _tasks(
    "reading_a2",
    "reading_meaning",
    [
        ("Текст: `Maks gets up at 7:00, grabs breakfast, and leaves home at 7:40.` Когда он выходит из дома?", ("At 7:00", "At 7:40", "At 8:00"), 1, "В тексте прямо сказано `leaves home at 7:40`."),
        ("Текст: `Nina likes English because the lessons feel more interactive than math.` Почему ей нравится английский?", ("Because it's easier than every subject.", "Because the lessons feel more interactive.", "Because her teacher gives less homework."), 1, "Ключевая причина дана прямо: `more interactive`."),
        ("Текст: `After school, Oleg usually eats, rests for half an hour, and only then starts homework.` Что он делает перед домашкой?", ("He goes for a run.", "He rests for half an hour.", "He watches a film."), 1, "В тексте сказано `rests for half an hour`."),
        ("Текст: `I can't hang out today. I need to finish a project before tomorrow.` Что предлагает автор?", ("Meet right now.", "Postpone hanging out.", "Skip the project."), 1, "Он отказывается на сегодня, значит встречу нужно перенести."),
        ("Текст: `Lena was late because the bus got stuck in traffic.` Почему она опоздала?", ("She overslept.", "The bus was delayed.", "She missed the alarm."), 1, "Причина указана прямо: `stuck in traffic`."),
        ("Текст: `Artem doesn't talk much in class, but he always helps people after lessons.` Что можно сказать об Артеме?", ("He is lazy.", "He is quiet but helpful.", "He hates school."), 1, "По тексту он неразговорчивый, но помогает другим."),
        ("Текст: `On Saturday, I cleaned my room, met a friend, and then played games at night.` Что было первым?", ("Meeting a friend.", "Cleaning the room.", "Playing games."), 1, "Сначала было `cleaned my room`."),
        ("Текст: `Sasha trains three times a week and usually feels better after practice.` Как часто он тренируется?", ("Three times a week.", "Every day.", "Only on weekends."), 0, "Частота названа прямо в первом предложении."),
        ("Текст: `We're going to the cinema on Friday. The tickets are already booked.` Что уже решено?", ("They might go somewhere.", "The cinema trip is planned.", "They need to ask their parents first."), 1, "Раз билеты уже забронированы, план уже подтвержден."),
        ("Текст: `I studied all evening, so now I just want to sleep.` Какое у автора настроение?", ("Relaxed and energetic.", "Tired.", "Angry."), 1, "По фразе `I just want to sleep` ясно, что он устал."),
        ("Текст: `Today was chaotic: two tests, one project, and almost no break.` Чего в дне было слишком много?", ("Free time.", "Work and pressure.", "Sports."), 1, "День описан как `chaotic`, с тестами и проектом."),
        ("Текст: `The lesson was hard because I understood the words, but not the idea.` В чем была проблема?", ("The vocabulary was too easy.", "The main idea was unclear.", "The teacher spoke too fast."), 1, "Проблема была не в словах, а в смысле."),
        ("Текст: `Hi, Ms Brown. I was sick yesterday, so I missed the test. Can I take it tomorrow?` Зачем пишет ученик?", ("To complain about the test.", "To ask for another chance.", "To say he doesn't want to do the test."), 1, "Он просит возможность написать тест позже."),
        ("Текст: `I started reading in English for fun, and now I don't translate every word in my head.` Какой вывод верный?", ("Reading made comprehension easier.", "Reading is boring for the author.", "The author stopped learning English."), 0, "По тексту видно, что читать стало легче и естественнее."),
        ("Текст: `The app gives me short tasks every day, which helps me stay consistent.` Почему автору нравится приложение?", ("It replaces school completely.", "It helps keep a routine.", "It teaches only grammar."), 1, "Ключевая польза — регулярность."),
        ("Текст: `My friend is loud in a good way. He keeps every conversation moving.` Какой у него характер?", ("Quiet and nervous.", "Energetic and social.", "Cold and distant."), 1, "Он явно активный и общительный."),
        ("Текст: `I missed the bus, so I had to walk for twenty minutes.` Что случилось потом?", ("The person stayed at home.", "The person walked.", "The person called a taxi."), 1, "Это прямо сказано во второй части предложения."),
        ("Текст: `I'm not scared of vocabulary tasks, but speaking still stresses me out.` Чего человек боится больше?", ("Speaking.", "Vocabulary.", "Reading."), 0, "Говорение `still stresses me out`."),
        ("Текст: `I'm learning English because I want to study abroad later and understand more online content now.` Зачем он учит английский?", ("Only for school marks.", "For future study and real-life use.", "Only because parents said so."), 1, "В тексте две реальные причины: учеба и контент."),
        ("Текст: `I don't love early mornings, but once I'm fully awake, my brain works much better.` Какой вывод можно сделать?", ("The person hates all studying.", "The start of the day is hard, but then it gets better.", "The person never wakes up properly."), 1, "Идея текста — тяжело начать, потом становится нормально."),
    ],
)


READING_PLUS = _tasks(
    "reading_plus",
    "reading_meaning",
    [
        ("Текст: `I used to panic when I saw long tasks, but now I break them into parts and deal with them one by one.` Что изменилось?", ("The tasks got shorter.", "The person changed strategy.", "The teacher lowered the level."), 1, "Смысл текста: изменился подход к задачам."),
        ("Текст: `The lesson wasn't hard because of vocabulary. It was hard because I couldn't see what the writer was really getting at.` В чем была проблема?", ("Unknown words.", "Hidden meaning.", "Bad handwriting."), 1, "Фраза `what the writer was really getting at` указывает на скрытый смысл."),
        ("Текст: `I still make grammar mistakes, but at least now I notice them before I send the message.` Какой прогресс уже есть?", ("Mistakes disappeared completely.", "Self-check became better.", "Grammar stopped mattering."), 1, "Человек стал лучше замечать свои ошибки до отправки."),
        ("Текст: `Our teacher doesn't simplify everything for us, which is annoying sometimes, but it also forces us to think.` Какое отношение у автора?", ("Only negative.", "Mixed, but mostly useful.", "Completely indifferent."), 1, "Есть раздражение, но и признание пользы."),
        ("Текст: `I can understand short videos pretty well now, but fast podcasts still completely destroy me.` Что пока остается сложным?", ("Short videos.", "Fast podcasts.", "Reading posts."), 1, "Проблема названа прямо: `fast podcasts`."),
        ("Текст: `When I answer too fast, I usually go with the first thing in my head, and that's when the answer sounds awkward.` Что мешает?", ("Lack of grammar rules.", "Rushing.", "No vocabulary."), 1, "Ключевая причина — спешка."),
        ("Текст: `At first I memorized phrases without understanding them. Now I try to notice the pattern behind them.` Что изменилось?", ("The person stopped learning phrases.", "The person moved from memorizing to understanding patterns.", "The person only studies vocabulary now."), 1, "Смысл в переходе от заучивания к пониманию паттернов."),
        ("Текст: `I don't sound fluent yet, but I definitely sound less robotic than I did a few months ago.` Какой вывод верный?", ("There is visible progress.", "The person thinks nothing changed.", "The person stopped speaking."), 0, "Сравнение с прошлым показывает реальный прогресс."),
        ("Текст: `I thought the text was about routine, but the last sentence showed it was actually about stress.` Что произошло?", ("The topic stayed the same all the way.", "The main idea shifted at the end.", "The writer made a grammar mistake."), 1, "Ключевая мысль раскрылась только в финале."),
        ("Текст: `Most of my mistakes happen when I know the rule in theory but don't have time to catch myself in the moment.` Что здесь главное?", ("Theory is useless.", "The gap is between knowledge and real-time use.", "The person never studies theory."), 1, "Проблема не в знании правила, а в применении под нагрузкой."),
        ("Текст: `I like tasks that make me choose between similar answers, because they show whether I really feel the difference.` Почему ему нравятся такие задания?", ("They are always easier.", "They test real understanding.", "They take less time."), 1, "Смысл — проверить тонкую разницу, а не угадывание."),
        ("Текст: `I don't need easier tasks. I need clearer feedback on why my answer sounds off.` Чего хочет автор?", ("Less work.", "More precise feedback.", "More vocabulary lists."), 1, "Запрос сформулирован прямо: нужен более точный фидбек."),
        ("Текст: `My answers got better when I stopped translating from Russian word by word.` Что помогло?", ("Direct translation.", "Thinking in chunks, not word by word.", "Learning fewer phrases."), 1, "По тексту видно, что дословный перевод мешал."),
        ("Текст: `The reply wasn't wrong exactly, but nobody would really say it like that.` Какой вывод лучше?", ("The answer was natural.", "The answer was grammatically possible but unnatural.", "The answer had only spelling mistakes."), 1, "Это различие между формальной правильностью и естественностью."),
        ("Текст: `The more examples I see in context, the less random the grammar feels.` Что делает грамматику понятнее?", ("Memorizing isolated rules only.", "Contextual examples.", "Skipping explanations."), 1, "В тексте прямо названы примеры в контексте."),
        ("Текст: `I still hesitate when I speak, but now the pause is shorter because I know what structure I want.` Что улучшилось?", ("Vocabulary disappeared.", "The response time became better.", "The person stopped thinking before speaking."), 1, "Пауза стала короче — это и есть прогресс."),
        ("Текст: `The sentence looked simple, but the trap was in the preposition, not the verb.` Где была ловушка?", ("In the verb.", "In the preposition.", "In word order only."), 1, "Это прямо сказано в тексте."),
        ("Текст: `When I reread my answer, I can usually hear whether it sounds like me or like a textbook.` Что он проверяет?", ("Only grammar endings.", "Naturalness of the answer.", "Whether the answer is long enough."), 1, "Смысл в проверке естественности звучания."),
        ("Текст: `I'm not aiming for perfect English every second. I just want solid, clear answers that sound real.` Какой у автора подход?", ("Perfection at any cost.", "Clear and natural over perfect.", "No standards at all."), 1, "Приоритет — ясность и естественность."),
        ("Текст: `The final check doesn't scare me as much now, because the build-up before it feels more logical.` Почему финал пугает меньше?", ("Because it got shorter.", "Because the preparation flow makes sense.", "Because the level dropped."), 1, "Ключевая причина — более логичная подготовка до финала."),
    ],
)


NATURAL_A2 = _tasks(
    "natural_a2",
    "natural_phrasing",
    [
        ("Что звучит живее?", ("I like English because it's useful and not boring.", "I like English. It is useful.", "English I like useful."), 0, "Первый вариант не рваный и звучит как нормальная живая реплика."),
        ("Что звучит естественнее?", ("My school day is usually busy, but okay.", "My school day is busy usually but okay.", "My school day okay busy."), 0, "Коротко, естественно и без ломаного порядка слов."),
        ("Что звучит лучше?", ("After school I usually eat first and then start homework.", "After school I usually first eat and then start homework.", "After school eat first homework start."), 0, "Это нормальный живой ответ с понятным порядком слов."),
        ("Что звучит естественнее?", ("He's my friend, and he's easy to talk to.", "He is my friend. He is nice.", "He friend and nice."), 0, "Первый вариант живее и звучит ближе к реальной речи."),
        ("Что лучше ответить?", ("I'm not sure yet, to be honest.", "I don't know.", "Know not I."), 0, "Первый вариант мягче и звучит естественнее."),
        ("Что звучит сильнее?", ("English matters because I use it outside school too.", "English is important.", "English important because yes."), 0, "Первый вариант дает причину и звучит содержательнее."),
        ("Что лучше?", ("I study a bit every day, so it doesn't pile up.", "I study every day.", "Every day study and done."), 0, "Первый вариант живее и объясняет смысл действия."),
        ("Что звучит естественнее?", ("My favorite subject is PE because it clears my head.", "My favorite subject is PE.", "Favorite subject PE."), 0, "Так ответ звучит не сухо, а по-человечески."),
        ("Что звучит лучше?", ("I'm tired because today felt way too long.", "I am tired.", "Tired I am today."), 0, "Первый вариант естественно добавляет контекст."),
        ("Что звучит живее?", ("I watch a lot of videos, mostly in the evening.", "I watch videos.", "I videos watch."), 0, "Первый вариант ближе к реальному ответу, а не к обрубку."),
        ("Что звучит лучше?", ("I want to get to B2 and actually feel confident.", "I want B2.", "I want to B2."), 0, "Первый вариант грамотно и естественно формулирует цель."),
        ("Что звучит естественнее?", ("This task is tricky, but I think I can handle it.", "This task is difficult.", "Task difficult."), 0, "Первый вариант звучит живо и не по-учебниковому."),
        ("Что звучит лучше?", ("I was late because the bus completely messed up my timing.", "I was late.", "Late I was."), 0, "Хороший живой ответ с причиной."),
        ("Что звучит естественнее?", ("I like music, especially when I need to reset.", "I like music.", "Music I like."), 0, "Первый вариант звучит полнее и натуральнее."),
        ("Что лучше?", ("I get to school at eight, so my mornings are pretty rushed.", "I go to school at 8.", "At 8 I school go."), 0, "Такой ответ звучит как реальная речь, а не просто факт."),
        ("Что звучит лучше?", ("My day was pretty normal, just a bit too packed.", "My day is normal.", "Day normal."), 0, "Первый вариант естественнее и точнее."),
        ("Что звучит естественнее?", ("I learn words faster when I see them in context.", "I learn words.", "Words I learn."), 0, "Появляется причина, и ответ звучит живее."),
        ("Что звучит лучше?", ("He's funny because he can make any situation less awkward.", "He is funny.", "Funny he is."), 0, "Первый вариант делает характеристику более живой."),
        ("Что звучит естественнее?", ("I don't like math much because it drains me fast.", "I don't like math.", "Math no like."), 0, "Первый вариант звучит натуральнее и дает понятную причину."),
        ("Что лучше ответить?", ("I'm a bit busy right now, but maybe later.", "I am busy.", "Busy now."), 0, "Первый вариант мягкий и естественный для диалога."),
    ],
)


NATURAL_PLUS = _tasks(
    "natural_plus",
    "natural_phrasing",
    [
        ("Что звучит естественнее?", ("I get the rule in theory, but it still slips when I answer too fast.", "I know the rule but I make mistakes.", "I know rule mistakes happen."), 0, "Первый вариант точнее и ближе к реальной речи."),
        ("Что звучит лучше?", ("My answers are getting cleaner, but they still sound stiff sometimes.", "My answers are better now.", "Answers better now."), 0, "Первый вариант точнее описывает прогресс."),
        ("Что звучит живее?", ("I don't need a perfect answer, just one that sounds real and clear.", "I need a good answer.", "Need good answer."), 0, "Это естественная формулировка приоритета."),
        ("Что звучит сильнее?", ("This topic made more sense once I saw it in actual context.", "This topic became clear.", "Topic clear now."), 0, "Первый вариант звучит более взросло и естественно."),
        ("Что звучит лучше?", ("I still hesitate, but now at least I know what I'm trying to say.", "I still hesitate sometimes.", "Still hesitate."), 0, "Первый вариант дает живой и содержательный ответ."),
        ("Что звучит естественнее?", ("That reply wasn't exactly wrong, just a bit too textbook-ish.", "That reply was wrong.", "Reply wrong."), 0, "Первый вариант лучше передает тонкую разницу."),
        ("Что звучит лучше?", ("I learn faster when I stop translating everything word by word.", "I learn faster when I practice more.", "Learn faster more practice."), 0, "Первый вариант точнее и интереснее как живая мысль."),
        ("Что звучит естественнее?", ("I'm trying to sound less robotic and more like an actual person.", "I want to sound natural.", "Want sound natural."), 0, "Первый вариант звучит живее и с характером."),
        ("Что звучит лучше?", ("Some answers look simple until you actually have to explain why they work.", "Some answers are difficult.", "Answers difficult."), 0, "Первый вариант глубже и ближе к экзаменационному мышлению."),
        ("Что звучит сильнее?", ("The wording matters because two similar answers can feel completely different.", "Words are important.", "Wording important."), 0, "Первый вариант объясняет мысль, а не просто констатирует."),
        ("Что звучит естественнее?", ("I don't want to just memorize patterns, I want to feel when they fit.", "I want to understand grammar.", "Want understand grammar."), 0, "Первый вариант более живой и точный."),
        ("Что звучит лучше?", ("This kind of task is useful because it shows what I actually notice under pressure.", "This task is useful.", "Task useful."), 0, "Первый вариант сильнее и содержательнее."),
        ("Что звучит естественнее?", ("I can hear the difference now, even if I can't always explain it instantly.", "I understand now.", "Now I understand."), 0, "Такой ответ звучит взрослее и реалистичнее."),
        ("Что звучит лучше?", ("The idea wasn't hard, but the way it was phrased threw me off.", "The text was hard.", "Text hard."), 0, "Первый вариант точнее показывает причину сбоя."),
        ("Что звучит живее?", ("I usually catch the mistake after I read the sentence one more time.", "I usually find mistakes.", "Usually find mistakes."), 0, "Первый вариант звучит как реальное наблюдение."),
        ("Что звучит лучше?", ("My goal isn't just B2 on paper — I want answers to come out naturally.", "I want B2.", "Want B2 level."), 0, "Первый вариант сильнее и звучит по-человечески."),
        ("Что звучит естественнее?", ("The simpler answer often works better if it still sounds natural.", "Simple answers are good.", "Simple answer good."), 0, "Первый вариант выражает мысль точнее."),
        ("Что звучит лучше?", ("I'm getting less scared of mistakes because now I actually see what went wrong.", "I'm not scared now.", "Not scared now."), 0, "Первый вариант живее и глубже."),
        ("Что звучит сильнее?", ("The whole point is not to sound perfect — it's to sound clear and real.", "The point is to sound good.", "Point sound good."), 0, "Первый вариант звучит как настоящая сильная мысль."),
        ("Что звучит естественнее?", ("I can feel when a sentence technically works but still sounds off.", "I know some sentences are wrong.", "Sentences wrong sometimes."), 0, "Первый вариант лучше отражает нужный языковой навык."),
    ],
)


WRITING_A2 = _tasks(
    "writing_a2",
    "writing_build",
    [
        ("Какое первое предложение лучше открыть мини-ответ на тему `My school morning`?", ("My school morning usually starts at seven.", "School morning seven.", "I morning school start."), 0, "Первый вариант — нормальное стартовое предложение для короткого ответа."),
        ("Какое предложение лучше продолжает тему `After school`?", ("After school, I usually eat first and then start homework.", "After school homework start eat.", "After school I usually start and eat homework."), 0, "Такой вариант звучит естественно и логично."),
        ("Какой вариант лучше для темы `My favorite subject`?", ("My favorite subject is English because it feels useful.", "My favorite subject English useful.", "Favorite subject is because useful English."), 0, "Первый вариант — цельное предложение с причиной."),
        ("Какой вариант лучше для темы `The hardest subject for me`?", ("Math is probably the hardest for me because I need more time with it.", "Math hardest because more time.", "Hardest math for me because time."), 0, "Нормальная фраза с пояснением звучит сильнее."),
        ("Как лучше начать ответ `Describe your best friend`?", ("My best friend is funny, calm, and easy to talk to.", "My best friend funny and calm.", "Best friend funny calm."), 0, "Первый вариант — хороший старт мини-описания."),
        ("Какое предложение лучше для темы `Why I want better English`?", ("I want better English because I use it outside school too.", "I want better English because outside school too.", "Want better English outside school."), 0, "Полноценная причина делает ответ сильнее."),
        ("Какой вариант лучше для темы `My evening routine`?", ("In the evening I usually finish homework and then try to relax a bit.", "In evening I finish homework and relax.", "Evening homework relax."), 0, "Первый вариант звучит связно и естественно."),
        ("Какой вариант лучше для темы `My weekends`?", ("On weekends I usually sleep longer and spend more time with friends.", "On weekends I sleep longer friends.", "Weekends sleep longer and friends."), 0, "Первый вариант — нормальная, связная мысль."),
        ("Какой вариант лучше для темы `A good day at school`?", ("A good day at school is when the lessons feel clear and not too heavy.", "Good day at school clear and not heavy.", "Good school day when clear."), 0, "Первый вариант звучит как естественное мнение."),
        ("Какой вариант лучше для темы `A day when I was tired`?", ("One day I was really tired because I slept too little the night before.", "One day tired because slept little.", "Day tired because little sleep."), 0, "Первый вариант — связная и понятная фраза."),
        ("Какой вариант лучше для темы `Apps I use in English`?", ("I use English mostly in apps, videos, and short posts online.", "I use English in apps online mostly posts.", "Use English apps videos posts."), 0, "Первый вариант звучит чище и логичнее."),
        ("Какой вариант лучше для темы `Study alone or with someone`?", ("I usually study alone because I focus better that way.", "I study alone because focus better.", "Study alone better focus."), 0, "Первый вариант цельный и естественный."),
        ("Какой вариант лучше для темы `When I don't understand a topic`?", ("When I don't understand a topic, I usually look for more examples.", "When I don't understand a topic, usually look examples.", "Don't understand topic look examples."), 0, "Первый вариант грамотно собран."),
        ("Какой вариант лучше для темы `Plans for this weekend`?", ("This weekend I'm going to rest a bit and catch up on homework.", "This weekend going to rest and catch homework.", "Weekend rest homework."), 0, "Первый вариант подходит для короткого writing-ответа."),
        ("Какой вариант лучше для темы `A teacher I remember`?", ("I remember one teacher well because she explained things very clearly.", "I remember teacher because explained clearly.", "Remember one teacher clear."), 0, "Первый вариант естественно звучит и дает причину."),
        ("Какой вариант лучше для темы `Interesting classes`?", ("Classes feel interesting when I actually understand why the task matters.", "Classes interesting when understand why task matters.", "Interesting classes when task matter."), 0, "Первый вариант звучит взрослее и связнее."),
        ("Какой вариант лучше для темы `What is difficult about speaking English`?", ("The hardest part is answering fast without freezing.", "Hardest part speaking English answer fast freezing.", "Speaking hard because fast."), 0, "Первый вариант короткий, но сильный."),
        ("Какой вариант лучше для темы `Grammar or vocabulary`?", ("Vocabulary feels easier for me, but grammar is more predictable.", "Vocabulary easier but grammar predictable.", "Vocabulary easier grammar predictable."), 0, "Первый вариант естественно сравнивает две вещи."),
        ("Какой вариант лучше для темы `My ideal English lesson`?", ("My ideal English lesson would be active, clear, and not overloaded.", "My ideal lesson active clear not overloaded.", "Ideal lesson active."), 0, "Первый вариант — хороший короткий ответ с тремя ясными характеристиками."),
        ("Какое финальное предложение лучше завершает короткий ответ?", ("That's why I want my English to sound more natural, not just correct.", "That's why I want English natural.", "That why English natural."), 0, "Первый вариант хорошо закрывает мысль и звучит по-человечески."),
    ],
)


WRITING_PLUS = _tasks(
    "writing_plus",
    "writing_build",
    [
        ("Какой вариант лучше открывает ответ `How I study English now`?", ("Right now I'm trying to build consistency instead of studying in random bursts.", "Right now trying to build consistency random bursts.", "Now build consistency not random."), 0, "Первый вариант звучит взрослее и логичнее."),
        ("Какой вариант лучше продолжает тему `My school routine`?", ("My routine is pretty stable on weekdays, but it falls apart on weekends.", "My routine stable weekdays but falls apart weekends.", "Routine weekdays stable weekends apart."), 0, "Первый вариант естественно сравнивает две ситуации."),
        ("Какой вариант лучше для темы `Why English matters to me`?", ("English matters because it connects school, online life, and my future plans.", "English matters because school online life future plans.", "English matters future school online."), 0, "Первый вариант цельный и содержательный."),
        ("Какой вариант лучше для темы `What still feels hard`?", ("What still feels hard is answering naturally when I have to think fast.", "Hard is answering naturally when think fast.", "Hard answer naturally fast."), 0, "Первый вариант звучит как нормальная письменная мысль."),
        ("Какой вариант лучше для темы `A strong answer`?", ("A strong answer is not just correct — it also sounds natural in context.", "Strong answer not just correct also natural context.", "Strong answer correct natural."), 0, "Первый вариант хорошо формулирует идею."),
        ("Какой вариант лучше для темы `My biggest mistake`?", ("My biggest mistake is translating too directly instead of thinking in chunks.", "My biggest mistake translating too directly.", "Biggest mistake direct translation."), 0, "Первый вариант звучит сильнее и точнее."),
        ("Какой вариант лучше для темы `How I revise`?", ("I revise better when I see the same pattern in a few different examples.", "I revise better when see same pattern examples.", "Revise better same pattern examples."), 0, "Первый вариант связан и естественен."),
        ("Какой вариант лучше для темы `A useful lesson`?", ("The most useful lessons are the ones that show why an answer works.", "Useful lessons show why answer works.", "Useful lesson why answer works."), 0, "Первый вариант звучит как нормальный письменный ответ."),
        ("Какой вариант лучше для темы `Reading in English`?", ("Reading helps because it shows me how real sentences actually flow.", "Reading helps because shows how real sentences flow.", "Reading helps real sentences flow."), 0, "Первый вариант дает сильную и ясную причину."),
        ("Какой вариант лучше для темы `Speaking pressure`?", ("Speaking feels hardest when I know the rule but can't use it in the moment.", "Speaking hardest when know rule but can't use moment.", "Speaking hard rule moment."), 0, "Первый вариант естественен и хорошо объясняет проблему."),
        ("Какой вариант лучше для темы `My progress`?", ("I still make mistakes, but now I notice more of them before it's too late.", "I still make mistakes but notice more before too late.", "Still mistakes but notice more."), 0, "Первый вариант звучит взрослее и логичнее."),
        ("Какой вариант лучше для темы `What helps most`?", ("What helps most is clear feedback, not just knowing whether I'm wrong.", "What helps most clear feedback not just wrong.", "Clear feedback helps most."), 0, "Первый вариант точнее и сильнее."),
        ("Какой вариант лучше для темы `A difficult task`?", ("A difficult task usually teaches more if I actually understand the mistake after it.", "Difficult task teaches more if understand mistake.", "Difficult task more mistake."), 0, "Первый вариант звучит как настоящая мысль, а не телеграмма."),
        ("Какой вариант лучше для темы `My goal`?", ("My goal is to make my English feel solid, clear, and natural under pressure.", "My goal solid clear natural English pressure.", "Goal natural English pressure."), 0, "Первый вариант хорошо звучит и закрывает тему."),
        ("Какой вариант лучше для темы `Why context matters`?", ("Context matters because the same grammar can feel different in real speech.", "Context matters because same grammar different in speech.", "Context matters grammar speech."), 0, "Первый вариант понятнее и естественнее."),
        ("Какой вариант лучше для темы `What throws me off`?", ("What throws me off most is when two answers are both almost right.", "What throws me off two answers almost right.", "Throws me off almost right answers."), 0, "Первый вариант хорошо передает сложность выбора."),
        ("Какой вариант лучше для темы `A better answer`?", ("A better answer is usually shorter, clearer, and less robotic.", "Better answer shorter clearer less robotic.", "Better answer less robotic."), 0, "Первый вариант звучит как хорошая письменная формулировка."),
        ("Какой вариант лучше для темы `How I want to sound`?", ("I want to sound like a real person, not like I'm reciting a rule.", "I want sound like real person not reciting rule.", "Want sound real person."), 0, "Первый вариант живой и естественный."),
        ("Какой вариант лучше для темы `Why consistency matters`?", ("Consistency matters because small daily steps work better than random panic sessions.", "Consistency matters because small daily steps better than panic.", "Consistency small steps better."), 0, "Первый вариант звучит зрелее и точнее."),
        ("Какой вариант лучше как финальная мысль?", ("That's why I care less about perfect wording and more about clear, natural answers.", "That's why perfect wording less and clear answers more.", "That's why clear answers more."), 0, "Первый вариант хорошо завершает короткий письменный ответ."),
    ],
)


CHECK_A2 = _tasks(
    "check_a2",
    "checkpoint",
    [
        ("Выбери лучший вариант для школьной переписки:", ("I won't make it today because I still have to finish a project.", "I won't make it today because I still have finish a project.", "I won't makes it today because I still have to finish a project."), 0, "После `have to` нужен базовый глагол `finish`, а `won't make it` — естественная фраза для отказа."),
        ("Какой вывод по фразе `I keep falling behind when I don't plan ahead` точнее?", ("Человек не любит планы вообще.", "Человек отстает, если не планирует заранее.", "Человек всегда всё успевает."), 1, "`fall behind` — это отставать, а `plan ahead` — планировать заранее."),
        ("Выбери грамотный вопрос:", ("Why does this answer sound too stiff?", "Why do this answer sound too stiff?", "Why does this answer sounds too stiff?"), 0, "С `this answer` нужен `does`, а смысловой глагол остается `sound`."),
        ("Что звучит естественнее как объяснение?", ("It isn't wrong, but nobody would really say it like that.", "It isn't wrong, but nobody would really says it like that.", "It isn't wrong, but nobody really say it like that."), 0, "С `would` нужен базовый глагол `say`, и весь ответ звучит естественно."),
        ("Что лучше передает смысл `I need a clearer structure, not easier tasks`?", ("Мне нужны задания полегче, а не структура.", "Мне нужна более понятная структура, а не более лёгкие задания.", "Мне не нужны никакие задания."), 1, "Здесь акцент именно на ясности структуры, а не на снижении сложности."),
        ("Выбери правильную фразу:", ("She usually figures it out after a second try.", "She usually figure it out after a second try.", "She usually figures out it after a second try."), 0, "С `she` нужен `figures`, а фразовый глагол здесь естественно звучит как `figures it out`."),
        ("Какой ответ лучше на вопрос `What still feels hard?`", ("Answering fast without losing clarity.", "Answering fast without lose clarity.", "Fast answering without clarity lose."), 0, "После `without` здесь естественно используется форма на `-ing`."),
        ("Что лучше объясняет разницу?", ("One answer is shorter, but the other sounds more natural.", "One answer are shorter, but the other sounds more natural.", "One shorter, other natural."), 0, "С `one answer` нужен `is`, и первый вариант звучит как нормальное пояснение."),
        ("Выбери корректную фразу:", ("My replies got better once I stopped translating every word.", "My replies got better once I stop translating every word.", "My replies get better once I stopped translating every word."), 0, "Past Simple `got / stopped` показывает завершенное изменение."),
        ("Что означает `The wording threw me off`?", ("Формулировка сбила меня.", "Формулировка помогла мне.", "Формулировка была слишком короткой."), 0, "`throw off` здесь означает сбить, запутать."),
        ("Выбери лучший вариант:", ("I don't want perfect English, I want clear English I can trust.", "I don't want perfect English, I wants clear English I can trust.", "I don't want perfect English, I want clear English I can trusts."), 0, "С `I` нужен `want`, а после `can` — базовый глагол `trust`."),
        ("Что звучит естественнее как мини-вывод?", ("The grammar matters, but the message matters too.", "The grammar matter, but the message matters too.", "Grammar matters, but message matter too."), 0, "С `grammar` и `message` в таких формулировках нужен `matters`."),
        ("Выбери правильный вопрос:", ("How do you know this one is the stronger option?", "How does you know this one is the stronger option?", "How do you knows this one is the stronger option?"), 0, "С `you` нужен `do`, а глагол — `know`."),
        ("Что лучше передает смысл `I can hear that it's off, even if I can't explain it instantly`?", ("Я сразу всё идеально объясняю.", "Я уже слышу, что что-то не так, даже если не могу сразу объяснить почему.", "Я не замечаю ошибки вообще."), 1, "Смысл в том, что чувство языка уже есть, даже если объяснение приходит не сразу."),
        ("Выбери естественный ответ:", ("It works better because it sounds more like real speech.", "It works better because it sound more like real speech.", "It works better because more real speech."), 0, "С `it` нужен `sounds`, и первый вариант звучит чисто."),
        ("Что означает `I don't want to freeze when I have to answer on the spot`?", ("Я не хочу теряться, когда нужно ответить сразу.", "Я не хочу сидеть на месте, когда отвечаю.", "Я не хочу писать ответ на бумаге."), 0, "`freeze` здесь — зависнуть, растеряться, а `on the spot` — сразу, на месте."),
        ("Выбери правильную фразу:", ("The more context I get, the less random the rule feels.", "The more context I get, the less random the rule feel.", "The more context I gets, the less random the rule feels."), 0, "С `rule` нужен `feels`, а с `I` — `get`."),
        ("Какой вариант лучше как финальная мысль?", ("At this point I care more about sounding natural than sounding impressive.", "At this point I cares more about sounding natural than sounding impressive.", "At this point care more about sounding natural."), 0, "С `I` нужен `care`, и первый вариант звучит как сильный вывод."),
        ("Что лучше описывает фразу `The task looked easy, but the trap was in the logic`?", ("Задача была сложной из-за словаря.", "Задача выглядела простой, но подвох был в логике.", "Задача была очень длинной."), 1, "Смысл в том, что сложность была не во внешнем виде, а в скрытой логике."),
        ("Выбери лучший ответ учителю:", ("I think the answer works, but the phrasing still feels a bit unnatural.", "I think the answer works, but the phrasing still feel a bit unnatural.", "I think answer works but phrasing unnatural."), 0, "С `phrasing` нужен `feels`, и первый вариант звучит как зрелый комментарий."),
    ],
)


CHECK_PLUS = _tasks(
    "check_plus",
    "checkpoint",
    [
        ("Выбери лучший вариант:", ("She tends to overthink when two answers look almost equally right.", "She tend to overthink when two answers look almost equally right.", "She tends overthink when two answers look almost equally right."), 0, "С `she` нужен `tends`, а после него естественно звучит `to overthink`."),
        ("Что ближе по смыслу к `The wording matters more than people think`?", ("Формулировка важнее, чем многим кажется.", "Формулировка ничего не решает.", "Люди всегда замечают формулировку."), 0, "Ключевая мысль — формулировка влияет сильнее, чем это обычно признают."),
        ("Выбери правильный вопрос:", ("Why does this version feel more natural even though it's shorter?", "Why do this version feel more natural even though it's shorter?", "Why does this version feels more natural even though it's shorter?"), 0, "С `this version` нужен `does`, а дальше — базовый глагол `feel`."),
        ("Что звучит сильнее как объяснение?", ("Because it sounds like something a real person would actually say under pressure.", "Because it sound like something a real person would actually say under pressure.", "Because real person would say under pressure."), 0, "С `it` нужен `sounds`, и первый вариант звучит как зрелое объяснение."),
        ("Что лучше передает смысл `I don't just want correct English — I want usable English`?", ("Мне нужен не просто правильный английский, а такой, которым можно реально пользоваться.", "Мне нужен только академический английский.", "Мне всё равно, как звучит английский."), 0, "Разница именно между формальной правильностью и практической пригодностью."),
        ("Выбери грамотную фразу:", ("He doesn't always notice when his answer sounds too stiff.", "He doesn't always notices when his answer sounds too stiff.", "He don't always notice when his answer sounds too stiff."), 0, "После `doesn't` нужен базовый глагол `notice`."),
        ("Что точнее описывает `The task wasn't hard, but the framing was tricky`?", ("Слова были трудные, но идея простая.", "Сама задача была несложной, но формулировка сбивала.", "Задача была длинной, но очевидной."), 1, "Смысл в том, что подвох был именно в подаче, а не в материале."),
        ("Выбери лучший ответ:", ("I can usually feel when a sentence works, even before I fully explain why.", "I can usually feels when a sentence works, even before I fully explain why.", "I usually feel when a sentence works even before fully explain why."), 0, "После `can` нужен базовый глагол `feel`."),
        ("Что звучит естественнее?", ("The shorter answer wins here because it stays clear and direct.", "The shorter answer win here because it stays clear and direct.", "Shorter answer wins because clear direct."), 0, "С `answer` нужен `wins`, а весь ответ звучит по-взрослому."),
        ("Что означает `I keep second-guessing myself in speaking tasks`?", ("Я постоянно сомневаюсь в себе в заданиях на говорение.", "Я легко и уверенно отвечаю в speaking tasks.", "Я забываю слова только при чтении."), 0, "`second-guessing myself` — это постоянно пересомневаться в себе."),
        ("Выбери правильную фразу:", ("The more examples I compare, the easier it gets to hear the difference.", "The more examples I compare, the easier it get to hear the difference.", "The more examples I compares, the easier it gets to hear the difference."), 0, "С `it` нужен `gets`, а с `I` — `compare`."),
        ("Что лучше как мини-вывод?", ("A strong answer isn't always longer — it's usually just sharper.", "A strong answer isn't always longer — it's usually just sharperer.", "Strong answer longer sharper."), 0, "Первый вариант звучит естественно и четко."),
        ("Выбери лучший вопрос:", ("How do you tell when an answer is technically right but still off?", "How does you tell when an answer is technically right but still off?", "How do you tells when an answer is technically right but still off?"), 0, "С `you` нужен `do`, а смысловой глагол — `tell`."),
        ("Что точнее передает смысл `I don't need easier prompts, I need better feedback loops`?", ("Мне не нужны подсказки вообще.", "Мне нужны не более лёгкие задания, а более полезная обратная связь.", "Мне нужно меньше английского."), 1, "Смысл именно в качестве обратной связи, а не в упрощении."),
        ("Выбери естественный ответ:", ("It works because the logic is cleaner, not because the words are fancier.", "It works because the logic are cleaner, not because the words are fancier.", "It works because logic cleaner not words fancy."), 0, "С `logic` нужен `is`, и первый вариант формулирует мысль сильно."),
        ("Что означает `That sentence is doing too much at once`?", ("В предложении слишком много всего сразу.", "Предложение слишком короткое.", "Предложение не связано с темой."), 0, "Идея в перегруженности конструкции."),
        ("Выбери правильную фразу:", ("My writing gets better when I stop trying to sound impressive all the time.", "My writing get better when I stop trying to sound impressive all the time.", "My writing gets better when I stops trying to sound impressive all the time."), 0, "С `writing` нужен `gets`, а с `I` — `stop`."),
        ("Что звучит лучше как сильная мысль?", ("At this level, noticing the difference matters almost as much as explaining it.", "At this level, noticing the difference matter almost as much as explaining it.", "At this level noticing difference matter."), 0, "С подлежащим `noticing the difference` нужен `matters`."),
        ("Что лучше описывает `The answer sounded safe, but not convincing`?", ("Ответ был аккуратный, но неубедительный.", "Ответ был грубый и агрессивный.", "Ответ был слишком длинный."), 0, "Здесь противопоставляется безопасная формулировка и убедительность."),
        ("Выбери лучший ответ учителю:", ("I think the content is fine, but the phrasing still needs tightening.", "I think the content are fine, but the phrasing still needs tightening.", "I think content fine but phrasing tightening."), 0, "С `content` в таком значении нужен `is`, и первый вариант звучит профессиональнее."),
    ],
)


PAST_EVENTS = _tasks(
    "past_events",
    "past_simple",
    [
        ("Выбери правильную фразу:", ("I watched a film last night.", "I watch a film last night.", "I watched a film last night yesterday."), 0, "С `last night` нужен Past Simple: `watched`."),
        ("Выбери правильную фразу:", ("She went to school yesterday.", "She goed to school yesterday.", "She goes to school yesterday."), 0, "У `go` в прошедшем времени форма `went`."),
        ("Выбери правильную фразу:", ("We had a test two days ago.", "We have a test two days ago.", "We had a test two days before."), 0, "С `two days ago` нужен Past Simple: `had`."),
        ("Выбери правильный вопрос:", ("Did you finish the project?", "Did you finished the project?", "Do you finish the project yesterday?"), 0, "После `did` глагол идет в базовой форме."),
        ("Выбери правильную фразу:", ("He didn't see the message.", "He didn't saw the message.", "He doesn't see the message yesterday."), 0, "После `didn't` нужен базовый глагол `see`."),
        ("Выбери правильную фразу:", ("I met my friend after class.", "I meet my friend after class yesterday.", "I meted my friend after class."), 0, "Прошедшее время от `meet` — `met`."),
        ("Выбери правильную фразу:", ("They stayed home because it rained.", "They stay home because it rained.", "They stayed home because it rain."), 0, "В прошедшем времени здесь `stayed` и `rained`."),
        ("Выбери правильную фразу:", ("She bought a new notebook last week.", "She buyed a new notebook last week.", "She buys a new notebook last week."), 0, "У `buy` форма Past Simple — `bought`."),
        ("Выбери правильную фразу:", ("I woke up late and missed the bus.", "I waked up late and missed the bus.", "I wake up late and missed the bus."), 0, "`wake up` в Past Simple — `woke up`."),
        ("Выбери правильный ответ:", ("Yes, I did.", "Yes, I was.", "Yes, I do."), 0, "На вопрос в Past Simple отвечаем через `did`."),
        ("Выбери правильную фразу:", ("He wrote the answer quickly.", "He writed the answer quickly.", "He writes the answer quickly yesterday."), 0, "Past Simple от `write` — `wrote`."),
        ("Выбери правильную фразу:", ("We left school at three.", "We leaved school at three.", "We leave school at three yesterday."), 0, "Past Simple от `leave` — `left`."),
        ("Выбери правильную фразу:", ("I didn't understand the task at first.", "I didn't understood the task at first.", "I don't understand the task at first."), 0, "После `didn't` — базовый глагол `understand`."),
        ("Выбери правильную фразу:", ("She told me the truth.", "She telled me the truth.", "She tells me the truth yesterday."), 0, "Past Simple от `tell` — `told`."),
        ("Выбери правильный вопрос:", ("Where did you go after school?", "Where did you went after school?", "Where do you go after school yesterday?"), 0, "После `did` нужен базовый глагол `go`."),
        ("Выбери правильную фразу:", ("They came late but still joined us.", "They comed late but still joined us.", "They come late but still joined us yesterday."), 0, "Past Simple от `come` — `came`."),
        ("Выбери правильную фразу:", ("I made a small mistake in the test.", "I maked a small mistake in the test.", "I make a small mistake in the test yesterday."), 0, "Past Simple от `make` — `made`."),
        ("Выбери правильную фразу:", ("She didn't bring her book.", "She didn't brought her book.", "She doesn't bring her book yesterday."), 0, "После `didn't` нужен базовый `bring`."),
        ("Выбери правильную фразу:", ("We spoke about it after class.", "We speaked about it after class.", "We speak about it after class yesterday."), 0, "Past Simple от `speak` — `spoke`."),
        ("Выбери правильную фразу:", ("I felt better after some rest.", "I feeled better after some rest.", "I feel better after some rest yesterday."), 0, "Past Simple от `feel` — `felt`."),
    ],
)


STORY_ORDER = _tasks(
    "story_order",
    "story_logic",
    [
        ("Что звучит логичнее?", ("I got home, ate dinner, and then started homework.", "I started homework, got home, and then ate dinner.", "I ate dinner, got home, and started homework."), 0, "События выстроены в естественном порядке."),
        ("Какой вариант лучше собирает историю?", ("We missed the bus, so we walked to school.", "We walked to school, so we missed the bus.", "We missed the bus, but we stayed home."), 0, "Причина и следствие стоят на своих местах."),
        ("Какой вариант звучит логичнее?", ("She revised for the test, so she felt calmer later.", "She felt calmer later, so she revised for the test.", "She revised for the test, but she never opened her notes."), 0, "Сначала действие, потом результат."),
        ("Какой вариант лучше?", ("I forgot my charger, so my phone died by the evening.", "My phone died by the evening, so I forgot my charger.", "I forgot my charger, but my phone was fully charged forever."), 0, "Первый вариант строит нормальную причинно-следственную связь."),
        ("Что звучит как цельная история?", ("He overslept, rushed out, and got to class late.", "He got to class late, rushed out, and overslept.", "He rushed out and got to class late before he overslept."), 0, "События идут в естественном порядке."),
        ("Какой вариант логичнее?", ("I didn't understand the task at first, but the example helped.", "The example helped, but I didn't understand the task at first after that.", "I understood the task first, but then the example helped me understand it."), 0, "Сначала сложность, потом помощь."),
        ("Что звучит лучше?", ("We planned to meet, but the rain ruined it.", "The rain ruined it, but we planned to meet after that.", "We planned to meet, so the rain started."), 0, "Здесь естественное столкновение плана и реальности."),
        ("Какой вариант точнее?", ("She lost her notes, so she had to borrow mine.", "She borrowed mine, so she lost her notes.", "She lost her notes, and I borrowed hers."), 0, "Нормальная логика: потеряла свои — взяла чужие."),
        ("Что звучит как нормальный мини-рассказ?", ("I came in tired, took a shower, and finally felt human again.", "I felt human again, took a shower, and came in tired.", "I came in tired and felt human again before the shower."), 0, "Порядок действий делает фразу живой и понятной."),
        ("Какой вариант логичнее?", ("He saw the message too late, so he missed the meeting point.", "He missed the meeting point, so he saw the message too late.", "He saw the message too late, but arrived early."), 0, "Сначала причина, потом последствие."),
        ("Что звучит лучше?", ("I finished the first part, then checked my answer, and only then sent it.", "I sent it, checked it, and finished the first part.", "I checked my answer after I sent it before finishing it."), 0, "События выстроены последовательно."),
        ("Какой вариант точнее?", ("She got nervous during the test, but calmed down after the easy question.", "She calmed down after the easy question, but then got nervous before it.", "She got nervous and calm at the same time."), 0, "Есть естественная смена состояния."),
        ("Что звучит как связная история?", ("We started late, lost some time, and had to cut the last part.", "We cut the last part, lost some time, and started late.", "We started late, so we had extra time."), 0, "Первый вариант последовательно показывает развитие ситуации."),
        ("Какой вариант логичнее?", ("I checked the bus app, saw the delay, and took a different route.", "I took a different route, checked the bus app, and saw the delay.", "I saw the delay and waited for hours happily."), 0, "Действия выстроены в нормальной последовательности."),
        ("Что звучит лучше?", ("He promised to help, but then completely forgot about it.", "He forgot about it, but then promised to help before that.", "He promised to help, so he forgot about it."), 0, "Нормальная логика: обещание, потом забывчивость."),
        ("Какой вариант точнее?", ("I reread the sentence, noticed the trap, and changed my answer in time.", "I changed my answer in time, noticed the trap, and reread the sentence.", "I noticed the trap after I finished the test and changed nothing."), 0, "Логика действий важна: сначала перечитал, потом заметил, потом исправил."),
        ("Что звучит связно?", ("She prepared well, but the first question still caught her off guard.", "The first question caught her off guard, but she prepared well after that.", "She prepared well, so nothing surprised her at all."), 0, "Есть контраст между подготовкой и неожиданностью."),
        ("Какой вариант лучше?", ("We reached the station, realized we were early, and grabbed coffee.", "We grabbed coffee, reached the station, and realized we were early.", "We realized we were early before getting there."), 0, "Сначала пришли, потом поняли, потом заполнили паузу."),
        ("Что звучит логичнее?", ("I didn't reply at once because I wanted to think it through.", "I replied at once because I wanted to think it through.", "I didn't reply at once, so I answered immediately."), 0, "Причина хорошо объясняет задержку."),
        ("Какой вариант лучше собирает мысль?", ("He tried to explain it simply, and that finally made it click for me.", "It clicked for me, and then he tried to explain it simply.", "He explained it simply, but nothing changed and it clicked."), 0, "Сначала объяснение, потом результат."),
    ],
)


FUTURE_PLANS = _tasks(
    "future_plans",
    "future_plans",
    [
        ("Выбери правильную фразу:", ("I'm going to revise tonight.", "I going to revise tonight.", "I'm go to revise tonight."), 0, "Конструкция плана: `am/is/are going to`."),
        ("Выбери правильную фразу:", ("She's going to stay home this weekend.", "She's going stay home this weekend.", "She going to stay home this weekend."), 0, "С `she` нужен `is going to`."),
        ("Выбери правильный вопрос:", ("Are you going to join us later?", "Do you going to join us later?", "Are you going join us later?"), 0, "Вопрос строится через `am/is/are`."),
        ("Выбери правильную фразу:", ("We aren't going to leave early.", "We don't going to leave early.", "We aren't going leave early."), 0, "Отрицание строится через `aren't going to`."),
        ("Выбери правильную фразу:", ("He's going to call me after class.", "He is going call me after class.", "He going to calls me after class."), 0, "После `going to` идет базовый глагол `call`."),
        ("Что звучит естественнее?", ("I'm going to take a break first and then study.", "I'm going to taking a break first and then study.", "I going to take a break first and then study."), 0, "После `going to` глагол остается в базовой форме."),
        ("Выбери правильную фразу:", ("They're going to meet near the station.", "They are going meet near the station.", "They're going to met near the station."), 0, "После `going to` — базовый `meet`."),
        ("Выбери правильный вопрос:", ("What are you going to do tomorrow?", "What do you going to do tomorrow?", "What are you going do tomorrow?"), 0, "Вопрос про планы строится через `are ... going to`."),
        ("Выбери правильную фразу:", ("I'm not going to panic this time.", "I don't going to panic this time.", "I'm not going panic this time."), 0, "Правильное отрицание: `am not going to`."),
        ("Выбери правильную фразу:", ("She's going to start earlier next time.", "She's going to starts earlier next time.", "She going to start earlier next time."), 0, "После `going to` — базовый `start`."),
        ("Что звучит лучше?", ("We're going to finish this after dinner.", "We're going finishing this after dinner.", "We going to finish this after dinner."), 0, "План оформляется через `are going to finish`."),
        ("Выбери правильную фразу:", ("He's not going to skip the lesson.", "He isn't going skip the lesson.", "He doesn't going to skip the lesson."), 0, "После `isn't going to` нужен базовый глагол."),
        ("Выбери правильный ответ:", ("Yes, I am.", "Yes, I do.", "Yes, I going."), 0, "На вопрос с `Are you going to ...?` отвечаем через `am`."),
        ("Что звучит естественнее?", ("I'm going to text you when I get home.", "I'm going to texting you when I get home.", "I going to text you when I get home."), 0, "Здесь нужен `going to text`."),
        ("Выбери правильную фразу:", ("They're going to work on it together.", "They going to work on it together.", "They're going to works on it together."), 0, "После `going to` — базовый `work`."),
        ("Выбери правильный вопрос:", ("Is she going to talk to the teacher?", "Does she going to talk to the teacher?", "Is she going talk to the teacher?"), 0, "Вопрос строится через `is she going to`."),
        ("Выбери правильную фразу:", ("We're going to leave as soon as he arrives.", "We're going to left as soon as he arrives.", "We going to leave as soon as he arrives."), 0, "После `going to` нужен базовый `leave`."),
        ("Что звучит лучше?", ("I'm going to try a different way next time.", "I'm going to trying a different way next time.", "I am go to try a different way next time."), 0, "Здесь нужен `going to try`."),
        ("Выбери правильную фразу:", ("She's going to explain it later.", "She's going explain it later.", "She going to explains it later."), 0, "После `going to` — `explain` без `-s`."),
        ("Выбери правильную фразу:", ("They're not going to change the plan now.", "They don't going to change the plan now.", "They're not going change the plan now."), 0, "Правильная форма отрицания — `are not going to`."),
    ],
)


CHOICE_MOVE = _tasks(
    "choice_move",
    "dialogue_choice",
    [
        ("Friend: `Do you want to come with us later?`", ("I'd like to, but I'm going to stay home tonight.", "I'd like, but I going to stay home tonight.", "I go stay home tonight."), 0, "Естественный отказ с вежливым тоном и причиной."),
        ("Classmate: `Can we move it to tomorrow?`", ("Yeah, that's probably better for me.", "Yeah, that probably better for me.", "Tomorrow move better."), 0, "Короткий естественный ответ для переноса плана."),
        ("Friend: `What are you doing this weekend?`", ("I'm going to catch up on homework and rest a bit.", "I'm going catch up on homework and rest a bit.", "Catch up homework and rest."), 0, "Ответ про планы собирается через `going to`."),
        ("Classmate: `Do you mind if I join you?`", ("Not at all. You're welcome to come.", "Not at all. You welcome to come.", "No mind come."), 0, "Хорошая вежливая реакция."),
        ("Friend: `Can you help me after class?`", ("I can, but only for a few minutes.", "I can, but only few minutes.", "Can, few minutes only."), 0, "Такой ответ короткий, живой и естественный."),
        ("Teacher: `Are you going to finish it today?`", ("I think so, if nothing gets in the way.", "I think so, if nothing get in the way.", "I think yes if nothing in way."), 0, "С `nothing` нужен `gets`, и весь ответ звучит уверенно."),
        ("Friend: `Why don't we just start earlier next time?`", ("Yeah, that would probably save us some stress.", "Yeah, that would probably saves us some stress.", "Yes save stress."), 0, "После `would` нужен базовый глагол."),
        ("Classmate: `So what's the plan now?`", ("We're going to split the work and compare answers later.", "We're going split the work and compare answers later.", "We split work later answers."), 0, "План звучит ясно и по-человечески."),
        ("Friend: `Can we skip this part?`", ("I'd rather not. It still looks important.", "I'd rather not. It still look important.", "Rather not, important still."), 0, "С `it` нужен `looks`, и ответ звучит мягко."),
        ("Classmate: `Do you want me to explain it again?`", ("Yeah, but maybe a bit more simply this time.", "Yeah, but maybe a bit more simple this time.", "Yeah explain simple this time."), 0, "Естественная просьба переформулировать объяснение."),
        ("Friend: `Are you free after school?`", ("Not really. I'm going to revise for the test.", "Not really. I going to revise for the test.", "Not really revise test."), 0, "План оформлен через `going to revise`."),
        ("Teacher: `Can you present first?`", ("I'd rather go second, if that's okay.", "I'd rather goes second, if that's okay.", "Rather second okay."), 0, "После `would rather` нужен базовый глагол `go`."),
        ("Friend: `What if the plan doesn't work?`", ("Then we'll figure something else out.", "Then we'll figures something else out.", "Then something else out."), 0, "После `will` нужен базовый глагол `figure`."),
        ("Classmate: `Do you want to work alone or together?`", ("Together is fine, as long as we stay focused.", "Together are fine, as long as we stay focused.", "Together fine stay focused."), 0, "Первый вариант звучит естественно и собранно."),
        ("Friend: `Can you send me your notes later?`", ("Sure, I'm going to do it when I get home.", "Sure, I'm going do it when I get home.", "Sure do when home."), 0, "План в будущем оформлен правильно и звучит живо."),
        ("Teacher: `Are you ready to answer now?`", ("Almost. I just need a few more seconds.", "Almost. I just need few more seconds.", "Almost need seconds."), 0, "Первый вариант естественно тянет паузу."),
        ("Friend: `Do you want to leave now or wait?`", ("Let's wait a bit longer and see.", "Let's waits a bit longer and see.", "Wait bit longer see."), 0, "После `let's` нужен базовый глагол `wait`."),
        ("Classmate: `Why don't you ask the teacher directly?`", ("Yeah, I probably will if I'm still confused.", "Yeah, I probably will if I still confused.", "Probably will if confused."), 0, "Нормальный ответ с условием и живой логикой."),
        ("Friend: `Are you going to join the extra class?`", ("I think I am. It sounds useful.", "I think I am. It sound useful.", "I think am useful."), 0, "С `it` нужен `sounds`, и весь ответ звучит по-человечески."),
        ("Classmate: `Can you explain what happened?`", ("Yeah. The plan changed at the last minute.", "Yeah. The plan change at the last minute.", "Yeah plan changed last minute."), 0, "Past Simple `changed` нужен для завершенного события."),
    ],
)


EVENT_READING = _tasks(
    "event_reading",
    "reading_events",
    [
        ("Текст: `Yesterday I planned to revise after school, but I got home late and felt too tired to focus.` Что помешало плану?", ("The task was too easy.", "The person came home late and was tired.", "The teacher cancelled everything."), 1, "Причина прямо названа: поздно пришел и устал."),
        ("Текст: `We were going to meet at six, but then Kate texted that she was still on the bus.` Что произошло?", ("They started early.", "The meeting was probably delayed.", "Kate forgot her phone."), 1, "Если она еще в автобусе, встречу, скорее всего, пришлось сдвинуть."),
        ("Текст: `I thought the test would be awful, but the first two questions were actually manageable.` Как изменилось отношение автора?", ("It got less stressful after the start.", "It got worse immediately.", "Nothing changed."), 0, "После начала тест уже казался не таким страшным."),
        ("Текст: `Max revised vocabulary on Friday, so by Saturday he felt much calmer about the quiz.` Что помогло Максу?", ("Sleeping longer.", "Revising vocabulary earlier.", "Skipping the quiz."), 1, "Спокойствие стало результатом подготовки."),
        ("Текст: `We missed the first bus, walked to the next stop, and still made it in time.` Какой вывод верный?", ("They gave up and went home.", "They still arrived on time.", "They waited for hours."), 1, "Фраза `still made it in time` говорит о том, что они успели."),
        ("Текст: `I didn't answer right away because I wanted to think through the wording first.` Почему ответ задержался?", ("The person had no idea at all.", "The person wanted a clearer formulation.", "The phone battery died."), 1, "Причина прямо названа: нужно было продумать формулировку."),
        ("Текст: `At first the story looked simple, but the final line changed the whole meaning.` В чем была сложность?", ("Too many unknown words.", "The main idea shifted at the end.", "The text was too short."), 1, "Ключ — в последней строке, а не в лексике."),
        ("Текст: `Lena was going to skip the extra lesson, but then she found out it was about the topic she still didn't get.` Почему она передумала?", ("Her friend forced her.", "The topic was still important for her.", "She had nothing else to do."), 1, "Она осталась, потому что тема была ей нужна."),
        ("Текст: `I wrote the answer fast, reread it, and immediately saw why it sounded off.` Что случилось после перечитывания?", ("The answer seemed perfect.", "The person noticed the problem.", "The person deleted everything."), 1, "После перечитывания ошибка стала заметна."),
        ("Текст: `We were going to leave early, but the teacher kept us for ten extra minutes.` Как это повлияло на план?", ("They probably left later than planned.", "They still left earlier than usual.", "They cancelled the lesson."), 0, "Если их задержали, значит план по раннему уходу сдвинулся."),
        ("Текст: `I knew most of the words, but I still couldn't tell what the writer was really trying to say.` Что было настоящей проблемой?", ("Vocabulary was too advanced.", "The deeper meaning was unclear.", "The text had no structure."), 1, "Слова были понятны, проблема была в общем смысле."),
        ("Текст: `He promised to send the file that night, but I only got it the next afternoon.` Что можно понять?", ("He sent it exactly on time.", "There was a delay.", "The file was lost forever."), 1, "Раз файл пришел только днем позже, обещание не было выполнено вовремя."),
        ("Текст: `I wasn't going to say anything, but the mistake was so obvious that I had to point it out.` Почему человек заговорил?", ("Because the mistake was too clear to ignore.", "Because someone asked directly.", "Because the teacher got angry."), 0, "Причина прямо названа в тексте."),
        ("Текст: `The plan sounded good in theory, but once we started, it became obvious that it was too ambitious.` Какой вывод лучше?", ("The plan was realistic.", "The plan looked better than it worked.", "The plan was too easy."), 1, "Контраст между теорией и практикой здесь ключевой."),
        ("Текст: `I revised less this week, so I already know the final check will feel rougher.` Что ожидает автор?", ("The final check will be easier.", "The final check may feel harder.", "The final check was cancelled."), 1, "Он сам связывает слабую подготовку с более трудным финалом."),
        ("Текст: `We changed the order of tasks, and suddenly the whole thing started making sense.` Что помогло?", ("Doing less work.", "Changing the sequence.", "Taking a long break."), 1, "Изменение порядка задач дало ясность."),
        ("Текст: `I didn't need a new explanation. I just needed a better example.` Что было нужно человеку?", ("More theory.", "A clearer example.", "An easier teacher."), 1, "В тексте это сказано буквально."),
        ("Текст: `She looked confident, but later admitted she had been guessing on half the questions.` Что можно понять?", ("Her confidence was partly fake.", "She knew everything perfectly.", "She didn't do the test."), 0, "Внешняя уверенность не совпала с реальной ситуацией."),
        ("Текст: `I was going to stop after one attempt, but then I saw what exactly went wrong, so I tried again.` Почему человек сделал вторую попытку?", ("Because someone forced him.", "Because the mistake became clear.", "Because the first try was perfect."), 1, "Осознание ошибки дало мотивацию попробовать снова."),
        ("Текст: `The answer was technically okay, but it still didn't sound like something I would naturally say.` Что здесь проверяется?", ("Only grammar.", "Naturalness as well as correctness.", "Only spelling."), 1, "Идея в различии между формальной правильностью и естественностью."),
    ],
)


PRECISE_REPLY = _tasks(
    "precise_reply",
    "precise_reply",
    [
        ("Что звучит точнее?", ("I was tired, so I couldn't focus properly.", "I was tired.", "Tired, no focus."), 0, "Первый вариант точнее связывает причину и эффект."),
        ("Что звучит сильнее?", ("I went there because I thought it would actually help.", "I went there.", "I went because help."), 0, "Первый вариант дает причину и звучит как нормальный ответ."),
        ("Что звучит лучше?", ("I'm going to leave early because I still need time to revise.", "I'm going to leave early.", "Leave early revise."), 0, "План плюс причина дают более сильный ответ."),
        ("Что звучит точнее?", ("It wasn't hard exactly, just more confusing than I expected.", "It was hard.", "Not hard confusing."), 0, "Первый вариант точнее описывает оттенок проблемы."),
        ("Что звучит лучше?", ("The first part was fine, but the last question threw me off.", "The last question was difficult.", "Last question difficult."), 0, "Первый вариант показывает контраст внутри задания."),
        ("Что звучит сильнее?", ("I understood the rule, but I still used the wrong form under pressure.", "I knew the rule but was wrong.", "Rule knew wrong form."), 0, "Ответ становится точнее и ближе к реальной ситуации."),
        ("Что звучит точнее?", ("I'm not going to skip it, but I may do it later than planned.", "I'm not going to skip it.", "Not skip maybe later."), 0, "Появляется точный нюанс, а не только общий факт."),
        ("Что звучит лучше?", ("It sounded natural to me at first, but then I noticed the wording issue.", "It sounded natural at first.", "Natural at first issue later."), 0, "Первый вариант дает развитие мысли."),
        ("Что звучит сильнее?", ("I didn't answer quickly because I wanted the phrasing to be cleaner.", "I didn't answer quickly.", "Didn't answer quickly phrasing."), 0, "Здесь важна объясненная причина задержки."),
        ("Что звучит точнее?", ("The story wasn't difficult to read, but the last line changed everything.", "The last line changed everything.", "Story easy line changed."), 0, "Контраст делает ответ сильнее."),
        ("Что звучит лучше?", ("I'm going to try again because now I can see the mistake more clearly.", "I'm going to try again.", "Try again now mistake."), 0, "Появляется осмысленная мотивация."),
        ("Что звучит сильнее?", ("I don't mind grammar practice, but I need it to feel more connected to real speech.", "I don't mind grammar practice.", "Grammar okay real speech."), 0, "Первый вариант точнее выражает позицию."),
        ("Что звучит точнее?", ("At first I thought it was obvious, but then the logic trap hit me.", "At first it was obvious.", "Obvious then trap."), 0, "Первый вариант передает смену восприятия."),
        ("Что звучит лучше?", ("I was going to relax, but then I remembered I still had one task left.", "I was going to relax.", "Going to relax task left."), 0, "Ответ становится более живым и логичным."),
        ("Что звучит сильнее?", ("The answer looked okay on the surface, but it still felt a bit off.", "The answer looked okay.", "Answer okay but off."), 0, "Появляется важный нюанс про ощущение языка."),
        ("Что звучит точнее?", ("I usually learn faster when I see the same structure in different examples.", "I learn faster with examples.", "Examples faster learn."), 0, "Первый вариант точнее и сильнее."),
        ("Что звучит лучше?", ("I don't just want to pass the check — I want to feel in control.", "I want to pass the check.", "Pass check control."), 0, "Первый вариант звучит взрослее и глубже."),
        ("Что звучит сильнее?", ("The task got easier once I stopped translating every word in my head.", "The task got easier.", "Task easier translation stop."), 0, "Первый вариант показывает, за счет чего стало легче."),
        ("Что звучит точнее?", ("I'm going to fix the weak spots first and then come back to the hard part.", "I'm going to fix it.", "Fix weak spots hard part later."), 0, "План становится ясным и управляемым."),
        ("Что звучит лучше?", ("The real problem wasn't grammar itself — it was choosing under time pressure.", "The problem was grammar.", "Problem time pressure grammar."), 0, "Первый вариант точнее описывает реальную проблему."),
    ],
)


WRITING_PAST_FUTURE = _tasks(
    "writing_past_future",
    "writing_build",
    [
        ("Какое начало лучше для ответа `What did you do last weekend?`", ("Last weekend I mostly stayed home and caught up on sleep.", "Last weekend stayed home and sleep.", "Weekend home sleep."), 0, "Первый вариант звучит как нормальное начало короткого ответа."),
        ("Какой вариант лучше для темы `A day that went wrong`?", ("One day I missed the bus, got stressed, and arrived late.", "One day missed bus stressed arrived late.", "Day wrong bus."), 0, "Первый вариант собран и звучит как мини-история."),
        ("Какой вариант лучше для темы `Plans for tomorrow`?", ("Tomorrow I'm going to finish my homework earlier than usual.", "Tomorrow going to finish homework earlier.", "Tomorrow finish homework earlier."), 0, "План оформлен через `going to` и звучит естественно."),
        ("Какой вариант лучше для темы `What changed recently`?", ("Recently I started checking my answers more carefully before sending them.", "Recently I started check answers before sending.", "Recently answers careful."), 0, "Первый вариант — нормальная письменная фраза."),
        ("Какой вариант лучше для темы `What you learned from a mistake`?", ("That mistake showed me that I rush too much under pressure.", "That mistake showed me I rush too much.", "Mistake showed rush."), 0, "Первый вариант звучит сильнее и яснее."),
        ("Какой вариант лучше для темы `A useful lesson last week`?", ("Last week we had a lesson that finally made the topic click for me.", "Last week had lesson topic click.", "Week lesson click topic."), 0, "Первый вариант — хороший короткий writing-ответ."),
        ("Какой вариант лучше для темы `Your plans for the weekend`?", ("This weekend I'm going to rest, revise, and maybe meet a friend.", "This weekend going to rest revise maybe meet friend.", "Weekend rest revise friend."), 0, "Первый вариант грамотно строит план."),
        ("Какой вариант лучше для темы `Why a task felt hard`?", ("It felt hard because I understood the words but not the logic.", "It felt hard because understood words not logic.", "Hard because words logic."), 0, "Пояснение делает ответ содержательным."),
        ("Какой вариант лучше для темы `What happened after school yesterday`?", ("Yesterday after school I went home, ate, and then revised.", "Yesterday after school went home ate revised.", "After school yesterday home ate."), 0, "Первый вариант связный и естественный."),
        ("Какой вариант лучше для темы `What you are going to improve next`?", ("Next I'm going to work on making my answers sound less stiff.", "Next going to work on answers less stiff.", "Next less stiff answers."), 0, "План звучит естественно и конкретно."),
        ("Какой вариант лучше для темы `A moment you felt better`?", ("I felt better once I saw that the task was actually manageable.", "I felt better once saw task manageable.", "Felt better task manageable."), 0, "Первый вариант звучит как нормальная письменная мысль."),
        ("Какой вариант лучше для темы `A plan that changed`?", ("We were going to meet outside, but then it started raining.", "We were going meet outside but raining.", "Plan changed raining."), 0, "Контраст плана и реальности делает ответ живым."),
        ("Какой вариант лучше для темы `What you want to do differently now`?", ("Now I want to slow down a bit and think through the wording.", "Now I want slow down and think wording.", "Now slow wording."), 0, "Первый вариант звучит естественно и по-взрослому."),
        ("Какой вариант лучше для темы `Why the final check matters`?", ("The final check matters because it shows what I can do without help.", "Final check matters because shows what I can do.", "Final check shows help."), 0, "Первый вариант сильнее и яснее."),
        ("Какой вариант лучше для темы `A useful habit`?", ("One useful habit is rereading my answer before I send it.", "One useful habit rereading answer before send.", "Useful habit rereading."), 0, "Первый вариант — хороший короткий writing-ответ."),
        ("Какой вариант лучше для темы `A past success`?", ("I felt good when I finally noticed the trap before it was too late.", "I felt good when finally noticed trap.", "Felt good trap noticed."), 0, "Первый вариант лучше собирает мысль."),
        ("Какой вариант лучше для темы `Your next step in English`?", ("My next step is to make my speaking feel quicker and more natural.", "My next step make speaking quicker and more natural.", "Next step speaking quicker."), 0, "Первый вариант звучит естественно и содержательно."),
        ("Какой вариант лучше для темы `A difficult moment in class`?", ("I had a difficult moment when I knew the rule but still froze.", "I had difficult moment knew rule froze.", "Difficult class froze."), 0, "Первый вариант сильнее и точнее."),
        ("Какой вариант лучше для темы `A plan you want to keep`?", ("I'm going to keep studying in short daily blocks instead of random long sessions.", "I'm going keep studying in short daily blocks.", "Going keep short blocks."), 0, "После `going to` нужен базовый глагол `keep`."),
        ("Какой вариант лучше как финальная мысль?", ("That's why I want my answers to feel clearer, not just technically correct.", "That's why I want answers feel clearer.", "Answers clearer correct."), 0, "Первый вариант хорошо завершает короткий письменный ответ."),
    ],
)


TENSE_PRESSURE = _tasks(
    "tense_pressure",
    "tense_switch",
    [
        ("Выбери правильную фразу:", ("I usually study in the evening, but yesterday I studied in the morning.", "I usually studied in the evening, but yesterday I study in the morning.", "I usually study in the evening, but yesterday I study in the morning."), 0, "Настоящая привычка и одно событие в прошлом требуют разных времен."),
        ("Выбери правильную фразу:", ("We're going to leave soon because we finished everything already.", "We're going to leave soon because we finish everything already.", "We go to leave soon because we finished everything already."), 0, "План в будущем + завершенное действие в прошлом/уже сейчас."),
        ("Выбери правильную фразу:", ("She missed the bus yesterday, so today she's going to leave earlier.", "She misses the bus yesterday, so today she's going to leave earlier.", "She missed the bus yesterday, so today she going to leave earlier."), 0, "Вчерашнее событие — Past Simple, план на сегодня — `going to`."),
        ("Выбери правильную фразу:", ("I usually don't panic, but that question really threw me off.", "I usually didn't panic, but that question really throw me off.", "I usually don't panic, but that question really throwed me off."), 0, "Привычка — Present Simple, единичный сбой — Past Simple."),
        ("Выбери правильную фразу:", ("They're going to check the answer again because they aren't sure yet.", "They go to check the answer again because they aren't sure yet.", "They're going to checked the answer again because they aren't sure yet."), 0, "План в будущем: `are going to check`."),
        ("Выбери правильную фразу:", ("He usually comes late, but last time he arrived early.", "He usually came late, but last time he arrives early.", "He usually comes late, but last time he arrive early."), 0, "Привычка — `comes`, разовый случай в прошлом — `arrived`."),
        ("Выбери правильную фразу:", ("We talked about the task yesterday, and now we're going to rewrite it.", "We talk about the task yesterday, and now we're going to rewrite it.", "We talked about the task yesterday, and now we going to rewrite it."), 0, "Прошлое действие и текущий план."),
        ("Выбери правильную фразу:", ("I didn't get it at first, but now it makes sense.", "I don't get it at first, but now it made sense.", "I didn't got it at first, but now it makes sense."), 0, "Прошлое затруднение и настоящее понимание."),
        ("Выбери правильную фразу:", ("She usually checks everything twice, so she isn't going to rush this time.", "She usually check everything twice, so she isn't going to rush this time.", "She usually checks everything twice, so she doesn't going to rush this time."), 0, "Привычка в настоящем и план на этот раз."),
        ("Выбери правильную фразу:", ("We were tired yesterday, so today we're going to keep it short.", "We are tired yesterday, so today we're going to keep it short.", "We were tired yesterday, so today we going to keep it short."), 0, "Вчерашнее состояние — Past Simple, план на сегодня — `going to`."),
        ("Выбери правильную фразу:", ("He usually answers fast, but yesterday he needed more time.", "He usually answer fast, but yesterday he needed more time.", "He usually answers fast, but yesterday he need more time."), 0, "Привычка — `answers`, прошлое событие — `needed`."),
        ("Выбери правильную фразу:", ("I'm going to ask again because I still don't fully get the point.", "I'm going to ask again because I still didn't fully get the point.", "I going to ask again because I still don't fully get the point."), 0, "Текущее состояние непонимания — Present Simple, а план — `going to ask`."),
        ("Выбери правильную фразу:", ("Last week I felt lost, but now I'm starting to feel more confident.", "Last week I feel lost, but now I'm starting to felt more confident.", "Last week I felt lost, but now I starting to feel more confident."), 0, "Прошлое — `felt`, текущее развитие — `am starting to feel`."),
        ("Выбери правильную фразу:", ("We usually finish on time, but today we're going to stay longer.", "We usually finished on time, but today we're going to stay longer.", "We usually finish on time, but today we going to stay longer."), 0, "Привычка и план на сегодня."),
        ("Выбери правильную фразу:", ("She didn't answer right away because she wanted to think first.", "She doesn't answer right away because she wanted to think first.", "She didn't answered right away because she wanted to think first."), 0, "Прошедшее действие требует `didn't answer`."),
        ("Выбери правильную фразу:", ("I usually reread my answers, and tomorrow I'm going to do the same.", "I usually reread my answers, and tomorrow I do the same.", "I usually reread my answers, and tomorrow I'm going to did the same."), 0, "Привычка в настоящем и план на завтра."),
        ("Выбери правильную фразу:", ("They planned everything yesterday, so today they're going to move faster.", "They plan everything yesterday, so today they're going to move faster.", "They planned everything yesterday, so today they going to move faster."), 0, "Прошлое планирование и текущий план действий."),
        ("Выбери правильную фразу:", ("He didn't notice the trap before, but now he usually spots it quickly.", "He didn't noticed the trap before, but now he usually spots it quickly.", "He didn't notice the trap before, but now he usually spot it quickly."), 0, "После `didn't` — базовый `notice`, а привычка сейчас — `spots`."),
        ("Выбери правильную фразу:", ("I was nervous at first, but now I'm going to trust my first clear answer.", "I am nervous at first, but now I'm going to trust my first clear answer.", "I was nervous at first, but now I going to trust my first clear answer."), 0, "Прошлое состояние и текущий план."),
        ("Выбери правильную фразу:", ("We usually start earlier, but this time we're going to wait for everyone.", "We usually started earlier, but this time we're going to wait for everyone.", "We usually start earlier, but this time we going to wait for everyone."), 0, "Привычка в настоящем и особый план на этот раз."),
    ],
)


CHECK2_A2 = _tasks(
    "check2_a2",
    "checkpoint",
    [
        ("Выбери правильную фразу:", ("I missed the bus yesterday, so today I'm going to leave earlier.", "I miss the bus yesterday, so today I'm going to leave earlier.", "I missed the bus yesterday, so today I going to leave earlier."), 0, "Прошлое событие и план на сегодня требуют разных форм."),
        ("Что ближе по смыслу к `The wording threw me off`?", ("Формулировка сбила меня.", "Формулировка меня вдохновила.", "Формулировка была слишком короткой."), 0, "Здесь речь о том, что подача ответа запутала."),
        ("Выбери лучший вопрос:", ("Why did the answer sound okay but still feel unnatural?", "Why did the answer sounded okay but still feel unnatural?", "Why does the answer sound okay but still felt unnatural?"), 0, "После `did` — базовый `sound`."),
        ("Что звучит естественнее?", ("I was going to relax, but then I remembered the unfinished task.", "I was going to relax, but then I remember the unfinished task.", "I was going to relaxing, but then I remembered the unfinished task."), 0, "План в прошлом + воспоминание о задаче."),
        ("Текст: `We were going to start at six, but one person arrived twenty minutes late.` Что произошло?", ("They probably started later than planned.", "They started early.", "Nobody arrived."), 0, "Опоздание явно сдвинуло план."),
        ("Что звучит точнее?", ("I didn't fail because I didn't know the rule — I failed because I rushed.", "I failed because I didn't know the rule.", "I failed because rush."), 0, "Первый вариант точнее объясняет реальную причину ошибки."),
        ("Выбери правильную фразу:", ("She usually checks the logic, but this time she trusted the first option.", "She usually check the logic, but this time she trusted the first option.", "She usually checks the logic, but this time she trust the first option."), 0, "Привычка — Present Simple, разовый выбор — Past Simple."),
        ("Что лучше передает смысл `I need a clearer structure, not easier prompts`?", ("Мне нужна более понятная структура, а не более лёгкие задания.", "Мне нужны только простые задания.", "Мне не нужна никакая структура."), 0, "Ключ — в ясности структуры, а не в снижении сложности."),
        ("Выбери правильную фразу:", ("They're going to compare answers after they finish the first part.", "They going to compare answers after they finish the first part.", "They're going to compared answers after they finish the first part."), 0, "После `going to` нужен базовый глагол."),
        ("Текст: `I knew the words, but I still couldn't tell what the writer was really getting at.` В чем была проблема?", ("Смысл текста оставался неясным.", "Слова были слишком сложными.", "Текст был слишком длинным."), 0, "Слова понятны, а вот реальный смысл — нет."),
        ("Что звучит сильнее?", ("The answer wasn't wrong exactly, just too stiff for the situation.", "The answer was wrong.", "Answer stiff wrong."), 0, "Первый вариант различает ошибку и неестественность."),
        ("Выбери правильный вопрос:", ("Are you going to rewrite it or leave it like this?", "Do you going to rewrite it or leave it like this?", "Are you going rewrite it or leave it like this?"), 0, "Вопрос про планы — через `are ... going to`."),
        ("Что звучит лучше?", ("Last week I froze in speaking tasks, but now I recover faster.", "Last week I freeze in speaking tasks, but now I recover faster.", "Last week I froze in speaking tasks, but now I recovered faster."), 0, "Прошлое сравнивается с текущим состоянием."),
        ("Что лучше как мини-вывод?", ("The shorter version works because the logic is cleaner.", "The shorter version work because the logic is cleaner.", "Shorter version cleaner logic."), 0, "С `version` нужен `works`, и ответ звучит цельно."),
        ("Текст: `I wasn't going to ask for help, but the example made the whole thing click.` Почему человек всё-таки сдвинулся вперед?", ("Потому что хороший пример прояснил идею.", "Потому что задание стало легче само по себе.", "Потому что он решил всё пропустить."), 0, "Именно пример дал понимание."),
        ("Выбери правильную фразу:", ("He didn't notice the trap at first, but later he saw exactly what was off.", "He didn't noticed the trap at first, but later he saw exactly what was off.", "He doesn't notice the trap at first, but later he saw exactly what was off."), 0, "После `didn't` нужен базовый `notice`."),
        ("Что звучит естественнее?", ("I'm going to keep my answer simple, but I want it to sound real.", "I'm going to keep my answer simple, but I want it sound real.", "I going to keep answer simple but real."), 0, "После `want` нужен инфинитив `to sound`."),
        ("Что точнее описывает `The task looked easy, but the trap was in the logic`?", ("Подвох был не в словах, а в самой логике.", "Задача была лёгкой во всём.", "Проблема была только в грамматике."), 0, "Суть именно в логической ловушке."),
        ("Выбери лучший ответ учителю:", ("I think the idea is clear, but the phrasing still needs work.", "I think the idea are clear, but the phrasing still needs work.", "Idea clear phrasing work."), 0, "С `idea` нужен `is`, и первый вариант звучит зрелее."),
        ("Что лучше как финальная мысль?", ("I'm not aiming for perfect wording every time — I want clear, usable English.", "I'm not aiming for perfect wording every time — I wants clear, usable English.", "Not aiming perfect wording usable English."), 0, "С `I` нужен `want`, и весь ответ звучит как сильный вывод."),
    ],
)


CHECK2_PLUS = _tasks(
    "check2_plus",
    "checkpoint",
    [
        ("Выбери лучший вариант:", ("I wasn't going to say anything, but the phrasing was so off that I had to point it out.", "I wasn't going to say anything, but the phrasing was so off that I had point it out.", "I wasn't going to say anything, but the phrasing were so off that I had to point it out."), 0, "После `had to` нужен базовый глагол `point`, а `phrasing` требует `was`."),
        ("Что ближе по смыслу к `I second-guessed myself and changed the better answer`?", ("Я пересомневался и заменил более сильный ответ.", "Я стал увереннее и улучшил ответ.", "Я оставил всё как было."), 0, "Здесь смысл в том, что сомнение только ухудшило выбор."),
        ("Выбери правильный вопрос:", ("Why did the safer answer still sound less convincing?", "Why did the safer answer still sounded less convincing?", "Why does the safer answer still sound less convincing yesterday?"), 0, "После `did` нужен базовый `sound`."),
        ("Что звучит естественнее?", ("I knew the rule in theory, but in the moment I still froze.", "I know the rule in theory, but in the moment I still froze.", "I knew the rule in theory, but in the moment I still freeze."), 0, "Прошлое событие требует Past Simple и для знания, и для сбоя."),
        ("Текст: `The answer looked polished, but it didn't really match the tone of the situation.` Что было слабым местом?", ("The tone fit perfectly.", "The phrasing didn't fit the context.", "The answer was too short."), 1, "Проблема в несоответствии тону ситуации."),
        ("Что звучит сильнее?", ("I don't need easier tasks — I need sharper feedback on why my answer feels off.", "I don't need easier tasks.", "Need sharper feedback."), 0, "Первый вариант формулирует реальную потребность точнее."),
        ("Выбери правильную фразу:", ("She usually spots the grammar trap, but this time the logic trap got her.", "She usually spot the grammar trap, but this time the logic trap got her.", "She usually spots the grammar trap, but this time the logic trap get her."), 0, "Привычка — `spots`, разовый удар ловушки — `got`."),
        ("Что лучше передает смысл `The shorter answer won because it stayed cleaner under pressure`?", ("Победил более короткий ответ, потому что под давлением он остался чище.", "Победил более длинный ответ, потому что он был сложнее.", "Под давлением победило всё сразу."), 0, "Ключ — в ясности под давлением, а не в длине ради длины."),
        ("Выбери правильную фразу:", ("They're going to compare the two versions and keep the clearer one.", "They're going to compared the two versions and keep the clearer one.", "They going to compare the two versions and keep the clearer one."), 0, "После `going to` нужны базовые `compare` и `keep`."),
        ("Текст: `I understood every sentence separately, but I still missed what the whole paragraph was doing.` В чем была проблема?", ("В отдельных словах.", "В общей функции абзаца и его идее.", "В орфографии."), 1, "Проблема уже не в словах, а в роли абзаца целиком."),
        ("Что звучит точнее?", ("The answer wasn't weak because it was short — it was weak because it was vague.", "The answer was weak because it was short.", "Answer weak because short."), 0, "Первый вариант точнее объясняет причину слабости."),
        ("Выбери правильный вопрос:", ("Are you going to keep this version or rewrite it from scratch?", "Do you going to keep this version or rewrite it from scratch?", "Are you going keep this version or rewrite it from scratch?"), 0, "Вопрос про план — через `are ... going to`."),
        ("Что звучит лучше?", ("Last month I would've picked the safer option, but now I trust the cleaner one more.", "Last month I would've pick the safer option, but now I trust the cleaner one more.", "Last month I would picked the safer option, but now I trust the cleaner one more."), 0, "После `would've` нужен базовый `pick`."),
        ("Что лучше как мини-вывод?", ("A strong answer doesn't just survive grammar — it survives context too.", "A strong answer don't just survive grammar — it survives context too.", "Strong answer survive grammar context."), 0, "С `answer` нужен `doesn't`, и мысль звучит сильнее."),
        ("Текст: `I wasn't lost because the English was too hard. I was lost because I couldn't see what mattered most.` Что это показывает?", ("Проблема была в приоритете смысла, а не в сложности языка.", "Проблема была только в словаре.", "Проблемы вообще не было."), 0, "Главная мысль — не всё трудное из-за языка, иногда из-за фокуса."),
        ("Выбери правильную фразу:", ("He didn't change the wording much, but the one change he made fixed the whole tone.", "He didn't changed the wording much, but the one change he made fixed the whole tone.", "He doesn't change the wording much, but the one change he made fixed the whole tone."), 0, "После `didn't` — базовый `change`, а дальше Past Simple `fixed`."),
        ("Что звучит естественнее?", ("I'm going to keep the answer simple, but I want it to land more clearly.", "I'm going to keep the answer simple, but I want it land more clearly.", "I going to keep answer simple but clear."), 0, "После `want` нужен инфинитив `to land`, даже в разговорном оттенке."),
        ("Что точнее описывает `The task wasn't hard, but the framing pushed me in the wrong direction`?", ("Сложность была в подаче, которая вела к неверному выбору.", "Задача была легкой и прямой.", "Проблема была только во времени."), 0, "Здесь важна именно опасная формулировка."),
        ("Выбери лучший ответ учителю:", ("I think the content works, but the delivery still feels slightly off.", "I think the content work, but the delivery still feels slightly off.", "Content works delivery off."), 0, "С `content` здесь нужен `works`, и первый вариант звучит точнее."),
        ("Что лучше как финальная мысль?", ("At this point I care less about sounding impressive and more about sounding precise.", "At this point I cares less about sounding impressive and more about sounding precise.", "At this point sounding precise more."), 0, "С `I` нужен `care`, и весь ответ звучит как уверенный вывод."),
    ],
)


MISSION_LEVEL_TASKS: dict[str, dict[str, tuple[Task, ...]]] = {
    "routine_words": {"default": ROUTINE_A2, "plus": ROUTINE_PLUS},
    "present_simple": {"default": GRAMMAR_A2, "plus": GRAMMAR_PLUS},
    "school_dialogue": {"default": DIALOGUE_A2, "plus": DIALOGUE_PLUS},
    "mistake_hunt": {"default": MISTAKE_HUNT_A2, "plus": MISTAKE_HUNT_PLUS},
    "fast_dialogue": {"default": FAST_DIALOGUE_A2, "plus": FAST_DIALOGUE_PLUS},
    "reading_meaning": {"default": READING_A2, "plus": READING_PLUS},
    "natural_reply": {"default": NATURAL_A2, "plus": NATURAL_PLUS},
    "writing_build": {"default": WRITING_A2, "plus": WRITING_PLUS},
    "past_events": {"default": PAST_EVENTS, "plus": PAST_EVENTS},
    "story_order": {"default": STORY_ORDER, "plus": STORY_ORDER},
    "future_plans": {"default": FUTURE_PLANS, "plus": FUTURE_PLANS},
    "choice_move": {"default": CHOICE_MOVE, "plus": CHOICE_MOVE},
    "event_reading": {"default": EVENT_READING, "plus": EVENT_READING},
    "precise_reply": {"default": PRECISE_REPLY, "plus": PRECISE_REPLY},
    "writing_past_future": {"default": WRITING_PAST_FUTURE, "plus": WRITING_PAST_FUTURE},
    "tense_pressure": {"default": TENSE_PRESSURE, "plus": TENSE_PRESSURE},
}

CHECKPOINT_LEVEL_TASKS: dict[str, dict[str, tuple[Task, ...]]] = {
    "daily_routine": {"default": CHECK_A2, "plus": CHECK_PLUS},
    "movement_control": {"default": CHECK2_A2, "plus": CHECK2_PLUS},
}


DAILY_ROUTINE_CHAPTER = Chapter(
    id="daily_routine",
    title="Глава 1. База без паники",
    description="Здесь уже не просто разогрев. Глава собирает словарь, грамматику, живые ответы, чтение по смыслу и короткий письменный строй перед финальным чеком.",
    missions=(
        Mission("routine_words", "Миссия 1. Ритм и словарь", "Здесь не разминаемся по-детски, а собираем нужную лексику для обычного дня и школьного ритма.", 45, ROUTINE_A2),
        Mission("present_simple", "Миссия 2. Грамматика без развала", "Подтягиваем Present Simple так, чтобы фразы держались ровно и не рассыпались на вопросах и отрицаниях.", 55, GRAMMAR_A2),
        Mission("school_dialogue", "Миссия 3. Живые ответы", "Здесь уже важна не только грамматика, но и ощущение нормальной речи: короткие ответы, реакция, контекст.", 60, DIALOGUE_A2),
        Mission("mistake_hunt", "Миссия 4. Ошибки под прицелом", "Ловим типовые сбои, правим кривые фразы и добиваем грамматическую внимательность перед более плотными заданиями.", 65, MISTAKE_HUNT_A2),
        Mission("fast_dialogue", "Миссия 5. Быстрый диалог", "Короткие реплики, реакция на лету и нормальный ритм речи без деревянных ответов.", 70, FAST_DIALOGUE_A2),
        Mission("reading_meaning", "Миссия 6. Смысл без перевода", "Короткие тексты и вопросы по сути: здесь важно не переводить по словам, а реально понимать, что сказал текст.", 75, READING_A2),
        Mission("natural_reply", "Миссия 7. Скажи по-человечески", "Берем школьные ответы и превращаем их в живые, естественные и более сильные формулировки.", 75, NATURAL_A2),
        Mission("writing_build", "Миссия 8. Мини-письмо без развала", "Собираем короткие письменные ответы так, чтобы они звучали как цельная мысль, а не как набор обрывков.", 80, WRITING_A2),
    ),
    boss=Boss(
        id="daily_routine_checkpoint",
        title="Финальный чек главы",
        description="Это уже контрольный заход по главе: меньше шума, больше ощущения реального уровня.",
        xp_reward=90,
        tasks=CHECK_A2,
    ),
)

MOVEMENT_CONTROL_CHAPTER = Chapter(
    id="movement_control",
    title="Глава 2. Движение и контроль",
    description="Здесь уже идем дальше базы: прошлое, планы, выбор хода, смысл текста и более собранные ответы под давлением.",
    missions=(
        Mission("past_events", "Миссия 1. Что было вчера", "Собираем Past Simple так, чтобы прошлые события звучали ровно, без каши и кривых форм.", 65, PAST_EVENTS),
        Mission("story_order", "Миссия 2. История без каши", "Учимся держать порядок событий и выстраивать короткие истории так, чтобы они были понятны сразу.", 70, STORY_ORDER),
        Mission("future_plans", "Миссия 3. Планы без тумана", "Прокачиваем `going to` и говорим о планах так, чтобы это звучало спокойно и уверенно.", 70, FUTURE_PLANS),
        Mission("choice_move", "Миссия 4. Выбери ход", "Живые диалоги про предложения, переносы, выбор и короткие решения без деревянных ответов.", 75, CHOICE_MOVE),
        Mission("event_reading", "Миссия 5. Поймай смысл", "Короткие истории и выводы по событиям: важно не просто читать, а понимать, что произошло и почему.", 80, EVENT_READING),
        Mission("precise_reply", "Миссия 6. Скажи точнее", "Делаем ответы сильнее: меньше обрубков, больше точности, причин и нормальной логики.", 80, PRECISE_REPLY),
        Mission("writing_past_future", "Миссия 7. Мини-письмо: вчера и завтра", "Собираем короткие письменные ответы про прошлые события и будущие планы без развала по дороге.", 85, WRITING_PAST_FUTURE),
        Mission("tense_pressure", "Миссия 8. Времена под давлением", "Переключаемся между привычками, прошлым и планами так, чтобы не путаться под нагрузкой.", 85, TENSE_PRESSURE),
    ),
    boss=Boss(
        id="movement_control_checkpoint",
        title="Финальный чек главы",
        description="Финальный заход по второй главе: тут уже важны не только формы, но и уверенность в выборе, смысл и контроль под давлением.",
        xp_reward=110,
        tasks=CHECK2_A2,
    ),
)


CHAPTERS: tuple[Chapter, ...] = (DAILY_ROUTINE_CHAPTER, MOVEMENT_CONTROL_CHAPTER)


def get_level_bucket(level: str | None) -> str:
    if level in {"A2+", "A2-B1"}:
        return "plus"
    return "default"


def get_chapter(chapter_id: str) -> Chapter:
    for chapter in CHAPTERS:
        if chapter.id == chapter_id:
            return chapter
    raise KeyError(f"Unknown chapter id: {chapter_id}")


def get_next_chapter_after(chapter_id: str) -> Chapter | None:
    for index, chapter in enumerate(CHAPTERS):
        if chapter.id == chapter_id:
            if index + 1 < len(CHAPTERS):
                return CHAPTERS[index + 1]
            return None
    raise KeyError(f"Unknown chapter id: {chapter_id}")


def get_mission(chapter_id: str, mission_id: str) -> Mission:
    chapter = get_chapter(chapter_id)
    for mission in chapter.missions:
        if mission.id == mission_id:
            return mission
    raise KeyError(f"Unknown mission id: {mission_id}")


def get_mission_tasks(chapter_id: str, mission_id: str, level: str | None) -> tuple[Task, ...]:
    get_chapter(chapter_id)
    bucket = get_level_bucket(level)
    return MISSION_LEVEL_TASKS[mission_id][bucket]


def get_boss(chapter_id: str) -> Boss:
    return get_chapter(chapter_id).boss


def get_boss_tasks(chapter_id: str, level: str | None) -> tuple[Task, ...]:
    bucket = get_level_bucket(level)
    return CHECKPOINT_LEVEL_TASKS[chapter_id][bucket]


def get_placement_tasks() -> tuple[Task, ...]:
    return PLACEMENT_TASKS


def iter_all_tasks() -> tuple[Task, ...]:
    all_tasks: list[Task] = list(PLACEMENT_TASKS)
    for variants in MISSION_LEVEL_TASKS.values():
        for tasks in variants.values():
            all_tasks.extend(tasks)
    for variants in CHECKPOINT_LEVEL_TASKS.values():
        for tasks in variants.values():
            all_tasks.extend(tasks)
    return tuple(all_tasks)
