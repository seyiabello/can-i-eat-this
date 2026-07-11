import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models import MenuItem, SafetyStatus
from validate import deterministic_check, validate_response

CLEAN_ITEM = MenuItem(
    item="Margherita pizza slice",
    allergen_notes_raw="WHEAT, MILK",
    confirmed_allergens=["gluten", "milk"],
    ambiguous_flag=False,
    ambiguous_reason=None,
    price="£2.80",
)

AMBIGUOUS_ITEM = MenuItem(
    item="Veggie chilli (vegan?)",
    allergen_notes_raw="celery. may contain traces of nuts",
    confirmed_allergens=["celery"],
    ambiguous_flag=True,
    ambiguous_reason="may contain traces of nuts",
    price="£4.50",
)


def test_valid_unsafe_passes_through():
    result = validate_response("unsafe", "Contains gluten and milk.", CLEAN_ITEM, ["gluten", "milk"])
    assert result.status == SafetyStatus.UNSAFE


def test_valid_safe_passes_through_for_clean_item():
    result = validate_response("safe", "No nut allergens listed.", CLEAN_ITEM, [])
    assert result.status == SafetyStatus.SAFE


def test_unparseable_output_defaults_to_unverified():
    result = validate_response("probably fine", "garbage output", CLEAN_ITEM, [])
    assert result.status == SafetyStatus.UNVERIFIED


def test_ambiguous_item_cannot_be_reported_safe():
    result = validate_response("safe", "No nuts in the confirmed ingredients.", AMBIGUOUS_ITEM, [])
    assert result.status == SafetyStatus.UNVERIFIED


def test_ambiguous_item_can_still_be_reported_unsafe():
    result = validate_response("unsafe", "Contains celery.", AMBIGUOUS_ITEM, ["celery"])
    assert result.status == SafetyStatus.UNSAFE


def test_deterministic_check_flags_confirmed_allergen_unsafe():
    result = deterministic_check(CLEAN_ITEM, "milk")
    assert result.status == SafetyStatus.UNSAFE
    assert result.matched_allergens == ["milk"]


def test_deterministic_check_is_case_insensitive():
    result = deterministic_check(CLEAN_ITEM, "MILK")
    assert result.status == SafetyStatus.UNSAFE


def test_deterministic_check_clean_item_returns_safe():
    result = deterministic_check(CLEAN_ITEM, "peanuts")
    assert result.status == SafetyStatus.SAFE


def test_deterministic_check_ambiguous_item_never_safe():
    result = deterministic_check(AMBIGUOUS_ITEM, "nuts")
    assert result.status == SafetyStatus.UNVERIFIED


def test_deterministic_check_ambiguous_item_still_flags_confirmed_allergen():
    result = deterministic_check(AMBIGUOUS_ITEM, "celery")
    assert result.status == SafetyStatus.UNSAFE
