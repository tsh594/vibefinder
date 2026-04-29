"""evaluation.py – Reliability testing harness for VibeFinder."""
import logging
from datetime import datetime
from src.recommender import load_songs, recommend_songs
from src.main import PROFILES

logging.basicConfig(
    filename='evaluation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


def confidence_score(recommendations):
    """Confidence based on score spread between top and bottom recommendation."""
    if not recommendations:
        return 0.0
    scores = [s for _, s, _ in recommendations]
    hi, lo = max(scores), min(scores)
    if hi == lo:
        return 0.5
    return min(1.0, (hi - lo) / hi)


def check_guardrails(recommendations, user_prefs):
    """Detect duplicate artists, low diversity, missing favorite genre."""
    issues = []
    artists = [r[0]['artist'] for r in recommendations]
    if len(set(artists)) < len(artists):
        issues.append("Duplicate artist detected")

    genres = [r[0]['genre'] for r in recommendations]
    if len(set(genres)) == 1:
        issues.append("Low genre diversity – all same genre")

    fav = user_prefs.get('favorite_genre')
    if fav and not any(r[0]['genre'] == fav for r in recommendations):
        issues.append(f"No '{fav}' song in top recommendations")

    return issues


def evaluate_profile(name, prefs, songs, k=5):
    logging.info(f"Evaluating: {name} | prefs={prefs}")
    recs = recommend_songs(prefs, songs, k=k)
    if not recs:
        logging.error("No recommendations generated")
        return None

    conf = confidence_score(recs)
    issues = check_guardrails(recs, prefs)
    top_song, top_score, _ = recs[0]
    logging.info(f"Top: {top_song['title']} by {top_song['artist']} ({top_score:.2f})")
    logging.info(f"Confidence: {conf:.2f} | Issues: {issues}")

    return {
        "profile": name, "preferences": prefs, "recommendations": recs,
        "confidence": conf, "issues": issues,
    }


def run_full_evaluation():
    songs = load_songs("data/songs.csv")
    results = [evaluate_profile(n, p, songs) for n, p in PROFILES.items()]
    results = [r for r in results if r]

    print("\n" + "=" * 70)
    print("📊 RELIABILITY TEST SUMMARY")
    print("=" * 70)
    passed = 0
    for r in results:
        status = "✅" if not r['issues'] else "⚠️"
        if not r['issues']:
            passed += 1
        print(f"\n{status} {r['profile']}")
        print(f"   Confidence: {r['confidence']:.2f}")
        if r['issues']:
            print(f"   Issues: {', '.join(r['issues'])}")
        print(f"   Top pick: {r['recommendations'][0][0]['title']} "
              f"by {r['recommendations'][0][0]['artist']}")

    print(f"\n🎯 Result: {passed}/{len(results)} profiles passed all guardrails")

    with open("evaluation_report.txt", "w", encoding="utf-8") as f:
        f.write(f"EVALUATION REPORT — {datetime.now()}\n\n")
        for r in results:
            f.write(f"Profile: {r['profile']}\n")
            f.write(f"Confidence: {r['confidence']:.2f} | Issues: {r['issues']}\n")
            for i, (s, sc, _) in enumerate(r['recommendations'], 1):
                f.write(f"  {i}. {s['title']} - {s['artist']} ({sc:.2f})\n")
            f.write("\n")
    print("\n📄 Report → evaluation_report.txt | Log → evaluation.log")
    return results


if __name__ == "__main__":
    run_full_evaluation()
