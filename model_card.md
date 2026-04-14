# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This recommender suggests songs from a small catalog based on three things: your favorite genre, your current mood, and how energetic you want the music to feel.

It is built for classroom exploration, not real users. It does not learn from your behavior over time. It just scores every song against your stated preferences and returns the best matches.

It assumes the user knows what genre and mood they want and can express energy as a number between 0 (very calm) and 1 (very intense).

---

## 3. How the Model Works

Every song in the catalog gets a score based on how well it matches what the user asked for. The score has three parts.

First, if the song's genre matches the user's favorite genre, it gets a bonus point. Second, if the song's mood matches the user's mood, it gets another bonus point. Third, the system measures how close the song's energy level is to the user's target — a perfect match gets 2 points, and the score shrinks the further away the energy is.

The three parts are added together. The song with the highest total score ranks first.

One change was made from the original starter: the genre bonus was reduced from 2 points to 1 point, and the energy score was doubled. This was done because testing showed that genre was drowning out everything else — a wrong-vibe rock song was beating a perfect-match calm song just because it had the right genre label.

---

## 4. Data

The catalog has 18 songs. Each song has a genre, a mood, an energy level (0 to 1), and a few other features like tempo, danceability, and acousticness.

The genres covered include pop, lofi, rock, synthwave, jazz, ambient, hip-hop, classical, metal, indie pop, r&b, country, folk, edm, and blues. The moods include happy, chill, intense, moody, focused, energetic, peaceful, angry, romantic, melancholic, nostalgic, and euphoric.

No songs were added or removed from the original dataset.

The biggest gap is depth. Most genres have only one song. If you like hip-hop, there is exactly one hip-hop song and it will always be your top result no matter what. The catalog also skews toward high-energy songs — there are very few truly quiet tracks, so users who want calm music never get great energy matches.

---

## 5. Strengths

The system works well when the user's preferences are specific and well-represented in the catalog.

A high-energy pop fan gets `Gym Hero` and `Sunrise City` at the top — both feel right. A chill lofi listener gets `Library Rain` and `Focus Flow` — also a good match. When genre, mood, and energy all point in the same direction, the results feel natural.

The scoring is fully transparent. Every recommendation comes with an explanation of exactly which rules fired and how many points each one added. You always know why a song was recommended, which makes it easy to debug and improve.

---

## 6. Limitations and Bias

One significant weakness discovered during experimentation is that the genre weight dominates the scoring in a way that overrides the user's actual vibe. Because genre matching adds a fixed bonus that outweighs mood and energy combined, a user who requests "rock, chill, low energy" will receive `Storm Runner`, an intense, high-energy track ranked first, simply because it is the only rock song in the catalog. This means 14 out of 18 genres are represented by a single song, so any user whose preferred genre has only one catalog entry is guaranteed that song as their top result regardless of how poorly it fits their mood or energy target. In practice, this creates a "single-song genre trap" where specificity of taste is punished rather than rewarded: the more niche your genre preference, the less the rest of your profile matters. A fairer system would either expand the catalog to include multiple songs per genre, reduce the genre bonus so energy and mood can meaningfully compete, or introduce a genre-proximity concept where adjacent genres (such as folk and country, or pop and indie pop) share partial credit.

The system also has no way to catch typos or near-matches in mood. If you type "melancholy" instead of "melancholic," your mood preference is silently ignored with no warning. The system just keeps going as if you never said anything about mood.

Finally, features like valence, danceability, acousticness, and tempo are available in the data but never used in scoring. A user who wants acoustic guitar music gets the same results as someone who wants electronic music at the same energy level — the system cannot tell them apart.

---

## 7. Evaluation

To evaluate the recommender, six adversarial user profiles were designed specifically to expose weaknesses in the scoring logic, each targeting a different potential failure mode. These included a conflicting profile (lofi genre with happy mood and high energy 0.9), a non-existent genre (jazz, which happened to exist as a single song), an unknown mood string (melancholy, which matched nothing in the catalog), an ambiguous midpoint energy (0.5), a contradictory genre-vibe pairing (rock with chill mood and low energy 0.2), and a boundary energy value (0.0). For each profile, the top 5 results were printed to the terminal and compared against what a human listener would intuitively expect.

