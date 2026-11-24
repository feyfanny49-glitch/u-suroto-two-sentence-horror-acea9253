# Strategy — Two-Sentence Horror (u-suroto-two-sentence-horror-acea9253)

## Exact deliverable

A judged TEXT entry. The program at the repository root (`main.py`, python3.13) must
write precisely one artifact: `/output/entry.txt`. That file is the entry. Nothing
else is judged. The program is run in a sandbox with no network; everything it needs
is in this repository. An entry is valid only with transcripts, but this document and
the code are the whole judged artifact.

**Chosen entry (107 bytes, exactly two sentences, no trailing newline):**

    The school called to say my son had been picked up by his father. I've never told them he doesn't have one.

## Hard caps (gate)

- `/output/entry.txt` must be UTF-8 text of **1 to 400 characters**, not only whitespace.
- Fail the gate => Valid 0, never judged, no prize.
- Only 1st place pays ($2). Top place only; near-misses pay nothing.
- Room: 1 CPU, 512 MiB, 64 pids, 60 s wall per run.
- At most 5 submissions per entrant per UTC day; final = last receipt before deadline
  unless an earlier one is explicitly picked.
- Two-sentence requirement is a judge criterion, so the text has exactly two
  sentence-ending periods and no other sentence terminators.

## Scoring / judge criteria, IN ORDER

The house judge (glm-5.3-flash on OpenRouter, "superbot" persona, reasoning effort
high) sees two entries at a time in both label orders and must pick one, margin 1-5.
A call gives the winner 0.5 + margin/10; a game is the mean of the two calls; a win
needs more than half. 3 Swiss rounds + a playoff among the top 3; final ranking is a
Bradley-Terry win rate over final-heat games. The brief says to go through the
criteria in order and let the FIRST difference decide unless a later one differs by
much more. Therefore I optimize lexicographically, not by averaging:

1. A horror story in **exactly two sentences** and **genuinely frightening**.
   Baseline: being a horror story in two sentences beats not being one.
2. The **second sentence turns or reveals** something that makes the first sentence
   worse on a second read.
3. The horror is **implied**, not explained — leave the reader to fill in the worst.
4. Prose is **precise and concrete**, every word earning its place in two sentences.
5. **Original** — not a familiar twist or a known story retold.

Restraint matters more than shock; gore does not count. Text addressed to the judge
is allowed but is not needed here.

## Rival reconnaissance

The live feed is in blind-round mode (API reports `judged: 0`, `entries: []`), so no
competitor text is public. Web research on the genre shows the exhausted staples a
jaded judge has read a thousand times: mirror/reflection discrepancies, "I live
alone" with a photo or footsteps, dead relatives in closets, "who is this" texts,
bodies in fridges, dolls, Bloody Mary name-chanting, and clock/time-loop reveals.
The entry must not resemble any of them.

## Concrete plan to maximize the score (lexicographic)

1. **C1 — frightening, two sentences.** Use a primal stakes (a child taken) told in
   flat, ordinary language. No gore, no monsters named, no shouting.
2. **C2 — the turn.** Sentence 1 is a normal administrative call: "picked up by his
   father." Sentence 2 reveals the father does not exist, so on a second read sentence
   1 becomes the disappearance itself. The word "never" adds a second, quieter turn:
   the narrator's silence is its own wrongness.
3. **C3 — implied.** Never say who took him, never say "kidnapped", "dead", or
   "ghost". The reader supplies the worst.
4. **C4 — precision.** 107 bytes, ordinary concrete nouns (school, son, father), one
   clause in each sentence, no adjectives, no adverbs, no wasted connective.
5. **C5 — originality.** The "school calls about a parent who cannot exist" premise
   is not one of the stock two-sentence shocks; it is new to this genre's canon.
6. **Engineering.** `main.py` stores the story as a single source of truth, validates
   UTF-8 / length / non-whitespace / sentence count locally, and writes `/output/entry.txt`
   atomically via a temp file in the same directory plus `os.replace`, with no trailing
   newline. The same entrypoint is written twice: a first working version, then a
   revised version that adds durability (fsync) and a byte-for-byte read-back check;
   both writes are visible in the transcript.
7. **Verification.** Run the entrypoint, confirm the exact bytes, UTF-8 decoding,
   character count <= 400, absence of a trailing newline, and a clean git commit
   preserving the makefun freshness and LICENSE commits.
