### Step 1: Explore Real Recommendation Systems

1. Research and summarize how major streaming platforms (like Spotify or YouTube) predict what users will love next. Structure your prompt to specifically ask for the difference between collaborative filtering (using other users' behavior) and content-based filtering (using song attributes).

**How Streaming Platforms Predict What You'll Love**

- **Collaborative Filtering — "People Like You Also Liked..."**
CF ignores what a song sounds like and focuses entirely on who else listened to it.

How it works:
- Every user gets a compact numerical "embedding" vector based on their listening history
- Every song also gets an embedding vector
- Recommendation = find songs whose embedding is closest to yours
- Two songs can be in completely different genres and still be "similar" if the same kinds of people listen to both

Real example — Spotify Discover Weekly:

- Trained on 600+ billion streaming events
- A skip counts as weak negative signal; a save counts as strong positive
- If you and 50,000 strangers all love Radiohead and Portishead, and those strangers also stream a lesser-known band heavily, CF surfaces that band to you — even if you've never heard of them and they sound nothing alike

**Weakness: The cold start problem — new songs/users have no data, so CF is blind to them.**

**Content-Based Filtering — "This Song Sounds Like What You Like..."**

Content-based filtering analyzes the actual attributes of a song and recommends things that are acoustically/structurally similar.

Spotify's audio features (all exposed in their public API, via The Echo Nest acquisition):

| Feature | What it measures |
|---|---|
| Tempo (BPM) | Speed |
| Energy | Intensity (0.0–1.0) |
| Valence | Happiness/positivity (0.0–1.0) |
| Danceability | Rhythm suitability |
| Acousticness | How acoustic vs. electronic |
| Speechiness | Spoken word presence |
| Instrumentalness | Vocal vs. instrumental |
| Key & Mode | Musical key, major/minor |

**How it works:** Deep audio CNNs analyze raw waveforms and position songs in feature space. Songs with similar feature vectors get recommended together.

**Weakness: Over-specialization — it only recommends "more of the same." Two songs can sound identical but have completely different cultural meaning and audiences.**

**How Platforms Actually Combine Both (Hybrid Systems)**

No major platform uses just one approach:

**Spotify's three-layer architecture:**

1. CF (matrix factorization) — primary engine, powers Discover Weekly
2. NLP / web text mining — crawls music blogs and Reddit to extract cultural descriptors per artist; helps surface niche artists with little streaming data
3. Audio features (content-based) — used mainly for cold start: a brand-new upload with zero plays can immediately be placed in embedding space based on how it sounds


**YouTube's two-stage pipeline (published in a 2016 paper):**

1. Candidate generation — a neural CF model narrows millions of videos to ~hundreds of candidates using watch history embeddings
2. Ranking — a second model scores candidates using richer content signals (video age, predicted watch time, topic relevance)
Note: YouTube famously shifted from optimizing for clicks to watch time in 2012, which fundamentally changed what their system recommended

Netflix runs multiple parallel algorithms (CF-based rows, trending, "because you watched", continue watching) and blends their outputs with a ranking model. They even A/B test which thumbnail image to show different user segments for the same title.

| Aspect | Collaborative Filtering | Content-Based Filtering |
|---|---|---|
| **Data source** | Other users' behavior | The song's own attributes |
| **Best for** | Discovery, cross-genre surprises | Cold start, explainability |
| **Main weakness** | Cold start, popularity bias | Over-specialization, filter bubbles |
| **Used by** | All major platforms (primary engine) | All major platforms (supplementary) |

2. Identify the main data types involved in these systems, such as likes, skips, playlists, tempo, or mood.

Data Types in Music Recommendation Systems

## Data Types in Music Recommendation Systems

### Content-Based Data — Song Attributes
These describe **what a song is made of**:

| Field | Type | What it represents |
|---|---|---|
| `genre` | `str` | Categorical bucket (pop, jazz, metal) |
| `mood` | `str` | Emotional label (happy, melancholic, energetic) |
| `energy` | `float` | Intensity 0.0–1.0 |
| `tempo_bpm` | `float` | Beats per minute (e.g., 120.0) |
| `valence` | `float` | Positivity/happiness 0.0–1.0 |
| `danceability` | `float` | Rhythm suitability 0.0–1.0 |
| `acousticness` | `float` | Acoustic vs. electronic 0.0–1.0 |

---

### User Preference Data — Taste Profile

**Explicit preferences** (user stated them):
- `favorite_genre: str` — direct taste declaration
- `favorite_mood: str` — declared mood preference
- `likes_acoustic: bool` — binary preference flag

**Derived/target preferences** (inferred or set):
- `target_energy: float` — what energy level the user tends to seek

---

### Behavioral / Collaborative Data

| Signal | Type | Meaning |
|---|---|---|
| **Like / save** | `bool` | Strong positive signal |
| **Skip** | `bool` / timestamp | Negative signal — didn't finish |
| **Play count** | `int` | Repeated listening = strong preference |
| **Completion rate** | `float` (0.0–1.0) | Did they hear the whole song? |
| **Playlist add** | `bool` | Strong positive, intentional curation |
| **Share** | `bool` | Very strong positive signal |
| **Session context** | `str` / `datetime` | Time of day, workout vs. studying |

---

### Key Insight

**Float features** (`energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`) are ideal for computing a **distance or similarity score**.
**String fields** (`genre`, `mood`) work as **exact-match or category-match** signals.

### Step 2: Identify Key Features

1. Examine the data/songs.csv file to see the available attributes for your simulator, such as genre, mood, energy, and tempo_bpm.

Available Features in `songs.csv`

| Feature        | Type        | Range / Values                                      |
|----------------|-------------|-----------------------------------------------------|
| `genre`        | Categorical | pop, lofi, rock, ambient, jazz, synthwave, indie pop |
| `mood`         | Categorical | happy, chill, intense, moody, focused, relaxed       |
| `energy`       | Float       | 0.28 – 0.93                                         |
| `tempo_bpm`    | Float       | 60 – 152                                            |
| `valence`      | Float       | 0.48 – 0.84                                         |
| `danceability` | Float       | 0.41 – 0.88                                         |
| `acousticness` | Float       | 0.05 – 0.92                                         |

---

**Feature Recommendations by Priority**

**Tier 1 — Most Effective (primary similarity dimensions)**

- **`energy`** — Widest spread in the dataset; cleanly separates songs by
  intensity. Compare *Spacewalk Thoughts* (0.28) vs *Gym Hero* (0.93). The
  single best numeric discriminator.
- **`valence`** — Measures emotional positivity. Distinguishes *Sunrise City*
  (0.84, sunny pop) from *Night Drive Loop* (0.49, moody synthwave). Pairs with
  energy to form a 2D mood plane.
- **`acousticness`** — Separates organic/acoustic textures (*Library Rain*: 0.86)
  from electronic/produced ones (*Gym Hero*: 0.05). Strong proxy for sonic
  texture without relying on genre labels.

**Tier 2 — Good Supporting Features**

- **`danceability`** — Useful, but partially correlated with energy. Best used as
  a tiebreaker rather than a primary axis.
- **`tempo_bpm`** — Objective and meaningful (60 BPM lofi vs. 152 BPM rock), but
  must be **normalized to [0, 1]** before computing similarity since its raw
  scale dwarfs the other features.

**Tier 3 — Use Cautiously**

- **`mood`** — High-signal categorical label, but brittle. "Chill" spans lofi,
  ambient, and jazz — very different sonic contexts. Best used as a **hard
  filter**, not a distance metric.
- **`genre`** — Too coarse for nuanced similarity. Works as an optional filter
  but should not be the primary matching axis.

**Recommended Feature Set for a Simple Recommender**

Use **cosine similarity** on a normalized vector of:

[energy, valence, acousticness, danceability, tempo_bpm_normalized]


Optionally apply `mood` as a **pre-filter** to narrow candidates before
computing similarity scores.

---

**Do Energy + Valence Actually Capture "Vibe"?**

The energy × valence pairing is borrowed from Spotify's internal model and maps
onto Russell's circumplex of affect — a well-established psychological model of
emotion. In practice, it maps onto real listening experience as follows:

| Quadrant                        | Feel              | Example in dataset         |
|---------------------------------|-------------------|----------------------------|
| Low energy + high valence       | Calm / content    | *Coffee Shop Stories* (jazz)|
| Low energy + low valence        | Melancholic / moody | *Spacewalk Thoughts* (ambient) |
| High energy + high valence      | Euphoric / hype   | *Sunrise City*, *Gym Hero* |
| High energy + low valence       | Aggressive / dark | *Storm Runner* (rock)      |

**What these features capture well:**
- The emotional intensity of a listening session
- Whether a song feels "up" or "down" emotionally
- The acoustic vs. electronic texture (via `acousticness`)

**What these features miss:**
- **Lyrical content** — two songs can share identical feature vectors but one is
  about heartbreak and the other about summer.
- **Timbre and instrumentation** — `acousticness` partially covers this but
  cannot distinguish piano from guitar or synth pad from string section.
- **Context dependency** — a focused study playlist and an evening chill playlist
  may overlap in energy/valence but feel wrong in each other's context. The
  `mood` label handles this better than numerics alone.

**Conclusion:** Energy and valence form a solid foundation for a simple
content-based recommender. Adding `acousticness` as a third axis meaningfully
improves texture matching. For this dataset, this three-feature core captures the
dominant axes of musical "vibe" without overfitting to the small sample size.


3. Determine the "Algorithm Recipe" — the set of rules the system will use to score songs.

## Algorithm Recipe

### Overview

The recommender scores every song against the user's `UserProfile` and ranks
candidates by total score descending. Each rule contributes a partial score;
the sum is normalized to [0, 1].

---

### Input Contracts

**`UserProfile` fields (from `recommender.py`)**

| Field            | Type    | Role in scoring          |
|------------------|---------|--------------------------|
| `favorite_genre` | `str`   | Hard bonus rule          |
| `favorite_mood`  | `str`   | Hard bonus rule          |
| `target_energy`  | `float` | Continuous distance rule |
| `likes_acoustic` | `bool`  | Binary bonus rule        |

**`Song` fields used for scoring**

| Field          | Type    |
|----------------|---------|
| `genre`        | `str`   |
| `mood`         | `str`   |
| `energy`       | `float` |
| `valence`      | `float` |
| `danceability` | `float` |
| `acousticness` | `float` |
| `tempo_bpm`    | `float` |

---

### Scoring Rules

#### Rule 1 — Genre Match (categorical, weight: 0.25)
if song.genre == user.favorite_genre → +0.25
else                                 → +0.00


Rationale: Genre is the coarsest filter. A user who wants pop should see pop
songs at the top, but should still receive non-pop songs with matching feel.

---

#### Rule 2 — Mood Match (categorical, weight: 0.20)
if song.mood == user.favorite_mood → +0.20
else                               → +0.00


Rationale: Mood is a high-signal label ("happy", "chill", "intense") that
directly reflects listening intent.

---

#### Rule 3 — Energy Proximity (continuous, weight: 0.25)
energy_score = 1.0 - abs(song.energy - user.target_energy)
contribution = energy_score × 0.25


Rationale: Energy has the widest spread in the dataset (0.28–0.93) and is the
strongest single axis for "vibe" matching. Penalizes proportionally to
distance, not as a hard cutoff.

---

#### Rule 4 — Acoustic Preference (binary, weight: 0.15)
if user.likes_acoustic and song.acousticness >= 0.6 → +0.15
if not user.likes_acoustic and song.acousticness < 0.4 → +0.15
else                                                    → +0.00


Rationale: `likes_acoustic` is a boolean in `UserProfile`, so it maps cleanly
to a threshold rather than a continuous distance. Threshold values (0.6 / 0.4)
create a gap that avoids penalizing ambiguous mid-range songs.

---

#### Rule 5 — Valence Bonus (continuous, weight: 0.15)
valence_score = 1.0 - abs(song.valence - derived_target_valence)
contribution = valence_score × 0.15


Where `derived_target_valence` is inferred from `favorite_mood`:
mood → valence target mapping:
"happy"    → 0.80
"chill"    → 0.65
"relaxed"  → 0.70
"focused"  → 0.60
"moody"    → 0.50
"intense"  → 0.50
default    → 0.65


Rationale: `UserProfile` has no explicit valence field, but mood strongly
implies an expected positivity level. This infers it rather than requiring a
new input field.

---

**Total Score Formula**

score = genre_score   (0.25)
+ mood_score    (0.20)
+ energy_score  (0.25)
+ acoustic_score(0.15)
+ valence_score (0.15)
─────────────────────
max possible: 1.00


---

**Ranking & Output**

1. Score all songs in the catalog using the formula above.
2. Sort descending by score.
3. Return the top-`k` songs (default `k=5`, per `main.py`).
4. For each result, return `(song_dict, score, explanation)` as expected by
   `main.py`'s unpack: `song, score, explanation = rec`.

---

### Explanation Template (`explain_recommendation`)

"Matched your {genre} preference. Energy {song.energy:.2f} is close to your
target {user.target_energy:.2f}. {mood phrase}. {acoustic phrase}."



Example output:
> "Matched your pop preference. Energy 0.82 is close to your target 0.80.
> Mood 'happy' fits your vibe. Low acousticness matches your preference for
> produced sound."

---

### Score Validation Against Test Cases

| Song                | Genre | Mood   | Energy | Acousticness | Expected rank |
|---------------------|-------|--------|--------|--------------|---------------|
| *Test Pop Track*    | pop   | happy  | 0.80   | 0.20         | **1st** ✓     |
| *Chill Lofi Loop*   | lofi  | chill  | 0.40   | 0.90         | 2nd ✓         |

For the test user (`favorite_genre="pop"`, `favorite_mood="happy"`,
`target_energy=0.8`, `likes_acoustic=False`):
- *Test Pop Track* earns genre + mood + near-perfect energy + low-acoustic
  bonus = ~0.92
- *Chill Lofi Loop* earns nothing on genre/mood/acoustic, partial energy credit
  = ~0.28

This satisfies `test_recommend_returns_songs_sorted_by_score` which asserts
`results[0].genre == "pop"` and `results[0].mood == "happy"`.