The most surprising finding was that the system confidently returned `Storm Runner` (rock, intense, energy 0.91) as the top result for a user who explicitly requested chill, low-energy music — simply because genre matched. Equally unexpected was that an unknown mood string such as "melancholy" produced no error and no warning; the mood signal silently zeroed out and the system continued recommending as if mood had never been specified. A weight sensitivity test was also run by halving the genre bonus from 2.0 to 1.0 and doubling the energy weight, which corrected three of the four broken profiles. A feature removal test followed, temporarily disabling the mood check entirely, which revealed that mood was doing meaningful work for atmospheric profiles like Late-Night Synthwave but was already effectively disabled for profiles using mood labels absent from the catalog.

---

## 8. Future Work

The most important improvement would be expanding the catalog. Most genres only have one song, which makes diverse recommendations impossible. Adding five to ten songs per genre would immediately make the results feel more useful.

After that, validating mood input would help. If a user types a mood that does not exist in the catalog, the system should say so instead of silently skipping it.

It would also be worth using the extra features already in the data. Acousticness could help separate organic and electronic songs. Valence could replace mood matching with something more continuous and harder to mistype.

A diversity rule would also help. Right now the same five songs always appear for the same profile. Shuffling in occasional surprises or making sure the same artist does not appear twice would make the system feel less repetitive.

---

## 9. Personal Reflection

### Biggest Learning Moment

The biggest learning moment was the Storm Runner result. A user asked for quiet, chill, low-energy rock. The system returned an intense, high-energy track as the #1 recommendation. The code had no bug. Every number was calculated correctly. The problem was that one weight was too large — genre was worth so much that it could win an argument against both mood and energy combined.

That moment made the whole project click. A recommender is not just an algorithm. It is a set of decisions about what matters most. Those decisions are baked into the weights, and if the weights are off, the system will confidently give wrong answers with no warning. The math will be right, but the result will still be wrong.

### How AI Tools Helped — and When to Double-Check

AI tools were genuinely useful for two things: generating adversarial test profiles and explaining what the scoring math was doing step by step. Instead of manually working through six edge cases, the profiles were produced quickly and covered failure modes that might not have been obvious otherwise — like what happens at exactly energy 0.5, or when a mood string has a one-letter typo.

The moment to double-check was when an explanation sounded confident but had not been verified against actual output. For example, one explanation described how the weight shift would fix all broken profiles. Running the code showed it fixed three out of four — not all of them. The explanation was directionally right but not precise. AI tools are good at pattern reasoning but need the terminal output to catch the cases where the pattern breaks.

### What Was Surprising About Simple Algorithms

The most surprising thing was how much the results could feel like real recommendations even when the logic was just three additions. When the weights were balanced, `Library Rain` showing up for a chill lofi listener felt completely natural, like the app understood the vibe. It did not. It just added three numbers and picked the biggest one.

That is the illusion. A list of five songs ranked by a score looks like taste. It feels personalized. But the system has no concept of what music sounds like, no sense of atmosphere, no understanding of why someone might want something quiet at midnight versus something loud at the gym. It is arithmetic wearing the costume of a recommendation.

### What Would Come Next

The first thing to try would be adding more songs per genre — at least five per category. Most of the failures in this project were not logic failures, they were catalog failures. You cannot recommend good rock variety when there is only one rock song.

After that, validating mood input before scoring would prevent the silent zero-out problem. If the user types a mood that does not exist, the system should tell them and suggest the closest match from the catalog.

The most interesting extension would be using acousticness and valence as scoring signals. Acousticness could separate a user who wants unplugged folk guitar from one who wants electronic ambient, even if both have the same energy target. Valence — how emotionally positive a song feels — could replace the brittle mood string match with something continuous and harder to accidentally break with a typo.

Finally, it would be worth adding a diversity rule that prevents the same artist from appearing twice in the top five. Right now a user can get `Midnight Coding` and `Focus Flow` back to back — both by LoRoom — which makes the list feel thin. Variety in the output matters as much as accuracy in the scores.
