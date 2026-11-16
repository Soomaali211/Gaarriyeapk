# Backend-ka Gaarriye — API aasaasi ah

## Xaaladda hadda
- FastAPI server iyo endpoints waa la diyaariyey.
- HTML-ku wuxuu u diraa `POST /api/v1/analyze`.
- `GET /health` wuxuu xaqiijiyaa in server-ku socdo.
- `GET /api/v1/genres` wuxuu bixiyaa diiwaanka noocyada.
- **Metrical engine weli ma jiro.** Endpoint-ka falanqayntu si ula kac ah ayuu u soo celiyaa `501 ENGINE_NOT_READY`; ma curinayo miisaan, xeerar, ama fasiraad.

## Sida loo bilaabo
Python 3.11+ ayaa lagu taliyey.

```bash
cd backend
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000  
Docs: http://127.0.0.1:8000/docs

## Furitaanka frontend-ka
Habka lagu taliyey: ka fur terminal kale:

```bash
cd frontend
python -m http.server 5500
```

Kadib booqo http://127.0.0.1:5500

Haddii aad HTML-ka si toos ah `file://` uga furto, browser-ka qaar waxay xannibi karaan API request-ka. Isticmaal server-ka kore.

## API contract
`POST /api/v1/analyze`

```json
{
  "text": "Qoraalka maansada",
  "genre": "jiifto",
  "mode": "gaarriye_strict"
}
```

Marka engine-ka aan la xaqiijin, jawaabtu waa HTTP 501 oo leh `analysis_performed: false`. Taasi ma aha fashil qarsoon; waa ilaalin si aan natiijo been ah loo soo bandhigin.

## Kahor hawlgelinta engine-ka
1. Dib-u-eeg oo xaqiiji xeer kasta adigoo adeegsanaya bogga iyo jaantuska asalka ah.
2. Diiwaangeli fasiraadaha cilmi-baadhayaasha si gooni ah.
3. Xeer kasta sii aqoonsi, nooc, il, bog, tusaale, heer kalsooni iyo ansixin bini'aadan.
4. Kaliya xeerarka `APPROVED` ee leh caddeyn ku filan ayaa geli kara Gaarriye Strict Mode.
5. Ku dar tijaabooyin sax ah iyo kuwa khaldan ka hor inta aan xeer la hawlgelin.
6. `y/w` iyo xeer kasta oo kale oo aan la xaqiijin waa in uu ahaadaa proposal; lama hawlgelin karo si toos ah.

## Tijaabooyinka
```bash
cd backend
pytest -q
```

## Amniga
CORS-ka hadda wuxuu u oggol yahay horumarinta maxalliga ah oo keliya. Marka la daabacayo, ku koob origins-ka domain-ka rasmiga ah, ku dar authentication/rate limiting marka loo baahdo, kuna kaydi secrets-ka environment variables. Ha gelin xog sir ah repo-ga.\n
