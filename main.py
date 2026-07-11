import logging
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from models import AllergenQuery, AllergenResponse, SafetyStatus, StructuredCheckQuery
from rag.generator import generate
from rag.retriever import load_menu, retrieve_item
from validate import deterministic_check, validate_response

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "app.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)
logger = logging.getLogger("can_i_eat_this")

app = FastAPI(title="Can I Eat This?")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

menu = load_menu()


@app.get("/menu")
def get_menu():
    return menu


@app.post("/check", response_model=AllergenResponse)
def check(query: StructuredCheckQuery) -> AllergenResponse:
    item = next((m for m in menu if m.item == query.item), None)

    if item is None:
        result = AllergenResponse(
            status=SafetyStatus.UNVERIFIED,
            item=None,
            explanation="Unknown menu item.",
            matched_allergens=[],
        )
        logger.info("structured item=%r allergen=%r state=None", query.item, query.allergen)
        return result

    result = deterministic_check(item, query.allergen)
    logger.info(
        "structured item=%r allergen=%r ambiguous=%s final_state=%s",
        item.item,
        query.allergen,
        item.ambiguous_flag,
        result.status.value,
    )
    return result


@app.get("/allergen-check", response_model=list[AllergenResponse])
def allergen_check(allergen: str) -> list[AllergenResponse]:
    results = [deterministic_check(item, allergen) for item in menu]
    counts = {
        s.value: sum(1 for r in results if r.status.value == s.value)
        for s in SafetyStatus
    }
    logger.info("allergen_scan allergen=%r counts=%s", allergen, counts)
    return results


@app.post("/ask", response_model=AllergenResponse)
def ask(query: AllergenQuery) -> AllergenResponse:
    item = retrieve_item(query.question, menu)

    if item is None:
        result = AllergenResponse(
            status=SafetyStatus.UNVERIFIED,
            item=None,
            explanation="Couldn't match this question to a menu item.",
            matched_allergens=[],
        )
        logger.info("query=%r item=None state=%s", query.question, result.status.value)
        return result

    llm_output = generate(query.question, item)
    result = validate_response(
        llm_status=llm_output["status"],
        explanation=llm_output["explanation"],
        item=item,
        matched_allergens=llm_output["matched_allergens"],
    )

    logger.info(
        "query=%r item=%r retrieved_ambiguous=%s llm_status=%r final_state=%s",
        query.question,
        item.item,
        item.ambiguous_flag,
        llm_output["status"],
        result.status.value,
    )
    return result
