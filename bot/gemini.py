from __future__ import annotations

import json
from urllib import error, request


class GeminiClient:
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def generate_text(self, prompt: str) -> str | None:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        data = json.dumps(payload).encode("utf-8")
        opener = request.build_opener(request.ProxyHandler({}))

        for _ in range(2):
            req = request.Request(
                url,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": self.api_key,
                },
                method="POST",
            )

            try:
                with opener.open(req, timeout=20) as response:
                    body = json.loads(response.read().decode("utf-8"))
            except error.HTTPError as exc:
                if exc.code in {429, 500, 503}:
                    continue
                return None
            except (error.URLError, TimeoutError, json.JSONDecodeError):
                continue

            candidates = body.get("candidates") or []
            if not candidates:
                continue

            parts = candidates[0].get("content", {}).get("parts", [])
            text_chunks = [part.get("text", "").strip() for part in parts if part.get("text")]
            text = "\n".join(chunk for chunk in text_chunks if chunk).strip()
            if text:
                return text

        return None


def build_summary_prompt(kind: str, score_text: str, title: str) -> str:
    return "\n".join(
        [
            "Ты — AI-наставник по английскому для подростка, который идет к уровню B2+.",
            "Пиши по-русски.",
            "Стиль: живой, уверенный, современный, без канцелярщины и без клоунады.",
            "Нужен очень короткий комментарий после прохождения этапа.",
            "Формат: ровно 2 коротких абзаца.",
            "Первый абзац: реакция на результат.",
            "Второй абзац: на чем сфокусироваться дальше.",
            "Не используй списки.",
            f"Тип этапа: {kind}",
            f"Название: {title}",
            f"Результат: {score_text}",
        ]
    )


def build_tutor_prompt(user_text: str) -> str:
    return "\n".join(
        [
            "Ты — сильный AI-наставник по английскому для подростка, который идет к уровню B2 и выше.",
            "Пиши по-русски, но примеры и конструкции всегда показывай на английском.",
            "Объясняй по методике: суть -> короткое правило -> 2-3 живых примера -> мини-закрепление.",
            "Стиль: понятно, по-человечески, современно, без душноты.",
            "Если тема грамматическая, сравни похожие конструкции.",
            "Если тема про слово или фразу, дай смысл, оттенок и пример в контексте.",
            "Не используй длинные списки и тяжелые вступления.",
            "Если можно, закончи ответ одним коротким вопросом или мини-упражнением на закрепление.",
            "",
            f"Вопрос пользователя: {user_text}",
        ]
    )


def build_error_coach_prompt(
    *,
    stage: str,
    prompt: str,
    chosen_answer: str,
    correct_answer: str,
    explanation: str,
) -> str:
    return "\n".join(
        [
            "Ты — AI-наставник по английскому для подростка, который идет к уровню B2+.",
            "Нужен короткий разбор ошибки после задания в Telegram-боте.",
            "Пиши по-русски.",
            "Стиль: спокойно, понятно, без канцелярщины.",
            "Формат: ровно 2 коротких абзаца.",
            "Первый абзац: где именно логика ответа сломалась.",
            "Второй абзац: как быстро не ошибаться в похожем месте в следующий раз.",
            "Не используй списки.",
            "Не пересказывай задание слишком длинно.",
            f"Этап: {stage}",
            f"Задание: {prompt}",
            f"Выбранный ответ: {chosen_answer}",
            f"Правильный ответ: {correct_answer}",
            f"Базовое объяснение: {explanation}",
        ]
    )
