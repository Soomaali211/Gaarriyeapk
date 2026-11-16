from app.meter_engine import AnalysisModes, analyze_poem


def test_three_rule_classes_are_independent():
    modes = AnalysisModes(
        gaarriye=True,
        researchers=False,
        compatible_other=True,
    )

    assert modes.enabled_classes() == [
        "GAARRIYE_PRIMARY",
        "COMPATIBLE_OTHER_RULE",
    ]


def test_all_modes_off_is_invalid_configuration():
    result = analyze_poem(
        "Tuduc tijaabo ah",
        modes=AnalysisModes(False, False, False),
    )

    assert result.status == "INVALID_CONFIGURATION"
    assert result.analysis_performed is False
    assert result.explanation_code == "NO_ANALYSIS_CLASS_ENABLED"


def test_unknown_rules_never_generate_a_meter_verdict():
    result = analyze_poem(
        "Tuduc aan la miisaamin\nTuduc labaad",
        genre_id="jiifto",
        modes=AnalysisModes(gaarriye=True),
    )

    assert result.status == "UNVERIFIED"
    assert result.analysis_performed is False
    assert result.rules_applied == ()
    assert len(result.lines) == 2
    assert all(line.status == "UNVERIFIED" for line in result.lines)
    assert all(
        line.explanation_code == "NO_VERIFIED_EXECUTABLE_RULES"
        for line in result.lines
    )


def test_original_line_text_and_line_numbers_are_preserved():
    original = "  Tuduc koowaad  \n\nTuduc labaad"
    result = analyze_poem(original)

    assert result.lines[0].original == "  Tuduc koowaad  "
    assert result.lines[0].line_number == 1
    assert result.lines[1].original == "Tuduc labaad"
    assert result.lines[1].line_number == 3


def test_empty_text_does_not_run_analysis():
    result = analyze_poem("  \n ")

    assert result.status == "UNVERIFIED"
    assert result.analysis_performed is False
    assert result.lines == ()
    assert result.explanation_code == "EMPTY_TEXT"


def test_analysis_modes_are_returned_for_provenance():
    result = analyze_poem(
        "Tuduc",
        modes=AnalysisModes(False, True, True),
    )

    assert result.enabled_rule_classes == (
        "RESEARCHER_INTERPRETATION",
        "COMPATIBLE_OTHER_RULE",
    )
