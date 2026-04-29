"""VibeFinder recommender core.

Provides:
- `Song`, `UserProfile` dataclasses
- `Recommender` OOP class (used by tests)
- `load_songs`, `score_song`, `recommend_songs` functional API (used by main.py)
"""
import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


# ==================== Data Classes ====================

@dataclass
class Song:
    """Represents a song with all its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


# ==================== OOP Recommender ====================

class Recommender:
    """Object-oriented recommender that uses Song and UserProfile objects."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top k songs sorted by relevance score."""
        scored = [(self._compute_score(user, s), s) for s in self.songs]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate a human-readable explanation of why a song was recommended."""
        score, reasons = self._score_with_reasons(user, song)
        return f"Score: {score:.2f}\nReasons: " + "; ".join(reasons)

    def _compute_score(self, user: UserProfile, song: Song) -> float:
        score, _ = self._score_with_reasons(user, song)
        return score

    def _score_with_reasons(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons: List[str] = []

        if song.genre == user.favorite_genre:
            score += 2.0
            reasons.append(f"genre match ({song.genre}) +2.0")

        if song.mood == user.favorite_mood:
            score += 1.0
            reasons.append(f"mood match ({song.mood}) +1.0")

        energy_sim = 1.0 - abs(song.energy - user.target_energy)
        score += energy_sim
        reasons.append(f"energy similarity {energy_sim:.2f}")

        acoustic_score = song.acousticness if user.likes_acoustic else 1.0 - song.acousticness
        score += acoustic_score
        reasons.append(f"acoustic preference {acoustic_score:.2f}")

        return score, reasons


# ==================== Functional Implementation ====================

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV and return list of dicts with numeric fields cast."""
    songs: List[Dict] = []
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['id'] = int(row['id'])
            for key in ('energy', 'tempo_bpm', 'valence', 'danceability', 'acousticness'):
                row[key] = float(row[key])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song based on user preferences. Returns (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    if user_prefs.get('favorite_genre') == song['genre']:
        score += 2.0
        reasons.append(f"genre match ({song['genre']}) +2.0")

    if user_prefs.get('favorite_mood') == song['mood']:
        score += 1.0
        reasons.append(f"mood match ({song['mood']}) +1.0")

    target_energy = user_prefs.get('target_energy', 0.5)
    energy_sim = 1.0 - abs(song['energy'] - target_energy)
    score += energy_sim
    reasons.append(f"energy similarity {energy_sim:.2f}")

    if 'target_danceability' in user_prefs:
        dance_sim = 1.0 - abs(song['danceability'] - user_prefs['target_danceability'])
        score += dance_sim
        reasons.append(f"danceability similarity {dance_sim:.2f}")

    if 'likes_acoustic' in user_prefs:
        acoustic_score = song['acousticness'] if user_prefs['likes_acoustic'] else 1.0 - song['acousticness']
        score += acoustic_score
        reasons.append(f"acoustic preference {acoustic_score:.2f}")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5):
    """Rank songs by score with a diversity penalty for repeat artists."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))
    scored.sort(key=lambda x: x[1], reverse=True)

    artists_seen = set()
    penalized = []
    for song, score, reasons in scored:
        if song['artist'] in artists_seen:
            score *= 0.8
            reasons = reasons + ["diversity penalty -0.2x"]
        else:
            artists_seen.add(song['artist'])
        penalized.append((song, score, reasons))
    penalized.sort(key=lambda x: x[1], reverse=True)
    return penalized[:k]
