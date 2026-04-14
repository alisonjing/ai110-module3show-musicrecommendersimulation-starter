"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs

## User Profiles
## Define at least three distinct user preference dictionaries (e.g., "High-Energy Pop," "Chill Lofi," "Deep Intense Rock").
PROFILES = {
    "High-Energy Pop":    {"genre": "pop",    "mood": "happy",      "energy": 0.9},
    "Chill Lofi":         {"genre": "lofi",   "mood": "chill",      "energy": 0.3},
    "Deep Intense Rock":  {"genre": "rock",   "mood": "intense",    "energy": 0.85},
    "Late-Night Synthwave": {"genre": "synthwave", "mood": "moody", "energy": 0.6},
}


def print_recommendations(label: str, recommendations: list) -> None:
    """Print a formatted recommendations block for one user profile."""
    print(f"\n{'=' * 40}")
    print(f"  Profile: {label}")
    print(f"{'=' * 40}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"      Score : {score:.2f} / 4.00")
        print(f"      Why   :")
        for reason in explanation.split(" | "):
            print(f"              • {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs\n")

    for label, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(label, recommendations)


if __name__ == "__main__":
    main()
