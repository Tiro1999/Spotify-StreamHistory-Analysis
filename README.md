# Spotify-Streaming-History-Analysis
My personal Spotify Data Analysis Repository

## Setup

1. Add your files you can request on your [Spotify privacy settings](https://www.spotify.com/de/account/privacy/)
2. Devcontainer: Rebuild and open in Container
3. Terminal Setup:
```bash
cd src
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Windows:
.\venv\Scripts\pip install -r requirements.txt

# Linux/Mac:
./venv/bin/pip install -r requirements.txt
```

4. You need to select the activated venv as kernal for your jupyter notebook

## Projektstruktur

```
src/
  config.py                       # Globale Einstellungen (Pfade, Top-N, Farben, etc.)
  data_loader.py                  # Daten laden & aufbereiten
  requirements.txt                # Python Dependencies
  notebooks/
    01_overview.ipynb             # Gesamtübersicht (Stunden, Artists, Tracks)
    02_yearly_trends.ipynb        # Monatliche Trends, Rolling Averages
    03_top_artists_tracks.ipynb   # Top Artists & Tracks pro Jahr
    04_listening_patterns.ipynb   # Heatmaps, Tageszeit, Platform, Skip-Rate
    05_genre_analysis.ipynb       # Genre-Analyse (benötigt Spotify API)
results/
  overview/                       # Jahresübergreifende Plots
  <year>/                         # Plots pro Jahr
res/                     
  /2026-04-13_my_spotify_data     # Spotify Exportdaten (gitignored) - extrahierte .zip
```

## Konfiguration

Alle globalen Einstellungen in `src/config.py`:
- `MIN_MS_PLAYED` – Mindest-Hörzeit pro Stream (Default: 30s)
- `TOP_N_ARTISTS` / `TOP_N_TRACKS` – Anzahl Einträge in Rankings
- `YEARS_TO_ANALYZE` – Jahre einschränken (Default: alle)
- Plot-Farben, Größen, DPI
