
import os
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.meter_engine import AnalysisModes, analyze_poem
from app.phonology_service import inspect_text
from app.models import Rule
from app.rule_service import (
    get_verified_rules,
    get_verified_rule_registry,
    get_rule_evidence,
)
from app.source_service import (
    create_source,
    get_source,
    list_sources,
)
from app.research_claim_service import (
    create_research_claim,
    get_research_claim,
    list_research_claims,
)


app = FastAPI(
    title="Gaarriye Meter API",
    version="0.1.0",
    description=(
        "API aasaasi ah; engine-ka miisaanka waxa la "
        "hawlgelinayaa kaddib xaqiijinta xeerarka asalka ah."
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://gaarriye-metre-analyzer.onrender.com",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "null",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Accept"],
)

GENRES = [
    {"id": "jiifto", "name": "Jiifto", "validation_enabled": False},
    {"id": "gabay", "name": "Gabay", "validation_enabled": False},
    {"id": "guurow", "name": "Guurow", "validation_enabled": False},
    {"id": "geeraar", "name": "Geeraar", "validation_enabled": False},
    {
        "id": "heesta_kabadaha",
        "name": "Heesta Kabadaha",
        "validation_enabled": False,
    },
    {
        "id": "heesta_xerta",
        "name": "Heesta Xerta",
        "validation_enabled": False,
    },
    {
        "id": "baarcaddaha_saarka",
        "name": "Baarcaddaha / Saarka",
        "validation_enabled": False,
    },
    {
        "id": "heesta_carruurta",
        "name": "Heesta Carruurta",
        "validation_enabled": False,
    },
    {
        "id": "herimaahee_hanna_haybsan",
        "name": "Herimaahee Hanna Haybsan",
        "validation_enabled": False,
    },
]


class AnalysisModesRequest(BaseModel):
    """Three independent switches; no category is silently merged."""

    model_config = ConfigDict(extra="forbid")

    gaarriye: bool = True
    researchers: bool = False
    compatible_other: bool = False

    def to_engine_modes(self) -> AnalysisModes:
        return AnalysisModes(
            gaarriye=self.gaarriye,
            researchers=self.researchers,
            compatible_other=self.compatible_other,
        )


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    text: str = Field(min_length=1, max_length=12000)
    genre: str | None = Field(default=None, max_length=64)
    # Legacy single-mode field remains supported for older frontend builds.
    mode: Literal[
        "gaarriye_strict",
        "research_comparison",
    ] | None = None
    # New contract used by the three independent Note Live switches.
    analysis_modes: AnalysisModesRequest | None = None

    @model_validator(mode="after")
    def validate_mode_contract(self):
        if self.mode is not None and self.analysis_modes is not None:
            raise ValueError(
                "Use either legacy 'mode' or 'analysis_modes', not both."
            )
        return self

    def selected_modes(self) -> AnalysisModes:
        if self.analysis_modes is not None:
            return self.analysis_modes.to_engine_modes()
        if self.mode == "research_comparison":
            return AnalysisModes(
                gaarriye=False,
                researchers=True,
                compatible_other=False,
            )
        # Preserve the historical default and gaarriye_strict behavior.
        return AnalysisModes()

class PhonologyInspectRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    text: str = Field(min_length=1, max_length=12000)
class SourceCreateRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    title: str = Field(min_length=1, max_length=500)
    author: str | None = Field(default=None, max_length=255)
    publication_year: int | None = Field(
        default=None,
        ge=0,
        le=2100,
    )
    source_type: str = Field(min_length=1, max_length=100)
    locator: str | None = Field(default=None, max_length=255)
    notes: str | None = None


class ResearchClaimCreateRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    claim: str = Field(min_length=1)
    researcher: str | None = Field(
        default=None,
        max_length=255,
    )
    source_id: int | None = Field(default=None, gt=0)
    page_reference: str | None = Field(
        default=None,
        max_length=100,
    )


# ------------------------------------------
# Health endpoints
# ------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "api_version": "0.1.0",
        "analysis_engine": "not_ready",
    }


@app.get("/health/database")
def database_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }


