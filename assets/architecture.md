# System Architecture

```mermaid
flowchart LR
    A[User Preferences<br/>genre, mood, energy,<br/>danceability, acoustic] --> B[score_song]
    C[(data/songs.csv<br/>20 tracks)] --> D[load_songs]
    D --> E[For each song]
    E --> B
    B --> F[Score + Reasons]
    F --> G[Sort desc by score]
    G --> H[Diversity penalty<br/>x0.8 repeat artist]
    H --> I[Top K Recommendations]
    I --> J[CLI / Web UI]
    I --> K[evaluation.py<br/>guardrails + confidence + logs]
    K --> L[(evaluation.log<br/>evaluation_report.txt)]
```

**Components**
- **Retriever / Loader** — `load_songs` (csv → typed dicts).
- **Logic / Scorer** — `score_song` deterministic weighted sum with reasons.
- **Ranker** — `recommend_songs` sort + diversity penalty.
- **Evaluator** — `evaluation.py` runs profiles, computes confidence, checks guardrails, logs everything.
- **Human checkpoint** — CLI tables and the web demo make every score auditable by a human.
