import difflib
import json
import re
from pathlib import Path

from models import MenuItem

MENU_PATH = Path(__file__).resolve().parent.parent / "data" / "menu.json"


def load_menu(path: Path = MENU_PATH) -> list[MenuItem]:
    with open(path, encoding="utf-8") as f:
        raw_items = json.load(f)
    return [MenuItem(**raw) for raw in raw_items]


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text.strip()


def retrieve_item(query: str, menu: list[MenuItem] | None = None) -> MenuItem | None:
    """Match a free-text question to a single menu item by name.

    The catalog is a small, structured, hand-curated JSON file (not free
    text), so exact/substring matching on item names does the job here -
    no embeddings or vector index needed for ~30 dishes.
    """
    if menu is None:
        menu = load_menu()

    normalized_query = _normalize(query)

    for candidate in menu:
        if _normalize(candidate.item) in normalized_query:
            return candidate

    item_names = [candidate.item for candidate in menu]
    normalized_names = {_normalize(name): name for name in item_names}
    close = difflib.get_close_matches(normalized_query, normalized_names.keys(), n=1, cutoff=0.4)
    if close:
        matched_name = normalized_names[close[0]]
        return next(c for c in menu if c.item == matched_name)

    return None
