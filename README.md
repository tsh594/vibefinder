# 🎵 VibeFinder 1.0 — Music Recommender Simulation

> **Base project:** *Music Recommender Simulation* (Modules 1–3). VibeFinder is a content-based music recommender that scores a small song catalog against a user's "taste profile" (genre, mood, energy, danceability, acousticness) and returns the top K with a **transparent score breakdown**. This Applied AI System extension adds a **reliability/evaluation harness**, **guardrails**, **logging**, **confidence scoring**, and an **interactive web demo**.

---

## 🎯 Title & Summary

VibeFinder ranks songs by computing a weighted similarity score between each track and a user's stated preferences. Every recommendation comes with a *why* (e.g. `genre match (pop) +2.0; mood match (happy) +1.0; energy similarity 0.92`). The system is designed for classroom exploration of how recommenders work, where bias enters, and how to test them.

## 🧱 Architecture Overview

```
data/songs.csv          ← catalog (20 songs, 7 genres)
       │
       ▼
src/recommender.py      ← Song / UserProfile / score_song / recommend_songs
       │                  (genre +2, mood +1, energy/dance/acoustic similarity, diversity penalty)
       ▼
┌──────────────┬─────────────────────┐
│ src/main.py  │ src/evaluation.py   │
│ CLI demo     │ Reliability harness │
│              │  • confidence score │
│              │  • guardrails       │
│              │  • logging          │
└──────────────┴─────────────────────┘
       │
       ▼
tests/test_recommender.py   ← pytest coverage of OOP API
```

See `assets/architecture.md` for the Mermaid diagram.

## ⚙️ Setup

```bash
git clone <your-repo-url>
cd vibefinder
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Run

```bash
# CLI recommendations for 5 profiles
python -m src.main

# Reliability harness with guardrails + confidence scoring
python -m src.evaluation

# Tests
pytest -q
```

## 🧪 Sample Interactions

**Input:** `Pop/Happy Dancer` (genre=pop, mood=happy, energy=0.8, dance=0.85)
**Output (top 3):**
1. `Levitating — Dua Lipa` — `genre match (pop) +2.0; mood match (happy) +1.0; energy similarity 0.95; dance 0.97; acoustic 0.95`
2. `Get Lucky — Daft Punk` — `genre +2.0; mood +1.0; energy 1.00`
3. `Blinding Lights — The Weeknd` — `genre +2.0; mood +1.0; energy 0.93`

**Input:** `Edge Case (rock + sad, energy 0.9)`
**Output:** Top picks become *intense* rock (Chop Suey!, Enter Sandman) — the +2.0 genre weight + energy similarity outweigh the missing mood match. This is the **filter bubble** documented in `model_card.md`.

**Input:** `Chill Lofi Lover`
**Output:** `Library Rain`, `Midnight Coding`, `Focus Flow` — diversity penalty kicks in to demote the second LoRoom track.

## 🧠 Design Decisions & Trade-offs

- **Weighted sum over ML model** — interpretable, easy to explain, every reason traceable.
- **Genre +2.0 vs mood +1.0** — matches user expectations ("rock fans want rock") but creates a known filter bubble (documented honestly in the model card).
- **Diversity penalty (×0.8 for repeat artists)** — cheap, reproducible alternative to randomness.
- **Dual API** — functional `score_song`/`recommend_songs` for the CLI + OOP `Recommender` for testability.

## ✅ Testing Summary

- **Unit tests:** 2/2 passed (`pytest`).
- **Reliability harness (`evaluation.py`):** 5 profiles tested. 4/5 pass all guardrails. The "rock + sad" edge case correctly triggers the *missing-mood* warning.
- **Confidence scores:** average ~0.6 across profiles (score spread / max). Low-confidence runs flag profiles where the catalog can't satisfy preferences.
- **Logging:** every evaluation written to `evaluation.log` + summary to `evaluation_report.txt`.

## 🎬 Demo Walkthrough

<!-- ============================================================
     DEMO PLACEHOLDER — replace ONE of the two options below
     before submitting. Delete the option you don't use.
     ============================================================ -->

**Option A — Loom video:** *<paste Loom link here>*

**Option B — Animated GIF walkthrough:**

![VibeFinder demo](assets/demo.gif)

> Drop your recorded `demo.gif` into `assets/demo.gif` and the image above will render automatically on GitHub.

The walkthrough covers: (1) CLI run on 3 profiles, (2) reliability harness output with guardrail warnings, (3) the web demo showing live re-ranking when sliders change.

## 🪞 Reflection

**Biggest learning moment.** Watching the "rock + sad" edge case return high-energy rock made me see weight choices as value judgments — every +2.0 is a designer telling the system what matters.

**AI collaboration — a helpful moment.** Copilot suggested computing energy similarity as `1 − |song.energy − target|` instead of a raw difference. That single change made scores intuitive (0–1 scale) and comparable across features.

**AI collaboration — a flawed moment.** Copilot once proposed `random.shuffle` for "diversity," which would break reproducibility and confidence scoring. I rejected it and used a deterministic ×0.8 penalty per repeat artist instead.

**What surprised me.** A 30-line scoring function "feels" like a real recommender. Users immediately treat the explanations as truth — which is exactly why model cards matter.

**What I'd try next.** Hybrid filtering with a tiny synthetic listening-history matrix, and an LLM-generated "vibe summary" of the top 5 picks.

See `model_card.md` for full responsible-AI documentation.
