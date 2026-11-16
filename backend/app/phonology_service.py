
"""Conservative Somali orthographic inspection.

This module preserves the original text and identifies orthographic
units without assigning unverified metrical weights.
"""

import unicodedata
from typing import Any


VOWELS = frozenset("aeiou")
AMBIGUOUS_LETTERS = frozenset("wy")


def normalize_text(text: str) -> str:
    """Normalize Unicode without changing the original stored text."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    return unicodedata.normalize("NFC", text)


def inspect_word(word: str) -> dict[str, Any]:
    """Inspect one word without making unsupported pronunciation claims."""
    normalized = normalize_text(word).lower()
    units = []
    index = 0

    while index < len(normalized):
        char = normalized[index]

        if char.isspace():
            index += 1
            continue

        if char in VOWELS:
            end = index + 1

            while end < len(normalized) and normalized[end] == char:
                end += 1

            group = normalized[index:end]

            units.append({
                "text": group,
                "kind": (
                    "repeated_vowel_candidate"
                    if len(group) > 1
                    else "vowel_candidate"
                ),
                "weight": None,
                "status": "REQUIRES_SOURCE_VERIFICATION",
            })

            index = end
            continue

        if char in AMBIGUOUS_LETTERS:
            units.append({
                "text": char,
                "kind": "ambiguous_letter",
                "possible_roles": ["vowel", "consonant"],
                "weight": None,
                "status": "REQUIRES_PRONUNCIATION_REVIEW",
            })

            index += 1
            continue

        units.append({
            "text": char,
            "kind": "consonant_candidate",
            "weight": None,
            "status": "NOT_METRICALLY_CLASSIFIED",
        })

        index += 1

    return {
        "original": word,
        "normalized": normalized,
        "units": units,
        "meter_calculated": False,
    }


def inspect_line(line: str) -> dict[str, Any]:
    """Inspect words in a line while preserving the original line."""
    normalized = normalize_text(line)

    words = [
        inspect_word(word)
        for word in normalized.split()
        if word
    ]

    return {
        "original": line,
        "normalized": normalized,
        "words": words,
        "meter_calculated": False,
    }


def inspect_text(text: str) -> dict[str, Any]:
    """Inspect a poem without producing a meter verdict."""
    normalized = normalize_text(text)

    lines = [
        inspect_line(line)
        for line in normalized.splitlines()
    ]

    return {
        "original": text,
        "normalized": normalized,
        "lines": lines,
        "analysis_status": "PHONOLOGY_INSPECTION_ONLY",
        "meter_calculated": False,
  }
  
