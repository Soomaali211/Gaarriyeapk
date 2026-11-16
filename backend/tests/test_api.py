
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.research_claim_service import create_research_claim
from app.database import Base, get_db
from app.main import app
from app.rule_service import (
    create_rule,
    add_rule_evidence,
)
from app.source_service import create_source


client = TestClient(app)


def test_health():
    r = client.get("/health")

    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["analysis_engine"] == "not_ready"


def test_genres_are_not_enabled_without_verified_rules():
    data = client.get("/api/v1/genres").json()

    assert data["strict_validation_available"] is False
    assert all(
        genre["validation_enabled"] is False
        for genre in data["items"]
    )
    assert any(
        genre["id"] == "heesta_carruurta"
        for genre in data["items"]
    )


def test_guurow_is_registered_separately():
    data = client.get("/api/v1/genres").json()
    ids = [genre["id"] for genre in data["items"]]

    assert "gabay" in ids
    assert "guurow" in ids
    assert ids.count("gabay") == 1
    assert ids.count("guurow") == 1


def test_analysis_does_not_fabricate_result():
    r = client.post(
        "/api/v1/analyze",
        json={
            "text": "Tusaale maanso",
            "genre": "jiifto",
            "mode": "gaarriye_strict",
        },
    )

    assert r.status_code == 200
    assert r.json()["code"] == "ENGINE_NOT_READY"
    assert r.json()["status"] == "UNVERIFIED"
    assert r.json()["analysis_performed"] is False
    assert r.json()["enabled_rule_classes"] == ["GAARRIYE_PRIMARY"]
    assert r.json()["rules_applied"] == []


def test_unknown_genre_rejected():
    r = client.post(
        "/api/v1/analyze",
        json={
            "text": "Tusaale maanso",
            "genre": "old_html_meter",
        },
    )

    assert r.status_code == 422
    assert r.json()["code"] == "UNKNOWN_GENRE"


def test_empty_text_rejected():
    r = client.post(
        "/api/v1/analyze",
        json={"text": "   "},
    )

    assert r.status_code == 422


def test_database_health():
    r = client.get("/health/database")

    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["database"] == "connected"


