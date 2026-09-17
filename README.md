# Support Assistant — Rule-Based & FAQ Chatbot

📄 [Full project write-up & interview notes (PDF)](docs/project-showcase.pdf)

A lightweight conversational assistant with two front ends — a command-line
version and a Flask web UI — that answers user questions using a two-tier
matching system: fuzzy FAQ lookup first, then intent-based fallback.

## What it does

- Takes free-text user input and returns a relevant response
- First checks a curated FAQ knowledge base using **fuzzy string matching**
  (so "wat r ur hours" still matches "what are your working hours")
- Falls back to lightweight **intent classification** (greeting, help, goodbye,
  etc.) when nothing in the FAQ is a good enough match
- Ships as both a terminal chatbot (`main.py`) and a Flask web chat interface
  (`chatbot/web.py`) sharing the exact same logic underneath

## Why this project

Most beginner chatbot tutorials do one of two things: hardcode a handful of
`if/elif` string checks, or jump straight to a heavyweight NLP framework.
I wanted something in between — a system that's honest about being
rule-based, but resilient to the messy way people actually type (typos,
partial phrasing, different word order), and structured cleanly enough that
a real ML intent classifier or LLM call could be swapped in later without
touching the interface layer.

## Architecture

```
chatbot_project/
├── main.py                 # CLI entry point
├── chatbot/
│   ├── nlp.py               # keyword-based intent classifier
│   ├── responses.py         # intent -> canned response mapping
│   ├── faq.py                # fuzzy-matches user text against data/faq.json
│   ├── web.py                 # Flask app: routes + chat history
│   └── templates/chat.html    # web chat UI
├── data/faq.json              # editable FAQ knowledge base
└── requirements.txt
```

**Request flow (web):**

```
User submits message
        │
        ▼
find_faq_answer(text)   ──► rapidfuzz scores text against every FAQ phrasing
        │
   match ≥ threshold?
   ├── yes → return FAQ answer
   └── no  → get_intent(text) → get_response(intent)
        │
        ▼
Append (sender, text) to chat_history → re-render chat.html
```

The CLI (`main.py`) and the web app (`chatbot/web.py`) both call into the
same `chatbot` package, so the matching logic only lives in one place.

## Tech stack

| Layer            | Choice                          | Why                                                                 |
|-------------------|---------------------------------|----------------------------------------------------------------------|
| Web framework      | Flask                            | Minimal, no build step, easy to reason about for a small app         |
| Fuzzy matching     | RapidFuzz (`WRatio` scorer)       | Handles typos/rewording without training a model; fast, in-memory     |
| Templating          | Jinja2 (via Flask)                | Server-rendered, no client framework needed for this scope           |
| State                | In-memory list                     | Simple for a demo; documented as the first thing to swap for a DB     |

## Key design decisions

- **FAQ before intent, not the other way around.** Specific knowledge-base
  answers are more useful than generic ones, so they take priority whenever
  the match score clears the threshold.
- **One shared package, two entry points.** `nlp.py`, `responses.py`, and
  `faq.py` don't know or care whether they're being called from a terminal
  loop or a Flask route — that separation made it trivial to add the web UI
  after the CLI version already worked.
- **Fuzzy matching over keyword lists for the FAQ.** A plain `if phrase in
  text` approach breaks the moment a user rewords a question slightly.
  RapidFuzz's `WRatio` scorer tolerates typos, word order, and partial
  phrasing while staying fast enough for real-time use.
- **Data-driven FAQ.** Knowledge lives in `data/faq.json`, not in code —
  non-technical content changes don't require touching Python.

## Challenges & how they were solved

- **Import path consistency across two entry points.** Running the CLI
  script directly vs. running the Flask app as a package (`python -m
  chatbot.web`) requires different import styles. Standardized both entry
  points on package-relative imports (`from chatbot.nlp import ...`) so the
  whole project has one predictable way to run it.
- **False-positive fuzzy matches.** An unconstrained fuzzy match will
  confidently match almost anything to *something*. Solved with a tunable
  `threshold` parameter (default 75) so weak matches fall through to the
  intent system instead of returning a wrong FAQ answer.

## Possible next steps

- Persist `chat_history` to a database instead of an in-memory list (currently
  resets on every server restart)
- Swap the keyword-based `get_intent()` for a small ML classifier or an LLM
  call, without changing `responses.py` or the web layer at all
- Add per-session history (currently global/shared across all visitors)
- Add automated tests for `find_faq_answer` and `get_intent` edge cases

## Running it

```bash
pip install -r requirements.txt

# CLI
python main.py

# Web (from the project root)
python -m chatbot.web
```

## Interview Talking Points

**30-second pitch**

> "I built a rule-based chatbot with two front ends — CLI and a Flask web
> app — that answers questions using fuzzy FAQ matching first, then falls
> back to keyword-based intent detection. The interesting part isn't the
> AI, it's the engineering: clean separation between matching logic and
> interface, so the same core code drives both entry points."

**"Walk me through it"**
Message comes in, checked against an FAQ knowledge base using RapidFuzz's
fuzzy scorer, so typos and reworded questions still match. If nothing scores
above the threshold, it falls back to a simple keyword-based intent
classifier. Whichever layer answers, the response flows back through the
same interface — printed to terminal or rendered into the Flask chat UI.

**"What was the hardest part?"**
Two real bugs, fixed: an import path inconsistency between the CLI and Flask
entry points, standardized on package-relative imports; and fuzzy-match
false positives, solved with a tunable score threshold so weak matches fall
through to intent detection instead of returning a wrong answer.

**"Why fuzzy matching instead of keyword checks?"**
Plain substring checks break the moment someone rewords a question.
RapidFuzz tolerates typos and word order while staying fast enough for
real-time use, with no model training required.

**"What would you improve given more time?"**
Persist chat history instead of in-memory storage, add per-session history
instead of one shared global history, swap the keyword classifier for a
small ML model or LLM call (architecture already isolates that logic), and
add tests for matching edge cases.

**"Why structure it as a package with two entry points?"**
Keeps business logic ignorant of how it's invoked, so adding the web UI
later didn't require touching the CLI code at all — a real
separation-of-concerns decision, not just file organization.