# ------------------------------------------
# Genre endpoints
# ------------------------------------------

@app.get("/api/v1/genres")
def genres():
    return {
        "items": GENRES,
        "strict_validation_available": False,
    }


# ------------------------------------------
# Poetry analysis endpoint
# ------------------------------------------

@app.post("/api/v1/analyze")
def analyze(payload: AnalyzeRequest):
    if not payload.text.strip():
        return JSONResponse(
            status_code=422,
            content={
                "code": "EMPTY_TEXT",
                "message": "Qoraal maanso ah ayaa loo baahan yahay.",
            },
        )

    if payload.genre and payload.genre not in {
        genre["id"] for genre in GENRES
    }:
        return JSONResponse(
            status_code=422,
            content={
                "code": "UNKNOWN_GENRE",
                "message": "Nooca maansada lama aqoonsan.",
            },
        )

    result = analyze_poem(
        payload.text,
        genre_id=payload.genre,
        modes=payload.selected_modes(),
    )

    if result.status == "INVALID_CONFIGURATION":
        return JSONResponse(
            status_code=422,
            content={
                "code": "NO_ANALYSIS_CLASS_ENABLED",
                "status": result.status,
                "message": (
                    "Fadlan daar ugu yaraan hal hab-falanqayn: "
                    "Gaarriye, Cilmi-baadhisaha, ama Xeerarka kale "
                    "ee waafaqsan."
                ),
                **result.to_dict(),
            },
        )

    return {
        "code": "ENGINE_NOT_READY",
        "message": (
            "Doorashooyinka falanqaynta waa la helay, khadadkana "
            "waa la kala aqoonsaday; hase yeeshee xeerar miisaan "
            "oo la xaqiijiyey oo engine-ku fulin karo weli lama "
            "xirin. Sidaas darteed qoraalka lama miisaamin, mana "
            "jirto natiijo xukun ah."
        ),
        **result.to_dict(),
    }

# ------------------------------------------
# Phonology inspection endpoint
# ------------------------------------------

@app.post("/api/v1/phonology/inspect")
def phonology_inspect(
    payload: PhonologyInspectRequest,
):
    return inspect_text(payload.text)
# ------------------------------------------
# Verified Rule Registry endpoint
# ------------------------------------------

@app.get("/api/v1/rules/verified")
def verified_rules(
    genre_id: str = Query(min_length=1, max_length=100),
    db: Session = Depends(get_db),
):
    rules = get_verified_rules(
        db,
        genre_id=genre_id,
    )

    return {
        "genre_id": genre_id,
        "status": "VERIFIED",
        "count": len(rules),
        "items": [
            {
                "id": rule.id,
                "code": rule.code,
                "genre_id": rule.genre_id,
                "title": rule.title,
                "description": rule.description,
                "status": rule.status,
                "rule_class": rule.rule_class,
            }
            for rule in rules
        ],
    }


@app.get("/api/v1/rules/registry")
def verified_rule_registry(
    genre_id: str | None = Query(default=None, min_length=1, max_length=100),
    rule_class: Literal[
        "GAARRIYE_PRIMARY",
        "RESEARCHER_INTERPRETATION",
        "COMPATIBLE_OTHER_RULE",
    ] | None = None,
    db: Session = Depends(get_db),
):
    """Return reviewed, explicitly classified rules; never implies executability."""
    rules = get_verified_rule_registry(
        db, genre_id=genre_id, rule_class=rule_class
    )
    return {
        "status": "VERIFIED_METADATA_ONLY",
        "engine_executable": False,
        "count": len(rules),
        "items": [
            {
                "id": rule.id,
                "code": rule.code,
                "genre_id": rule.genre_id,
                "rule_class": rule.rule_class,
                "title": rule.title,
                "description": rule.description,
                "status": rule.status,
            }
            for rule in rules
        ],
    }


# ------------------------------------------
# Rule Evidence endpoint
# ------------------------------------------

