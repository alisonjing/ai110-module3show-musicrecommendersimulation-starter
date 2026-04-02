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
