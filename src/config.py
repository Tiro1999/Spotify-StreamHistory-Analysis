"""
Globale Konfiguration für die Spotify Streaming History Analyse.
Hier werden Pfade, Jahre, Farbschemata und Plot-Einstellungen zentral verwaltet.
"""

from pathlib import Path

# ============================================================================
# PFADE – Hier anpassen falls sich die Ordnerstruktur ändert
# ============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "res" / "Spotify Extended Streaming History"
RESULTS_DIR = PROJECT_ROOT / "results"

# ============================================================================
# ANALYSE-EINSTELLUNGEN
# ============================================================================

# Jahre die analysiert werden sollen (None = alle verfügbaren)
YEARS_TO_ANALYZE: list[int] | None = None  # z.B. [2023, 2024, 2025]

# Minimale Hörzeit in Sekunden, damit ein Stream gezählt wird (filtert versehentliche Plays)
MIN_MS_PLAYED = 30_000  # 30 Sekunden

# Anzahl Top-Einträge für Rankings
TOP_N_ARTISTS = 20
TOP_N_TRACKS = 20

# ============================================================================
# PLOT-EINSTELLUNGEN
# ============================================================================

PLOT_STYLE = "seaborn-v0_8-darkgrid"
PLOT_DPI = 150
PLOT_FIGSIZE_WIDE = (14, 6)
PLOT_FIGSIZE_SQUARE = (10, 8)
PLOT_FIGSIZE_TALL = (10, 12)

# Farbpalette (Spotify-inspiriert)
COLOR_PRIMARY = "#1DB954"       # Spotify Grün
COLOR_SECONDARY = "#191414"     # Spotify Schwarz
COLOR_ACCENT = "#1ED760"        # Helleres Grün
COLOR_BG = "#121212"            # Dunkler Hintergrund
COLOR_TEXT = "#FFFFFF"           # Weiß

# Palette für mehrere Kategorien
COLOR_PALETTE = [
    "#1DB954", "#1ED760", "#2EBD59", "#57B660",
    "#1AA34A", "#148A3C", "#0F7132", "#0A5827",
    "#064F20", "#004516", "#509BF5", "#A0C4FF",
    "#FFD93D", "#FF6B6B", "#C44569", "#786FA6",
    "#F8A5C2", "#63CDDA", "#CF6A87", "#574B90",
]

# ============================================================================
# SPOTIFY API (für Genre-Analyse) – Credentials in .env Datei ablegen!
# ============================================================================
# Erstelle eine .env Datei im Projektroot mit:
#   SPOTIPY_CLIENT_ID=dein_client_id
#   SPOTIPY_CLIENT_SECRET=dein_client_secret

SPOTIFY_GENRE_CACHE_FILE = PROJECT_ROOT / "src" / ".genre_cache.json"
