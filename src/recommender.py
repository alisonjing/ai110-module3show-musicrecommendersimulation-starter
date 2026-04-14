import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score one song against user preferences and explain every point awarded.

    Algorithm Recipe
    ────────────────
    Rule 1 — Genre match  : +2.0  if song["genre"] == user_prefs["genre"]
    Rule 2 — Mood match   : +1.0  if song["mood"]  == user_prefs["mood"]
    Rule 3 — Energy score : 1.0 - abs(song["energy"] - user_prefs["energy"])
                            (0.0 → completely opposite, 1.0 → perfect match)
    Max possible          : 4.0

    Returns
    ───────
    score   : float         — total raw points
    reasons : List[str]     — one entry per rule that contributed points,
                              so the caller can show the user exactly why
                              each song was recommended
    """
    reasons: List[str] = []

    # Rule 1 — Genre match (+2.0)
    if song["genre"] == user_prefs["genre"]:
        genre_score = 2.0
        reasons.append(f"genre match (+{genre_score})")
    else:
        genre_score = 0.0

    # Rule 2 — Mood match (+1.0)
    if song["mood"] == user_prefs["mood"]:
        mood_score = 1.0
        reasons.append(f"mood match (+{mood_score})")
    else:
        mood_score = 0.0

    # Rule 3 — Energy similarity (continuous, 0.0–1.0)
    energy_score = 1.0 - abs(song["energy"] - user_prefs["energy"])
    reasons.append(
        f"energy score {energy_score:.2f} "
        f"(target {user_prefs['energy']:.2f}, song {song['energy']:.2f})"
    )

    score = genre_score + mood_score + energy_score
    return score, reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = {
            "genre":  user.favorite_genre,
            "mood":   user.favorite_mood,
            "energy": user.target_energy,
        }
        scored = []
        for song in self.songs:
            song_dict = {
                "genre":  song.genre,
                "mood":   song.mood,
                "energy": song.energy,
            }
            score, _ = score_song(user_prefs, song_dict)
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre":  user.favorite_genre,
            "mood":   user.favorite_mood,
            "energy": user.target_energy,
        }
        song_dict = {
            "genre":  song.genre,
            "mood":   song.mood,
            "energy": song.energy,
        }
        _, reasons = score_song(user_prefs, song_dict)
        return " | ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """
    Read data/songs.csv with Python's csv module and return a list of dicts.

    csv.DictReader reads every cell as a plain string.  The conversions below
    turn each numeric column into the right Python type so math works later:

      id            → int    (song identifier, used for lookups)
      energy        → float  (0.0–1.0, used in energy_score formula)
      tempo_bpm     → float  (60–152 BPM, available for normalization)
      valence       → float  (0.0–1.0, emotional positivity)
      danceability  → float  (0.0–1.0, rhythm suitability)
      acousticness  → float  (0.0–1.0, organic vs. electronic texture)

    String columns (title, artist, genre, mood) are left as-is.
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"]           = int(row["id"])
            row["energy"]       = float(row["energy"])
            row["tempo_bpm"]    = float(row["tempo_bpm"])
            row["valence"]      = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    user_prefs keys used: genre, mood, energy, likes_acoustic (optional, default False)
    Returns: list of (song_dict, score, explanation) sorted descending by score.
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
