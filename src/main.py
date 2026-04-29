"""Music Recommender Simulation - Main CLI."""
from src.recommender import load_songs, recommend_songs
from tabulate import tabulate


def print_recommendations_table(profile_name, user_prefs, recommendations):
    """Pretty-print recommendations as a table."""
    print("\n" + "=" * 80)
    print(f"🎵 Recommendations for: {profile_name}")
    print(f"   Genre: {user_prefs.get('favorite_genre', 'any')} | "
          f"Mood: {user_prefs.get('favorite_mood', 'any')} | "
          f"Target Energy: {user_prefs.get('target_energy', 'N/A')}")
    print("=" * 80)

    rows = []
    for i, (song, score, reasons) in enumerate(recommendations, 1):
        why = "; ".join(reasons)
        rows.append([i, song['title'], song['artist'], f"{score:.2f}",
                     why[:80] + "..." if len(why) > 80 else why])

    print(tabulate(rows, headers=["#", "Title", "Artist", "Score", "Why?"], tablefmt="grid"))
    print()


PROFILES = {
    "🎉 Pop/Happy Dancer": {
        "favorite_genre": "pop", "favorite_mood": "happy",
        "target_energy": 0.8, "target_danceability": 0.85, "likes_acoustic": False,
    },
    "🤘 High-Energy Rocker": {
        "favorite_genre": "rock", "favorite_mood": "intense",
        "target_energy": 0.95, "target_danceability": 0.55, "likes_acoustic": False,
    },
    "🍃 Chill Lofi Lover": {
        "favorite_genre": "lofi", "favorite_mood": "chill",
        "target_energy": 0.35, "target_danceability": 0.50, "likes_acoustic": True,
    },
    "🤠 Country Sad Soul": {
        "favorite_genre": "country", "favorite_mood": "sad",
        "target_energy": 0.35, "target_danceability": 0.55, "likes_acoustic": True,
    },
    "🔥 Edge Case (rock + sad)": {
        "favorite_genre": "rock", "favorite_mood": "sad",
        "target_energy": 0.9, "target_danceability": 0.6, "likes_acoustic": False,
    },
}


def main():
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from catalog.\n")

    for name, prefs in PROFILES.items():
        recs = recommend_songs(prefs, songs, k=5)
        print_recommendations_table(name, prefs, recs)


if __name__ == "__main__":
    main()
