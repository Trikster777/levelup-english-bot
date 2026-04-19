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


CHECK_A2 = _tasks(
    "check_a2",
    "checkpoint",
    [
        ("Выбери правильный вариант:", ("She usually gets home at five.", "She usually get home at five.", "She usually getting home at five."), 0, "С `she` нужен `gets`."),
        ("Что значит `free time`?", ("свободное время", "время урока", "список дел"), 0, "`free time` — это `свободное время`."),
        ("Что звучит правильно?", ("Do you usually study in the evening?", "Does you usually study in the evening?", "Do you usually studies in the evening?"), 0, "С `you` используем `Do`."),
        ("Friend: `What do you do after school?`", ("I usually chill for a bit and then do homework.", "I usually chill for a bit and then does homework.", "I usually am chill for a bit."), 0, "Первый вариант естественный и грамотно собран."),
        ("Что значит `rarely`?", ("редко", "быстро", "поздно"), 0, "`rarely` — это `редко`."),
        ("Выбери правильное отрицание:", ("He doesn't play basketball.", "He don't play basketball.", "He doesn't plays basketball."), 0, "После `doesn't` идет базовый глагол."),
        ("Что звучит естественно?", ("I get home at four and have dinner later.", "I home get at four and have dinner later.", "I am get home at four."), 0, "Первый вариант звучит нормально."),
        ("Friend: `Are you free tonight?`", ("Maybe later.", "Maybe I am later.", "Later maybe I am."), 0, "Короткий живой ответ: `Maybe later.`"),
        ("Что звучит правильно?", ("My friends usually go out on weekends.", "My friends usually goes out on weekends.", "My friends usually going out on weekends."), 0, "С `friends` — базовый глагол `go`."),
        ("Teacher: `Do you understand the rule?`", ("Mostly, yeah.", "Mostly, I do understand am.", "Yeah mostly understand."), 0, "Коротко и естественно: `Mostly, yeah.`"),
        ("Что значит `hang out`?", ("тусоваться", "опаздывать", "сдаваться"), 0, "`hang out` — это `тусоваться`."),
        ("Выбери правильный вопрос:", ("What time does he get up?", "What time do he get up?", "What time does he gets up?"), 0, "С `he` нужен `does`, а глагол остается базовым."),
    ],
)


CHECK_PLUS = _tasks(
    "check_plus",
    "checkpoint",
    [
        ("Выбери лучший вариант:", ("She usually ends up doing homework late because she puts it off.", "She usually end up doing homework late because she puts it off.", "She usually ends up does homework late because she puts it off."), 0, "С `she` нужен `ends up`."),
        ("Что ближе по смыслу к `I run on very little sleep`?", ("Я держусь почти без сна", "Я люблю мало спать", "Я быстро бегаю"), 0, "`run on very little sleep` — это `функционировать почти без сна`."),
        ("Что звучит правильнее?", ("Do you ever feel like you're learning rules but not using them?", "Does you ever feel like you're learning rules but not using them?", "Do you ever feels like you're learning rules but not using them?"), 0, "С `you` нужен `do`, а дальше базовая форма `feel`."),
        ("Teacher: `Why is this answer stronger?`", ("Because it sounds more natural and actually fits the context.", "Because it sound more natural and actually fits the context.", "Because more natural and fits context."), 0, "С `it` нужен `sounds`."),
        ("Что лучше переводит `My schedule is packed`?", ("Мой график забит под завязку", "Мой график спокойный", "Мой график запутанный"), 0, "`packed` — это `забитый, плотный`."),
        ("Выбери грамотно собранный вариант:", ("He doesn't always realize how much time he wastes online.", "He doesn't always realizes how much time he wastes online.", "He don't always realize how much time he wastes online."), 0, "После `doesn't` — `realize`, без `-s`."),
        ("Friend: `What still messes with your head in English?`", ("Probably prepositions. They still feel random sometimes.", "Probably prepositions. They still feels random sometimes.", "Probably prepositions still random sometimes."), 0, "С `they` нужен базовый глагол `feel`."),
        ("Что звучит лучше?", ("I remember words better when I see them in context.", "I remembers words better when I see them in context.", "I remember better words when see them in context."), 0, "С `I` — `remember`, без `-s`."),
        ("Teacher: `Can you make that more precise?`", ("Sure. It's not about the action, it's about the time frame.", "Sure. It's not about the action, it's about the time frames.", "Sure it about time frame."), 0, "Первый вариант звучит точнее и чище."),
        ("Что ближе к `I squeeze in homework before dinner`?", ("Я успеваю втиснуть домашку до ужина", "Я откладываю домашку до ужина", "Я полностью игнорирую домашку"), 0, "`squeeze in` — это `с трудом втиснуть в расписание`."),
        ("Выбери лучший вопрос:", ("How often do you actually revise vocabulary?", "How often are you actually revise vocabulary?", "How often does you actually revise vocabulary?"), 0, "С `you` нужен `do`, а дальше базовый глагол."),
        ("Classmate: `So what's the real difference here?`", ("One is about routine, the other is about something more temporary.", "One is about routine, the other are about something more temporary.", "One routine other temporary."), 0, "Первый вариант точно и естественно объясняет разницу."),
    ],
)


MISSION_LEVEL_TASKS: dict[str, dict[str, tuple[Task, ...]]] = {
    "routine_words": {"default": ROUTINE_A2, "plus": ROUTINE_PLUS},
    "present_simple": {"default": GRAMMAR_A2, "plus": GRAMMAR_PLUS},
    "school_dialogue": {"default": DIALOGUE_A2, "plus": DIALOGUE_PLUS},
}

CHECKPOINT_LEVEL_TASKS: dict[str, dict[str, tuple[Task, ...]]] = {
    "daily_routine": {"default": CHECK_A2, "plus": CHECK_PLUS},
}


DAILY_ROUTINE_CHAPTER = Chapter(
    id="daily_routine",
    title="Глава 1. База без паники",
    description="Это уже больше похоже на нормальный срез уровня: словарь, грамматика, живые ответы и финальный контрольный заход по главе.",
    missions=(
        Mission("routine_words", "Миссия 1. Ритм и словарь", "Здесь не разминаемся по-детски, а собираем нужную лексику для обычного дня и школьного ритма.", 45, ROUTINE_A2),
        Mission("present_simple", "Миссия 2. Грамматика без развала", "Подтягиваем Present Simple так, чтобы фразы держались ровно и не рассыпались на вопросах и отрицаниях.", 55, GRAMMAR_A2),
        Mission("school_dialogue", "Миссия 3. Живые ответы", "Здесь уже важна не только грамматика, но и ощущение нормальной речи: короткие ответы, реакция, контекст.", 60, DIALOGUE_A2),
    ),
    boss=Boss(
        id="daily_routine_checkpoint",
        title="Финальный чек главы",
        description="Это не босс для красоты. Это контрольный заход по главе: меньше шума, больше ощущения реального уровня.",
        xp_reward=90,
        tasks=CHECK_A2,
    ),
)


CHAPTERS: tuple[Chapter, ...] = (DAILY_ROUTINE_CHAPTER,)


def get_level_bucket(level: str | None) -> str:
    if level in {"A2+", "A2-B1"}:
        return "plus"
    return "default"


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