@app.get("/api/v1/rules/{rule_id}/evidence")
def rule_evidence_endpoint(
    rule_id: int,
    db: Session = Depends(get_db),
):
    rule = db.get(Rule, rule_id)

    if rule is None:
        raise HTTPException(
            status_code=404,
            detail="Rule not found.",
        )

    evidence_items = get_rule_evidence(
        db,
        rule_id=rule_id,
    )

    return {
        "rule_id": rule_id,
        "rule_code": rule.code,
        "count": len(evidence_items),
        "items": [
            {
                "id": evidence.id,
                "rule_id": evidence.rule_id,
                "source_id": evidence.source_id,
                "page_reference": evidence.page_reference,
                "quotation": evidence.quotation,
                "interpretation": evidence.interpretation,
                "verification_status": evidence.verification_status,
            }
            for evidence in evidence_items
        ],
    }


# ------------------------------------------
# Research Claims endpoints
# ------------------------------------------

@app.post("/api/v1/research-claims", status_code=201)
def create_research_claim_endpoint(
    payload: ResearchClaimCreateRequest,
    db: Session = Depends(get_db),
):
    try:
        claim = create_research_claim(
            db,
            claim=payload.claim,
            researcher=payload.researcher,
            source_id=payload.source_id,
            page_reference=payload.page_reference,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return {
        "id": claim.id,
        "claim": claim.claim,
        "researcher": claim.researcher,
        "source_id": claim.source_id,
        "page_reference": claim.page_reference,
        "status": claim.status,
    }


@app.get("/api/v1/research-claims")
def get_research_claims_endpoint(
    source_id: int | None = Query(default=None, gt=0),
    status: str | None = Query(default=None, min_length=1, max_length=30),
    db: Session = Depends(get_db),
):
    claims = list_research_claims(
        db,
        source_id=source_id,
        status=status,
    )

    return {
        "count": len(claims),
        "items": [
            {
                "id": claim.id,
                "claim": claim.claim,
                "researcher": claim.researcher,
                "source_id": claim.source_id,
                "page_reference": claim.page_reference,
                "status": claim.status,
            }
            for claim in claims
        ],
    }


@app.get("/api/v1/research-claims/{claim_id}")
def get_research_claim_endpoint(
    claim_id: int,
    db: Session = Depends(get_db),
):
    claim = get_research_claim(
        db,
        claim_id=claim_id,
    )

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Research claim not found.",
        )

    return {
        "id": claim.id,
        "claim": claim.claim,
        "researcher": claim.researcher,
        "source_id": claim.source_id,
        "page_reference": claim.page_reference,
        "status": claim.status,
    }


# ------------------------------------------
# Source Repository endpoints
# ------------------------------------------

@app.post("/api/v1/sources", status_code=201)
def create_source_endpoint(
    payload: SourceCreateRequest,
    db: Session = Depends(get_db),
):
    source = create_source(
        db,
        title=payload.title,
        author=payload.author,
        publication_year=payload.publication_year,
        source_type=payload.source_type,
        locator=payload.locator,
        notes=payload.notes,
    )

    return {
        "id": source.id,
        "title": source.title,
        "author": source.author,
        "publication_year": source.publication_year,
        "source_type": source.source_type,
        "locator": source.locator,
        "notes": source.notes,
    }


@app.get("/api/v1/sources")
def get_sources_endpoint(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    sources = list_sources(
        db,
        limit=limit,
        offset=offset,
    )

    return {
        "count": len(sources),
        "items": [
            {
                "id": source.id,
                "title": source.title,
                "author": source.author,
                "publication_year": source.publication_year,
                "source_type": source.source_type,
                "locator": source.locator,
                "notes": source.notes,
            }
            for source in sources
        ],
    }


@app.get("/api/v1/sources/{source_id}")
def get_source_endpoint(
    source_id: int,
    db: Session = Depends(get_db),
):
    source = get_source(db, source_id)

    if source is None:
        raise HTTPException(
            status_code=404,
            detail="Source not found.",
        )

    return {
        "id": source.id,
        "title": source.title,
        "author": source.author,
        "publication_year": source.publication_year,
        "source_type": source.source_type,
        "locator": source.locator,
        "notes": source.notes,
    }


# Mount frontend static files
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

