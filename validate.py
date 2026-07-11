from models import AllergenResponse, MenuItem, SafetyStatus


def validate_response(
    llm_status: str,
    explanation: str,
    item: MenuItem,
    matched_allergens: list[str],
) -> AllergenResponse:
    try:
        status = SafetyStatus(llm_status.strip().lower())
    except ValueError:
        return AllergenResponse(
            status=SafetyStatus.UNVERIFIED,
            item=item.item,
            explanation="Could not parse a valid safety state from the model output.",
            matched_allergens=matched_allergens,
        )

    if item.ambiguous_flag and status == SafetyStatus.SAFE:
        return AllergenResponse(
            status=SafetyStatus.UNVERIFIED,
            item=item.item,
            explanation=(
                f"Menu data for '{item.item}' is flagged ambiguous "
                f"({item.ambiguous_reason}) - cannot confirm safe regardless of model output."
            ),
            matched_allergens=matched_allergens,
        )

    return AllergenResponse(
        status=status,
        item=item.item,
        explanation=explanation,
        matched_allergens=matched_allergens,
    )


def deterministic_check(item: MenuItem, allergen: str) -> AllergenResponse:
    """Rule-based classification for structured (item, allergen) lookups.

    No LLM involved - when both the item and the allergen are already known
    (e.g. picked from buttons), this is a plain membership check against
    confirmed_allergens plus the same ambiguous-item override used for LLM
    output. The LLM is reserved for free-text questions that need parsing.
    """
    allergen_norm = allergen.strip().lower()
    matched = [a for a in item.confirmed_allergens if a.lower() == allergen_norm]

    if matched:
        return AllergenResponse(
            status=SafetyStatus.UNSAFE,
            item=item.item,
            explanation=f"{item.item} is confirmed to contain {allergen_norm}.",
            matched_allergens=matched,
        )

    if item.ambiguous_flag:
        return AllergenResponse(
            status=SafetyStatus.UNVERIFIED,
            item=item.item,
            explanation=(
                f"Menu data for '{item.item}' is flagged ambiguous "
                f"({item.ambiguous_reason}) - cannot confirm safe."
            ),
            matched_allergens=[],
        )

    return AllergenResponse(
        status=SafetyStatus.SAFE,
        item=item.item,
        explanation=f"No {allergen_norm} listed in the confirmed allergens for {item.item}.",
        matched_allergens=[],
    )
