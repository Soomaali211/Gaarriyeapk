# ZIP 05 — Backend & Database Integration

## Ujeeddo

ZIP 05 wuxuu isku xiraa FastAPI iyo meter-engine foundation ee ZIP 03. Wuxuu API-ga u ballaadhiyaa saddexda hab-falanqayn ee Note Live, isagoo ilaalinaya kala soociddooda iyo xeerka ah inaan la soo saarin miisaan aan caddayn lahayn.

## Isbeddellada

- `backend/app/main.py` — UPDATE: `analysis_modes` contract cusub, validation, legacy `mode` compatibility, iyo engine adapter.
- `backend/tests/test_api.py` — UPDATE: tijaabooyinka API-ga cusub iyo kuwii hore.
- `backend/app/meter_engine/` — UNCHANGED: nuqul tixraac ah oo ZIP 03 ah si package-ku u muujiyo ku-tiirsanaanta saxda ah. Haddii ZIP 03 hore loo rakibay, ha ku dul qorin wax ka beddel maxalli ah; marka hore isbarbar dhig.

## API contract cusub

`POST /api/v1/analyze`

```json
{
  "text": "Sadarka koowaad\nSadarka labaad",
  "genre": "jiifto",
  "analysis_modes": {
    "gaarriye": true,
    "researchers": true,
    "compatible_other": false
  }
}
```

Fasiraadda:
- `gaarriye`: xeerarka si toos ah Gaarriye looga hayo.
- `researchers`: fasiraadaha cilmi-baadhayaasha; looma nisbaynayo Gaarriye.
- `compatible_other`: xeerar kale oo waafaqsan qaabka, balse aan ahayn labada qaybood ee kore.

Mid kasta si gooni ah ayaa loo shidi/damin karaa. Dhammaantood OFF waxay keenayaan HTTP 422 iyo `NO_ANALYSIS_CLASS_ENABLED`.

Jawaabta hadda jirta waxay si ula kac ah u sidataa `analysis_performed: false`, `status: UNVERIFIED`, `rules_applied: []`, iyo `code: ENGINE_NOT_READY`. HTTP 200 halkan wuxuu ka dhigan yahay in API-gu aqbalay codsiga oo soo saaray qaab-jawaabtiisa; macnaheedu ma aha in miisaanka la xisaabiyey ama xeer la xaqiijiyey la adeegsaday.

## Iswaafajinta hore

Codsiyada hore ee wata `mode: gaarriye_strict` ama `mode: research_comparison` weli waa la aqbalayaa. `mode` iyo `analysis_modes` isku codsi laguma wada diri karo. Habka hore ee cilmi-baadhista waxaa loo turjumayaa researcher-only, si aan si qarsoodi ah loogu darin fasalka Gaarriye.

## Database

ZIP 05 ma beddelayo models ama migrations. Sababtu waa in isbeddelkan uu yahay API orchestration; weli ma jiro rule execution adapter oo u baahan columns cusub. Migrations-kii hore waa la tijaabiyey upgrade/downgrade.

## Xaaladda shaqada

- API contract iyo engine foundation adapter: la qoray oo tijaabooyin lagu xaqiijiyey.
- Meter matching / scansion: MA JIRO weli.
- Rule registry ilaa engine: lama xirin.
- Database migration cusub: looma baahnayn ZIP 05.
- Frontend-ka ZIP 04: wali wuxuu adeegsadaa legacy mode marka uu API la hadlayo; ZIP dambe ayaa u wareejinaya `analysis_modes` si saddexda switch si buuxda API-ga ugu gudbaan.

## Tijaabooyinka

Gudaha `backend/`:

```bash
PYTHONPATH=. pytest -q
```

Tijaabada migration-ka:

```bash
DATABASE_URL=sqlite:////tmp/gaarriye_migration_test.db alembic upgrade head
DATABASE_URL=sqlite:////tmp/gaarriye_migration_test.db alembic downgrade base
```
