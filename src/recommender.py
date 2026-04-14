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


# Mood → implied valence target (borrowed from Spotify's affect model)
_MOOD_VALENCE: Dict[str, float] = {
    "happy":    0.80,
    "chill":    0.65,
    "relaxed":  0.70,
    "focused":  0.60,
    "moody":    0.50,
    "intense":  0.50,
}


def _score_song(song_energy: float, song_valence: float, song_acousticness: float,
                song_genre: str, song_mood: str,
                user: UserProfile) -> float:
    """
    Compute a composite [0, 1] score for one song against a user profile.

    Weights:
      genre match       0.25
      mood match        0.20
      energy proximity  0.25
      acoustic pref     0.15
      valence bonus     0.15
    """
    # Rule 1 — Genre match (0.25)
    genre_score = 0.25 if song_genre == user.favorite_genre else 0.0

    # Rule 2 — Mood match (0.20)
    mood_score = 0.20 if song_mood == user.favorite_mood else 0.0

    # Rule 3 — Energy proximity (0.25, linear penalty)
    energy_score = (1.0 - abs(song_energy - user.target_energy)) * 0.25

    # Rule 4 — Acoustic preference (0.15, binary threshold)
    if user.likes_acoustic and song_acousticness >= 0.6:
        acoustic_score = 0.15
    elif not user.likes_acoustic and song_acousticness < 0.4:
        acoustic_score = 0.15
    else:
        acoustic_score = 0.0

    # Rule 5 — Valence bonus (0.15, inferred target from favorite_mood)
    target_valence = _MOOD_VALENCE.get(user.favorite_mood, 0.65)
    valence_score = (1.0 - abs(song_valence - target_valence)) * 0.15

    return genre_score + mood_score + energy_score + acoustic_score + valence_score


def _build_explanation(song_genre: str, song_mood: str, song_energy: float,
                       song_acousticness: float,
                       user: UserProfile) -> str:
    parts = []

    if song_genre == user.favorite_genre:
        parts.append(f"Matched your {song_genre} preference.")

    parts.append(
        f"Energy {song_energy:.2f} is {'close to' if abs(song_energy - user.target_energy) <= 0.15 else 'near'} "
        f"your target {user.target_energy:.2f}."
    )

    if song_mood == user.favorite_mood:
        parts.append(f"Mood '{song_mood}' fits your vibe.")

    if user.likes_acoustic and song_acousticness >= 0.6:
        parts.append("High acousticness matches your acoustic preference.")
    elif not user.likes_acoustic and song_acousticness < 0.4:
        parts.append("Low acousticness matches your preference for produced sound.")

    return " ".join(parts)


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [
            (song, _score_song(
                song.energy, song.valence, song.acousticness,
                song.genre, song.mood, user
            ))
            for song in self.songs
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        return _build_explanation(
            song.genre, song.mood, song.energy, song.acousticness, user
        )


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
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
    user = UserProfile(
        favorite_genre=user_prefs.get("genre", ""),
        favorite_mood=user_prefs.get("mood", ""),
        target_energy=float(user_prefs.get("energy", 0.5)),
        likes_acoustic=bool(user_prefs.get("likes_acoustic", False)),
    )

    scored = []
    for song in songs:
        score = _score_song(
            song["energy"], song["valence"], song["acousticness"],
            song["genre"], song["mood"], user
        )
        explanation = _build_explanation(
            song["genre"], song["mood"], song["energy"], song["acousticness"], user
        )
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
