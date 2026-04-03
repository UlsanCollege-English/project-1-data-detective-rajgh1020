"""Project 1 starter: Data Detective.
Implement the required functions below.
Use standard library only.
"""
from __future__ import annotations
import string
from pathlib import Path


def load_text(path: str) -> str:
    """Load and return the full text from a UTF-8 file."""
    with open(path, encoding="utf-8") as f:
        return f.read()


def normalize_text(text: str) -> str:
    """Lowercase, remove punctuation, and collapse whitespace."""
    text = text.lower()

    # Split hyphens into spaces so "well-known" -> "well known"
    text = text.replace("-", " ").replace("—", " ").replace("–", " ")

    # Remove all punctuation
    remove_punct = str.maketrans("", "", string.punctuation)
    text = text.translate(remove_punct)

    # Collapse tabs, newlines, and extra spaces into one space
    text = " ".join(text.split())

    return text


def tokenize(text: str) -> list[str]:
    """Split normalized text into a list of words."""
    if not text:
        return []
    return text.split()


def count_words(words: list[str]) -> dict[str, int]:
    """Count how many times each word appears.

    Time: O(n) | Space: O(u) where u = unique words.
    """
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_n_words(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    """Return the top N (word, count) tuples, sorted by count desc then alphabetically.

    Time: O(u log u) | Space: O(u).
    """
    if n <= 0:
        return []

    # (-count, word) sorts highest count first; ties go alphabetically
    sorted_words = sorted(counts.items(), key=lambda item: (-item[1], item[0]))

    return sorted_words[:n]


def extra_insight(words: list[str], counts: dict[str, int]) -> object:
    """Return a sorted list of unique palindrome words found in the text.

    Time: O(u * k) where k = average word length | Space: O(u)."""
 
    palindromes = sorted(
        word for word in counts
        if len(word) > 1 and word == word[::-1]
    )
    return palindromes


def run_demo(path: str, n: int = 10) -> dict[str, object]:
    """Run the full analysis pipeline and return summary data."""
    text = load_text(path)
    normalized = normalize_text(text)
    words = tokenize(normalized)
    counts = count_words(words)
    return {
        "total_words": len(words),
        "unique_words": len(counts),
        "top_words": top_n_words(counts, n),
        "extra_insight": extra_insight(words, counts),
    }


if __name__ == "__main__":
    demo_path = Path("data/data.txt")
    if demo_path.exists():
        results = run_demo(str(demo_path), n=10)
        for key, value in results.items():
            print(f"{key}: {value}")
    else:
        print("No demo file found at data/sample.txt")
