"""
Adversarial / edge-case profile runner for the Music Recommender.
Run from the project root:
    python run_adversarial.py
"""

import csv, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from recommender import load_songs, recommend_songs

SONGS = load_songs(os.path.join(os.path.dirname(__file__), "data", "songs.csv"))

ADVERSARIAL_PROFILES = {
    "1 — Conflicting: lofi genre + happy mood + HIGH energy (0.9)": {
        "genre": "lofi", "mood": "happy", "energy": 0.9
    },
    "2 — Non-existent genre: jazz (not in catalog)": {
        "genre": "jazz", "mood": "happy", "energy": 0.7
    },
    "3 — Unknown mood: melancholy (not in catalog)": {
        "genre": "pop", "mood": "melancholy", "energy": 0.5
    },
    "4 — Energy 0.5 (maximum ambiguity midpoint)": {
        "genre": "rock", "mood": "intense", "energy": 0.5
    },
    "5 — Genre dominance: rock + chill mood + LOW energy (0.2)": {
        "genre": "rock", "mood": "chill", "energy": 0.2
    },
    "6 — Boundary energy: energy = 0.0 (minimum)": {
        "genre": "pop", "mood": "happy", "energy": 0.0
    },
}


def print_results(label, recommendations):
    print(f"\n{'=' * 60}")
    print(f"  PROFILE: {label}")
    print(f"{'=' * 60}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  [{score:.2f}/4.00]  {song['title']}  —  {song['artist']}")
        print(f"        genre={song['genre']:12s}  mood={song['mood']:12s}  energy={song['energy']:.2f}")
        print(f"        Why: ", end="")
        parts = explanation.split(" | ")
        print(f"\n              • ".join([""] + parts).lstrip())
    print()


if __name__ == "__main__":
    print(f"Loaded {len(SONGS)} songs from catalog.\n")
    for label, prefs in ADVERSARIAL_PROFILES.items():
        recs = recommend_songs(prefs, SONGS, k=5)
        print_results(label, recs)
