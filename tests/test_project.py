from src.project import (
    count_words,
    normalize_text,
    tokenize,
    top_n_words,
    extra_insight,
)


# ---------------------------------------------------------------------------
# normalize_text
# ---------------------------------------------------------------------------

def test_normalize_text_lowercases_text() -> None:
    assert normalize_text("Hello WORLD") == "hello world"


def test_normalize_text_removes_punctuation() -> None:
    assert normalize_text("hello, world!") == "hello world"


def test_normalize_text_splits_hyphens() -> None:
    result = normalize_text("well-known")
    assert "well" in result and "known" in result


def test_normalize_text_empty_string() -> None:
    assert normalize_text("") == ""


def test_normalize_text_collapses_extra_spaces() -> None:
    assert normalize_text("too   many    spaces") == "too many spaces"


def test_normalize_text_strips_leading_trailing_whitespace() -> None:
    assert normalize_text("  hello  ") == "hello"


def test_normalize_text_handles_newlines() -> None:
    assert "\n" not in normalize_text("line one\nline two")


def test_normalize_text_all_punctuation() -> None:
    assert normalize_text("!!!???...") == ""


def test_normalize_text_numbers_preserved() -> None:
    assert "42" in normalize_text("chapter 42")


# ---------------------------------------------------------------------------
# tokenize
# ---------------------------------------------------------------------------

def test_tokenize_splits_words() -> None:
    assert tokenize("one two three") == ["one", "two", "three"]


def test_tokenize_empty_string_returns_empty_list() -> None:
    assert tokenize("") == []


def test_tokenize_preserves_order() -> None:
    assert tokenize("the green mile") == ["the", "green", "mile"]


def test_tokenize_single_word() -> None:
    assert tokenize("python") == ["python"]


def test_tokenize_no_empty_tokens() -> None:
    assert "" not in tokenize("hello world")


# ---------------------------------------------------------------------------
# count_words
# ---------------------------------------------------------------------------

def test_count_words_counts_repeated_words() -> None:
    words = ["red", "blue", "red"]
    assert count_words(words) == {"red": 2, "blue": 1}


def test_count_words_empty_list() -> None:
    assert count_words([]) == {}


def test_count_words_all_unique() -> None:
    counts = count_words(["a", "b", "c"])
    assert all(v == 1 for v in counts.values())


def test_count_words_all_same() -> None:
    assert count_words(["go", "go", "go"]) == {"go": 3}


def test_count_words_single_word() -> None:
    assert count_words(["hello"]) == {"hello": 1}


def test_count_words_keys_match_input_words() -> None:
    words = ["cat", "dog", "cat"]
    counts = count_words(words)
    assert set(counts.keys()) == {"cat", "dog"}


# ---------------------------------------------------------------------------
# top_n_words
# ---------------------------------------------------------------------------

def test_top_n_words_returns_most_common_items() -> None:
    counts = {"apple": 3, "banana": 1, "carrot": 2}
    assert top_n_words(counts, 2) == [("apple", 3), ("carrot", 2)]


def test_top_n_words_with_non_positive_n_returns_empty_list() -> None:
    counts = {"apple": 3}
    assert top_n_words(counts, 0) == []


def test_top_n_words_negative_n_returns_empty_list() -> None:
    assert top_n_words({"apple": 3}, -1) == []


def test_top_n_words_ties_broken_alphabetically() -> None:
    counts = {"cat": 5, "ant": 5}
    result = top_n_words(counts, 2)
    assert result[0][0] == "ant"


def test_top_n_words_n_larger_than_vocab_returns_all() -> None:
    counts = {"a": 1, "b": 2}
    assert len(top_n_words(counts, 100)) == 2


def test_top_n_words_empty_counts() -> None:
    assert top_n_words({}, 5) == []


def test_top_n_words_returns_list_of_tuples() -> None:
    counts = {"the": 10, "cat": 5}
    result = top_n_words(counts, 2)
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result)


def test_top_n_words_sorted_descending() -> None:
    counts = {"a": 1, "b": 3, "c": 2}
    result = top_n_words(counts, 3)
    counts_only = [c for _, c in result]
    assert counts_only == sorted(counts_only, reverse=True)


def test_top_n_words_n_equals_one() -> None:
    counts = {"the": 10, "cat": 5}
    result = top_n_words(counts, 1)
    assert result == [("the", 10)]


# ---------------------------------------------------------------------------
# extra_insight (palindromes)
# ---------------------------------------------------------------------------

def test_extra_insight_finds_palindromes() -> None:
    words = ["level", "hello", "noon", "world"]
    counts = count_words(words)
    result = extra_insight(words, counts)
    assert "level" in result
    assert "noon" in result
    assert "hello" not in result


def test_extra_insight_ignores_single_characters() -> None:
    words = ["a", "level", "b"]
    counts = count_words(words)
    result = extra_insight(words, counts)
    assert "a" not in result
    assert "b" not in result


def test_extra_insight_empty_input() -> None:
    assert extra_insight([], {}) == []


def test_extra_insight_returns_sorted_list() -> None:
    words = ["racecar", "did", "level"]
    counts = count_words(words)
    result = extra_insight(words, counts)
    assert result == sorted(result)


def test_extra_insight_no_palindromes() -> None:
    words = ["hello", "world", "green"]
    counts = count_words(words)
    assert extra_insight(words, counts) == []


def test_extra_insight_returns_unique_words_only() -> None:
    words = ["level", "level", "level"]
    counts = count_words(words)
    result = extra_insight(words, counts)
    assert result.count("level") == 1