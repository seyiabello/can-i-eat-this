import os
import sys
from pathlib import Path

import qrcode

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "frontend"))

ALLERGENS = [
    "gluten", "milk", "eggs", "fish", "crustaceans", "molluscs",
    "mustard", "nuts", "peanuts", "sesame", "soya", "sulphites",
    "celery", "lupin",
]

BASE_URL = os.environ.get("FRONTEND_BASE_URL", "http://localhost:3000")
OUT_DIR = Path(__file__).resolve().parent.parent / "qr-codes"


def main():
    OUT_DIR.mkdir(exist_ok=True)
    for allergen in ALLERGENS:
        url = f"{BASE_URL}/allergen/{allergen}"
        img = qrcode.make(url)
        out_path = OUT_DIR / f"{allergen}.png"
        img.save(out_path)
        print(f"{allergen:12s} -> {url}  ({out_path.name})")


if __name__ == "__main__":
    main()
