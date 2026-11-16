from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
js = (ROOT / "app.js").read_text(encoding="utf-8")
html_ids = set(re.findall(r'id=["\']([^"\']+)', html))
js_refs = set(re.findall(r'\$\(["\']#([^"\']+)', js))
missing = sorted(js_refs - html_ids)


def test_all_direct_js_id_references_exist_in_html():
    assert not missing, f"Missing HTML IDs referenced by app.js: {missing}"


def test_three_switches_map_to_backend_contract_without_merging():
    assert 'apiKey:"gaarriye"' in js
    assert 'apiKey:"researchers"' in js
    assert 'apiKey:"compatible_other"' in js
    assert 'analysis_modes:analysisModes' in js
    assert 'researchers:modes.research' in js
    assert 'compatible_other:modes.compatible' in js


def test_frontend_no_longer_sends_legacy_single_mode():
    assert 'mode:apiMode' not in js
    assert 'analysis_modes:analysisModes' in js


def test_note_live_displays_backend_line_status():
    assert 'lastAnalysis?.lines?.find' in js
    assert 'resultLine.status' in js
    assert 'resultLine.explanation_code' in js


def test_switch_change_reanalyzes_existing_text():
    assert 'if(poem.value.trim() && API_BASE) analyzePoem({quiet:true})' in js


def test_text_edit_invalidates_stale_analysis_response():
    assert 'requestSequence++' in js
    assert 'if(seq!==requestSequence)return' in js


def test_existing_note_live_controls_remain_present():
    required = {
        "poem", "editorGutter", "selectedLine", "liveLines",
        "modeGaarriye", "modeResearch", "modeCompatible",
        "saveBtn", "downloadBtn", "analyzeBtn", "clearBtn",
    }
    assert required.issubset(html_ids)


def test_frontend_does_not_claim_meter_analysis_is_already_active():
    assert "UNVERIFIED" in js
    assert "Qoraalka lama miisaamin" in js