def test_verified_rules_api_returns_only_verified_rules():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    def override_get_db():
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with Session(engine) as db:
            create_rule(
                db,
                code="API-UNVERIFIED-001",
                genre_id="gabay",
                title="Xeer aan la xaqiijin",
                description="Tijaabo.",
            )

            verified = create_rule(
                db,
                code="API-VERIFIED-001",
                genre_id="gabay",
                title="Xeer la xaqiijiyey",
                description="Tijaabo.",
            )

            verified.status = "VERIFIED"
            db.commit()

        response = client.get(
            "/api/v1/rules/verified",
            params={"genre_id": "gabay"},
        )

        assert response.status_code == 200

        data = response.json()

        assert data["genre_id"] == "gabay"
        assert data["status"] == "VERIFIED"
        assert data["count"] == 1
        assert data["items"][0]["code"] == "API-VERIFIED-001"

    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_rule_evidence_api_returns_evidence():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    def override_get_db():
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with Session(engine) as db:
            source = create_source(
                db,
                title="Mahadho",
                author="Gaarriye",
                source_type="primary_source",
            )

            rule = create_rule(
                db,
                code="EVIDENCE-API-001",
                genre_id="jiifto",
                title="Xeerka Jiiftada",
                description="Xeer tijaabo ah.",
            )

            add_rule_evidence(
                db,
                rule_id=rule.id,
                source_id=source.id,
                page_reference="Bogga 47",
                quotation="Xigasho Gaarriye.",
                interpretation="Fasiraad cilmiyeed.",
            )

            rule_id = rule.id
            source_id = source.id

        response = client.get(
            f"/api/v1/rules/{rule_id}/evidence"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["rule_id"] == rule_id
        assert data["rule_code"] == "EVIDENCE-API-001"
        assert data["count"] == 1

        evidence = data["items"][0]

        assert evidence["source_id"] == source_id
        assert evidence["page_reference"] == "Bogga 47"
        assert evidence["quotation"] == "Xigasho Gaarriye."
        assert evidence["interpretation"] == "Fasiraad cilmiyeed."
        assert evidence["verification_status"] == "UNVERIFIED"

    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_rule_evidence_api_returns_empty_list():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    def override_get_db():
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with Session(engine) as db:
            rule = create_rule(
                db,
                code="EVIDENCE-EMPTY-001",
                genre_id="gabay",
                title="Xeer aan caddayn lahayn",
                description="Tijaabo.",
            )

            rule_id = rule.id

        response = client.get(
            f"/api/v1/rules/{rule_id}/evidence"
        )

        assert response.status_code == 200
        assert response.json()["count"] == 0
        assert response.json()["items"] == []

    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_rule_evidence_api_returns_404_for_missing_rule():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    def override_get_db():
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.get(
            "/api/v1/rules/999/evidence"
        )

        assert response.status_code == 404

    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(engine)
        engine.dispose()
    
def test_create_research_claim_api():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    def override_get_db():
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with Session(engine) as db:
            source = create_source(
                db,
                title="Mahadho",
                author="Gaarriye",
                source_type="primary_source",
            )
            source_id = source.id

        response = client.post(
            "/api/v1/research-claims",
            json={
                "claim": "Shaqalladu waxay door ku leeyihiin miisaanka.",
                "researcher": "Cilmi-baare",
                "source_id": source_id,
                "page_reference": "Bogga 47",
            },
        )

        assert response.status_code == 201

        data = response.json()

        assert data["id"] is not None
        assert data["claim"] == (
            "Shaqalladu waxay door ku leeyihiin miisaanka."
        )
        assert data["researcher"] == "Cilmi-baare"
        assert data["source_id"] == source_id
        assert data["page_reference"] == "Bogga 47"
        assert data["status"] == "UNVERIFIED"

    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_research_claims_api_filters_by_status():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    def override_get_db():
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with Session(engine) as db:
            create_research_claim(
                db,
                claim="Sheegashada koowaad.",
            )

            verified = create_research_claim(
                db,
                claim="Sheegashada labaad.",
            )

            verified.status = "VERIFIED"
            db.commit()

        response = client.get(
            "/api/v1/research-claims",
            params={"status": "UNVERIFIED"},
        )

        assert response.status_code == 200

        data = response.json()

        assert data["count"] == 1
        assert data["items"][0]["claim"] == (
            "Sheegashada koowaad."
        )
        assert data["items"][0]["status"] == "UNVERIFIED"

    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_get_research_claim_api_and_missing_claim():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    def override_get_db():
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with Session(engine) as db:
            claim = create_research_claim(
                db,
                claim="Sheegasho cilmiyeed tijaabo ah.",
                researcher="Cilmi-baare",
            )
            claim_id = claim.id

        response = client.get(
            f"/api/v1/research-claims/{claim_id}"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == claim_id
        assert data["claim"] == (
            "Sheegasho cilmiyeed tijaabo ah."
        )
        assert data["status"] == "UNVERIFIED"

        missing_response = client.get(
            "/api/v1/research-claims/999"
        )

        assert missing_response.status_code == 404

    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_create_research_claim_api_rejects_missing_source():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    def override_get_db():
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.post(
            "/api/v1/research-claims",
            json={
                "claim": "Sheegasho tijaabo ah.",
                "source_id": 999,
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Source does not exist."

    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(engine)
        engine.dispose()
        
def test_phonology_inspect_api_preserves_original_text():
    original = "Haddii col la sheego\nCadaadda ku meere"

    response = client.post(
        "/api/v1/phonology/inspect",
        json={"text": original},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["original"] == original
    assert data["normalized"] == original
    assert data["analysis_status"] == "PHONOLOGY_INSPECTION_ONLY"
    assert data["meter_calculated"] is False


def test_phonology_inspect_api_separates_lines():
    response = client.post(
        "/api/v1/phonology/inspect",
        json={
            "text": "Haddii col la sheego\nCadaadda ku meere"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["lines"]) == 2
    assert data["lines"][0]["original"] == "Haddii col la sheego"
    assert data["lines"][1]["original"] == "Cadaadda ku meere"


def test_phonology_inspect_api_does_not_calculate_meter():
    response = client.post(
        "/api/v1/phonology/inspect",
        json={"text": "Haddii col la sheego"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["meter_calculated"] is False

    for line in data["lines"]:
        assert line["meter_calculated"] is False

        for word in line["words"]:
            assert word["meter_calculated"] is False

            for unit in word["units"]:
                assert unit["weight"] is None
                



        


def test_analysis_api_accepts_three_independent_modes():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "Sadarka koowaad\n\nSadarka labaad",
            "genre": "jiifto",
            "analysis_modes": {
                "gaarriye": True,
                "researchers": True,
                "compatible_other": False,
            },
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["enabled_rule_classes"] == [
        "GAARRIYE_PRIMARY",
        "RESEARCHER_INTERPRETATION",
    ]
    assert data["analysis_performed"] is False
    assert data["status"] == "UNVERIFIED"
    assert [line["line_number"] for line in data["lines"]] == [1, 3]
    assert all(line["status"] == "UNVERIFIED" for line in data["lines"])


def test_analysis_api_accepts_compatible_other_only():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "Tusaale maanso",
            "analysis_modes": {
                "gaarriye": False,
                "researchers": False,
                "compatible_other": True,
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["enabled_rule_classes"] == [
        "COMPATIBLE_OTHER_RULE"
    ]


def test_analysis_api_rejects_all_modes_off():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "Tusaale maanso",
            "analysis_modes": {
                "gaarriye": False,
                "researchers": False,
                "compatible_other": False,
            },
        },
    )

    assert response.status_code == 422
    assert response.json()["code"] == "NO_ANALYSIS_CLASS_ENABLED"
    assert response.json()["analysis_performed"] is False


def test_analysis_api_rejects_mixed_legacy_and_new_contracts():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "Tusaale maanso",
            "mode": "gaarriye_strict",
            "analysis_modes": {
                "gaarriye": True,
                "researchers": False,
                "compatible_other": False,
            },
        },
    )

    assert response.status_code == 422


def test_analysis_api_rejects_unknown_mode_switch():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "Tusaale maanso",
            "analysis_modes": {
                "gaarriye": True,
                "researchers": False,
                "compatible_other": False,
                "invented_class": True,
            },
        },
    )

    assert response.status_code == 422


def test_verified_rule_registry_separates_provenance_classes():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    def override_get_db():
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with Session(engine) as db:
            primary = create_rule(
                db,
                code="API-REG-PRIMARY",
                genre_id="jiifto",
                title="Xeer Gaarriye",
                description="Tijaabo.",
                rule_class="GAARRIYE_PRIMARY",
            )
            other = create_rule(
                db,
                code="API-REG-OTHER",
                genre_id="jiifto",
                title="Xeer kale",
                description="Tijaabo.",
                rule_class="COMPATIBLE_OTHER_RULE",
            )
            primary.status = "VERIFIED"
            other.status = "VERIFIED"
            primary_id = primary.id
            other_id = other.id
            db.commit()

        response = client.get(
            "/api/v1/rules/registry",
            params={"genre_id": "jiifto", "rule_class": "GAARRIYE_PRIMARY"},
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["engine_executable"] is False
        assert payload["count"] == 1
        assert payload["items"][0]["rule_class"] == "GAARRIYE_PRIMARY"
        assert payload["items"][0]["id"] == primary_id
        assert payload["items"][0]["id"] != other_id
    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(engine)
        engine.dispose()
