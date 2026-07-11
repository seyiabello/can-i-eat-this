from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SafetyStatus(str, Enum):
    SAFE = "safe"
    UNSAFE = "unsafe"
    UNVERIFIED = "unverified"


class MenuItem(BaseModel):
    item: str
    allergen_notes_raw: str
    confirmed_allergens: list[str]
    ambiguous_flag: bool
    ambiguous_reason: Optional[str] = None
    price: Optional[str] = None


class AllergenQuery(BaseModel):
    question: str


class StructuredCheckQuery(BaseModel):
    item: str
    allergen: str


class AllergenResponse(BaseModel):
    status: SafetyStatus
    item: Optional[str] = None
    explanation: str
    matched_allergens: list[str] = []
