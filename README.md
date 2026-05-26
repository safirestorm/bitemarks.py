# Bitemarks

Bitemarks er en webapplikation til at holde styr på restauranter, caféer og barer du har besøgt.
Tilføj steder med navn, kategori, cuisine og rating, se dem på et interaktivt kort og få AI-genererede anbefalinger baseret på din historik.

## Funktioner

- Tilføj og administrer restauranter
- Kort med geocoding via Google Maps API
- Statistik over dine besøg og ratings
- AI-anbefalinger via Mistral API

## Teknologier

- **Streamlit** — frontend
- **FastAPI** — backend API
- **Pandas, NumPy, Matplotlib** — databehandling og statistik
- **Pydeck** — interaktivt kort
- **Mistral API** — AI-anbefalinger
- **Docker Compose** — kørsel af applikationen

## Forudsætninger

- Docker og Docker Compose installeret
- Google Maps API-nøgle
- Mistral API-nøgle

## Kom i gang

1. Klon projektet:
   ```bash
   git clone https://github.com/safirestorm/bitemarks.py.git
   cd bitemarks.py
   ```

2. Opret en `.env` fil i roden med dine API-nøgler:
   ```
   GOOGLE_MAPS_API_KEY=dinNøgleHer
   MISTRAL_API_KEY=dinNøgleHer
   ```

3. Start applikationen:
   ```bash
   docker compose up --build
   ```

4. Åbn Streamlit i browseren: [http://localhost:8501](http://localhost:8501)

## Test og kodekvalitet

Kør tests:
```bash
pytest
```

Kør code analysis:
```bash
ruff check .
```
