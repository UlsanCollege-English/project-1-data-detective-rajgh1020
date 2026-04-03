[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/cDnlIYNC)
# P1: Data Detective

## Summary
This project loads a text file from The Green Mile by Stephen King, cleans it up, breaks it into words, and counts how often each word shows up. It then prints the top N most frequent words and lists any words that only appear once.

## Dataset
- File: `data/sample.txt`
- Why I chose it: I watched the movie a while back and really liked it, so when I needed a dataset I figured it would be interesting to look at the source material. I haven't read the book yet but seeing which words King actually leans on most felt like a good reason to start with it.

## How to run
```bash
pytest -q
python -m src.project
```

## Approach
- Load text from a file
- Normalize the text (lowercase, split hyphens, remove punctuation, collapse whitespace)
- Tokenize into words
- Count word frequencies
- Show the top N words
- Report one extra insight (words that appear exactly once)

## Complexity

### `count_words`
- Time: O(n)
- Space: O(u) where u = unique words
- Why: Single pass through n words with O(1) average-case dictionary operations, so the overall complexity stays linear. The dictionary grows to at most u entries where u ≤ n, one per unique token.

### `top_n_words`
- Time: O(u log u)
- Space: O(u)
- Why: Python's Timsort on u items is O(u log u) worst case and dominates everything else. The subsequent slice to n items is O(n) which is always bounded by O(u log u), so it doesn't affect the overall complexity.

## Edge-case checklist
- [x] empty file — tokenize gives back an empty list and everything downstream just returns empty too
- [x] punctuation-heavy input — normalize_text uses str.translate to strip out all punctuation before anything else runs
- [x] repeated words — count_words keeps adding to the same key so repeated words get counted correctly
- [x] uppercase/lowercase differences — normalize_text lowercases the whole text first so Hello and hello are treated as the same word
- [x] `n <= 0` — top_n_words checks for this right away and returns an empty list

## Assistance & sources
- AI used? Y
- What it helped with: Looked up how str.maketrans works and asked about pytest structure when my tests werent running right
- Other sources: The Green Mile by Stephen King (short excerpt, used for class)

## Design note
I chose The Green Mile because I watched the movie a while back and really enjoyed it. I haven't actually read the book yet, so using it as a dataset felt like a good excuse to get familiar with Kings prose. His writing tends to mix plain conversational language with very deliberate word choices, which I figured would produce an interesting frequency distribution.

The trickiest decision was handling hyphens in normalize_text. Deleting them silently turns words like half-remembered into halfremembered, which is a non-word that pollutes the vocabulary with noise. Replacing hyphens with spaces splits them into valid tokens and keeps the word counts accurate.

I used a plain dictionary with dict.get() for count_words rather than collections.Counter. Counter would have worked fine but writing the loop manually kept the O(n) logic explicit and easier to reason about during testing.

Choosing the extra insight took some thought. I went with hapax legomena — words that appear exactly once — because it felt more analytically meaningful than something like average word length. In a narrative text, once-only words tend to be the most expressive and contextually specific ones, which makes them worth surfacing.

The hardest part was writing edge case tests that actually verified behavior rather than just mirroring the implementation. One thing I would add next is argparse support so the tool can be pointed at any file from the command line without modifying the source.