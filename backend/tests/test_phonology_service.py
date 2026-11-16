
from app.phonology_service import (
    normalize_text,
    inspect_word,
    inspect_line,
    inspect_text,
)


def test_unicode_normalization():
    assert normalize_text("maanso") == "maanso"


def test_short_vowel_is_not_assigned_weight():
    result = inspect_word("guri")

    vowels = [
        unit for unit in result["units"]
        if unit["kind"] == "vowel_candidate"
    ]

    assert len(vowels) == 2
    assert all(unit["weight"] is None for unit in vowels)


def test_w_and_y_remain_ambiguous():
    result = inspect_word("wey")

    ambiguous = [
        unit for unit in result["units"]
        if unit["kind"] == "ambiguous_letter"
    ]

    assert len(ambiguous) == 2
    assert all(
        unit["weight"] is None
        for unit in ambiguous
    )


def test_original_line_is_preserved():
    original = "Haddii col la sheego"

    result = inspect_line(original)

    assert result["original"] == original


def test_poem_is_not_scanned():
    poem = "Haddii col la sheego\nCadaadda ku meere"

    result = inspect_text(poem)

    assert len(result["lines"]) == 2
    assert result["meter_calculated"] is False
    assert result["analysis_status"] == "PHONOLOGY_INSPECTION_ONLY"
  
