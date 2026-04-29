# 🎧 Model Card: VibeFinder 1.0

## 1. Model Name
**VibeFinder 1.0** — content-based music recommender for educational use.

## 2. Goal / Task
Suggest 5 songs from a small catalog matching a user's stated preferences (genre, mood, energy, danceability, acousticness) and explain *why* each was picked.

## 3. Data Used
- **20 songs**, 7 genres (pop, rock, lofi, country, hiphop, ambient, jazz, synthwave).
- Features: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`.
- **Limits:** no real listening history, hand-curated, missing electronic/metal/classical, English-language bias.

## 4. Algorithm Summary (plain language)
Each song earns points:
- **+2.0** if its genre matches the user's favorite.
- **+1.0** if its mood matches.
- Up to **+1.0** based on how close its energy is to the target (`1 − |diff|`).
- Up to **+1.0** for danceability closeness (if specified).
- Up to **+1.0** for acoustic preference alignment.
- **×0.8** penalty if the artist already appears higher in the list (diversity).
The 5 highest scorers are returned.

## 5. Observed Behavior / Biases
- **Genre filter bubble:** the +2.0 genre bonus dominates. A rock fan asking for "sad" mood still gets intense rock.
- **Small-catalog repetition:** the same songs surface across profiles.
- **Binary acoustic preference:** doesn't model "I like a little acoustic."
- **Pop over-representation:** a 5th of the catalog is pop, slightly inflating its match rate.

## 6. Evaluation Process
- **Unit tests** (pytest): 2/2 pass — verifies sort order and explanation output.
- **Reliability harness** (`src/evaluation.py`): runs 5 user profiles, computes a **confidence score** (top-vs-bottom score spread), and checks 3 **guardrails** (duplicate artist, low genre diversity, missing favorite genre). Logs to `evaluation.log`, summary to `evaluation_report.txt`.

**Profile comparisons:**
- *Pop/Happy* vs *Chill Lofi*: pop returns Levitating/Get Lucky (high energy + valence); lofi returns Library Rain/Midnight Coding (low energy, high acousticness). Confirms energy + acoustic features actually steer ranking.
- *High-Energy Rocker* vs *Country Sad Soul*: rock returns Enter Sandman/Chop Suey! (energy ≈ 0.95); country returns Hurt/Jolene (low energy, acoustic-leaning). Genre + energy both clearly contribute.
- *Pop/Happy* vs *Edge Case (rock + sad, energy 0.9)*: pop is well-served; edge case returns rock songs that **don't match the sad mood**, exposing that genre + energy outweigh mood (+2.0 vs +1.0). This is the central bias finding.

**Plain-language example:** "Gym Hero" keeps showing up for "Happy Pop" users because it's tagged *pop* (+2) and has very high energy (close to 0.8 target, +~0.85), so it scores ~3.85 even though most pop fans wouldn't call it a happy track.

## 7. Intended & Non-Intended Use
**Intended:** classroom demonstration of content-based filtering, scoring transparency, and bias auditing.
**Not intended:** production recommendations, content moderation, royalty / payout decisions, or any automated decision affecting real listeners or artists.

## 8. Ideas for Improvement
1. Normalize feature weights (z-scores) instead of fixed point bonuses.
2. Add hybrid collaborative filtering with a synthetic interaction matrix.
3. Replace binary acoustic preference with a continuous target.
4. Expand catalog to 200+ tracks across 15+ genres.

## 9. Reflection on AI Collaboration
- **Helpful suggestion:** Copilot proposed `1 − |song.energy − target|` for the energy-similarity formula. Clean, bounded in [0,1], and made the reason strings interpretable.
- **Flawed suggestion:** Copilot once proposed `random.shuffle(top_k)` for "diversity." That would have broken reproducibility and made the confidence score meaningless. Replaced with a deterministic ×0.8 penalty for repeat artists.
- **Surprise:** raising the genre weight from 2.0 → 5.0 collapsed every profile into pop/rock — a vivid in-class demo of how a single hyperparameter creates a filter bubble.
- **Could it be misused?** A naive deployment could entrench narrow taste. Mitigation: surface explanations to the user and force a diversity floor.
