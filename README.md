# Can I eat this?

A quick allergen check for a dining hall counter, built for Compass Group's AI Engineer pre-work brief.

The scenario the brief gives you: it's 12:40, the queue is moving, the person in front has a severe nut allergy, the allergen folder is behind the counter, and the server started on Monday. This app is meant to answer "can they eat this?" in about the time it takes to tap a screen twice.

**Live demo:** https://frontend-rose-three-32.vercel.app (backend at https://can-i-eat-this-api.fly.dev). The QR codes in `qr-codes/` point at the live URL and are scannable from a real phone.

## What it actually does

You pick a dish, then pick an allergen. You get back one of three answers: safe, unsafe, or "can't confirm, ask staff." That third state is the whole point of the project. A lot of real dining hall allergen data is messy on purpose, things like "may contain traces," "ask counter," or just a blank field, and the worst thing this system could do is guess safe when it doesn't actually know. So it never does. If the underlying data is ambiguous or missing, the answer is always unverified, no matter what.

There's also a free-text box for questions that don't fit the two-tap flow ("is this okay for a shellfish allergy?"), and a counter view that simulates what a QR code stuck on the counter would open: the whole menu, scanned against one allergen, sorted so the dishes you need to worry about show up first. That covers the person in the queue behind you as well as the customer at the front, and the server who started on Monday and doesn't know the menu yet either.

## Architecture

![Two routes through the system, one of which never touches an LLM](assets/architecture-diagram.png)

### The three-state design

`safe`, `unsafe`, `unverified`. Never a confidence score. A confidence score just moves the guessing problem onto the person reading it, and they have thirty seconds, not the time to interpret "72% safe." The unverified state exists because a lot of real allergen data is genuinely uncertain, and pretending otherwise is how someone gets hurt.

### Two routes, and the LLM only covers one of them

This is the decision worth defending hardest, so it's worth explaining properly.

`POST /check` takes an item and an allergen, both already known because they came from a button tap. Checking whether an allergen is on the confirmed list for that dish doesn't need language understanding, it's a lookup. So it is one, in `validate.py`. No LLM call, no network round trip to OpenAI, nothing to hallucinate, and it answers in well under a second.

`POST /ask` takes a free-text question. This is where GPT-4o-mini actually gets used, because turning "does this have anything a shellfish allergy would react to?" into "check the crustaceans and molluscs fields for this dish" is a real language problem that a keyword match handles badly.

`GET /allergen-check` reuses the same deterministic logic across the whole menu at once. That's what powers the counter view and the QR codes, so scanning a QR code never touches the LLM either.

The system started out routing everything through the LLM, including the button flow. It got pulled apart once it was obvious that most of the app didn't need AI at all, just correctly structured data. That's a stronger answer to "why does this need an LLM" than routing everything through one, since it shows the AI is scoped to the one part of the problem that actually needs it rather than being the default tool for everything.

### Why no vector database

The menu is 30 structured JSON records, not a large unstructured corpus. Matching a query to the right dish is an exact, small-scale problem that substring and fuzzy string matching solve for free, with no embedding pipeline, no external service, and no risk of returning the wrong dish with high confidence, which is what approximate nearest-neighbour search can do and a real problem for a system whose entire job is not guessing wrong. A vector database would earn its place if the catalogue grew to thousands of dishes across many sites, or if menus were being ingested from photos with no fixed structure. Neither is true here yet.

### The ops loop, today and later

![What's actually logged today versus what a full LLMOps loop would add](assets/ops-loop-diagram.png)

Every query gets logged with the question, the retrieved item, which route it took, and the final state, and a rule-based check confirms the output is always one of the three valid states. That's genuinely useful and cheap to keep. What it deliberately skips is the full evaluate, observe, diagnose, release loop you'd want once this is a real production service handling menu changes and traffic at scale. Building that now would be solving a maintenance problem this prototype doesn't have yet.

## How it's built

```
main.py                    FastAPI app: /menu, /check, /ask, /allergen-check
models.py                  Pydantic schema, including the three-state enum
validate.py                the actual safety logic, deterministic and LLM-output paths
rag/retriever.py           matches free text to a menu item, no embeddings
rag/generator.py           the one place an LLM gets called
data/menu.json             30 synthetic dishes, deliberately messy, all 14 EU allergens
frontend/                  Next.js app: two-tap picker, free-text box, counter view
qr-codes/                  generated QR codes, one per allergen
scripts/generate_qr_codes.py   regenerates the QR codes against any base URL
assets/                    the two architecture diagrams above, plus their editable HTML
tests/                     unit tests for the safety logic
Dockerfile, fly.toml       backend deployment to Fly.io
```

## Running it locally

Backend:

```
cd can-i-eat-this
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env
```

Add your OpenAI API key to `.env`, then:

```
.venv\Scripts\python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Frontend:

```
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Tests

```
.venv\Scripts\python -m pytest tests/ -v
```

Covers the ambiguous-item override (an item flagged ambiguous can never come back as safe, even if the model says otherwise), the deterministic lookup, and the fallback to unverified when the model output can't be parsed.

## Dataset

`data/menu.json` extends the brief's own ten-item starter menu to thirty. It keeps the original messiness on purpose (inconsistent capitalisation, "ask counter", a field that just says "null") and adds enough variety to cover celery, cereals with gluten, crustaceans, eggs, fish, lupin, milk, molluscs, mustard, tree nuts, peanuts, sesame, soya, and sulphites. One dish, the chicken satay skewers, has its allergen hidden in the sauce rather than the dish name on purpose, since that's a realistic way allergen information gets missed. Nuts and peanuts are kept as separate confirmed allergens throughout, matching how they're actually treated under EU allergen labelling, not merged into one "nuts" bucket.

## Deployment

Backend on Fly.io, frontend on Vercel, both on free tiers. The OpenAI key is set as a Fly secret, never baked into the image or committed anywhere. A live public deployment wasn't required by the brief, a laptop demo would have been fine, but having a real URL means the QR codes actually work if anyone wants to scan one during the pitch.

## What I'd build next

- A batch pipeline to turn a photo of a real laminated menu into structured entries like these, since hand-curating the dataset doesn't scale past a demo
- Basic auth and a proper admin view for updating menu data day to day
- The eval, observe, diagnose, release loop described above, once this is serving real traffic rather than a one-off demo
