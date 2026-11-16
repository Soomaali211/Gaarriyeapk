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


def test_note_live_required_controls_exist():
    required = {
        "poem", "editorGutter", "selectedLine", "liveLines",
        "modeGaarriye", "modeResearch", "modeCompatible",
        "saveBtn", "downloadBtn", "analyzeBtn", "clearBtn",
    }
    assert required.issubset(html_ids)


def test_api_request_does_not_send_unsupported_analysis_modes_field():
    assert "analysis_modes:modes" not in js
    assert "mode:apiMode" in js


def test_all_three_analysis_switches_are_kept():
    for switch_id in ("modeGaarriye", "modeResearch", "modeCompatible"):
        assert f'id="{switch_id}"' in html


def test_frontend_does_not_claim_meter_analysis_is_already_active():
    assert "ENGINE_NOT_READY" in js
    assert "miisaanka weli lama xisaabin" in js
