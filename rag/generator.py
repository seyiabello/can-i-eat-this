import json
import os

from openai import OpenAI

from models import MenuItem

_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client


SYSTEM_PROMPT = """You are an allergen-safety assistant for a dining hall counter.
You are given ONE menu item's structured allergen data and a customer's question about it.
Answer using ONLY the data provided - never guess or infer an allergen that isn't listed.

Respond with strict JSON:
{"status": "safe" | "unsafe" | "unverified", "explanation": "<one short sentence>", "matched_allergens": [<allergens from confirmed_allergens relevant to the question>]}

Rules:
- "unsafe": the allergen asked about appears in confirmed_allergens.
- "safe": the allergen asked about does NOT appear in confirmed_allergens AND ambiguous_flag is false.
- "unverified": ambiguous_flag is true, OR the data doesn't clearly cover the allergen asked about, OR you are not confident.
- When in doubt, choose "unverified". Never guess "safe" to be helpful.
"""


def build_user_prompt(question: str, item: MenuItem) -> str:
    return (
        f"Customer question: {question}\n\n"
        f"Menu item data:\n"
        f"- item: {item.item}\n"
        f"- allergen_notes_raw: {item.allergen_notes_raw!r}\n"
        f"- confirmed_allergens: {item.confirmed_allergens}\n"
        f"- ambiguous_flag: {item.ambiguous_flag}\n"
        f"- ambiguous_reason: {item.ambiguous_reason}\n"
    )


def generate(question: str, item: MenuItem) -> dict:
    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(question, item)},
        ],
    )
    content = response.choices[0].message.content

    try:
        parsed = json.loads(content)
        return {
            "status": str(parsed.get("status", "")),
            "explanation": str(parsed.get("explanation", "")),
            "matched_allergens": list(parsed.get("matched_allergens", [])),
        }
    except (json.JSONDecodeError, AttributeError):
        return {
            "status": "unverified",
            "explanation": "Model returned a response that could not be parsed.",
            "matched_allergens": [],
        }
