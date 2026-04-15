"""
Daten-Loader für Spotify Extended Streaming History.
Lädt alle JSON-Dateien, kombiniert sie und bereitet die Daten auf.
"""

import json
import pandas as pd
from pathlib import Path
from config import DATA_DIR, MIN_MS_PLAYED, YEARS_TO_ANALYZE, RESULTS_DIR


def load_raw_data(audio_only: bool = True) -> pd.DataFrame:
    """Lädt alle Streaming-History JSON-Dateien und gibt einen kombinierten DataFrame zurück."""
    pattern = "Streaming_History_Audio_*.json" if audio_only else "Streaming_History_*.json"
    files = sorted(DATA_DIR.glob(pattern))

    if not files:
        raise FileNotFoundError(f"Keine Dateien gefunden in {DATA_DIR} mit Pattern '{pattern}'")

    all_records = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            records = json.load(fh)
            all_records.extend(records)
        print(f"  Geladen: {f.name} ({len(records)} Einträge)")

    df = pd.DataFrame(all_records)
    print(f"\nGesamt: {len(df)} Einträge aus {len(files)} Dateien")
    return df


def prepare_dataframe(df: pd.DataFrame, filter_min_ms: bool = True) -> pd.DataFrame:
    """Bereitet den DataFrame auf: Timestamps parsen, Spalten ergänzen, filtern."""
    df = df.copy()

    # Timestamp parsen
    df["ts"] = pd.to_datetime(df["ts"], utc=True)

    # Kürzere Spaltennamen
    df = df.rename(columns={
        "master_metadata_track_name": "track",
        "master_metadata_album_artist_name": "artist",
        "master_metadata_album_album_name": "album",
    })

    # Abgeleitete Spalten
    df["year"] = df["ts"].dt.year
    df["month"] = df["ts"].dt.month
    df["day"] = df["ts"].dt.day
    df["hour"] = df["ts"].dt.hour
    df["weekday"] = df["ts"].dt.day_name()
    df["weekday_num"] = df["ts"].dt.weekday  # 0=Montag, 6=Sonntag
    df["date"] = df["ts"].dt.date
    df["year_month"] = df["ts"].dt.tz_localize(None).dt.to_period("M")

    # Minuten berechnen
    df["minutes_played"] = df["ms_played"] / 60_000
    df["hours_played"] = df["ms_played"] / 3_600_000

    # Musik vs. Podcast/Audiobook
    df["is_music"] = df["track"].notna() & (df["episode_name"].isna())
    df["is_podcast"] = df["episode_name"].notna()

    # Kurze Streams filtern
    if filter_min_ms:
        before = len(df)
        df = df[df["ms_played"] >= MIN_MS_PLAYED]
        print(f"Gefiltert: {before - len(df)} Einträge unter {MIN_MS_PLAYED/1000:.0f}s entfernt "
              f"({len(df)} verbleibend)")

    # Nach Jahr filtern falls konfiguriert
    if YEARS_TO_ANALYZE:
        df = df[df["year"].isin(YEARS_TO_ANALYZE)]
        print(f"Jahre gefiltert auf: {YEARS_TO_ANALYZE} ({len(df)} Einträge)")

    return df.sort_values("ts").reset_index(drop=True)


def load_data(audio_only: bool = True, filter_min_ms: bool = True) -> pd.DataFrame:
    """Hauptfunktion: Lädt und bereitet alle Daten auf."""
    print("Lade Spotify Streaming History...\n")
    df = load_raw_data(audio_only=audio_only)
    df = prepare_dataframe(df, filter_min_ms=filter_min_ms)
    print(f"\nDaten bereit: {len(df)} Einträge von {df['year'].min()} bis {df['year'].max()}")
    return df


def get_music(df: pd.DataFrame) -> pd.DataFrame:
    """Filtert nur Musik-Streams (keine Podcasts/Audiobooks)."""
    return df[df["is_music"]].copy()


def get_podcasts(df: pd.DataFrame) -> pd.DataFrame:
    """Filtert nur Podcast-Streams."""
    return df[df["is_podcast"]].copy()


def ensure_results_dir(year: int | str) -> Path:
    """Erstellt results/<year>/ Ordner falls nötig und gibt den Pfad zurück."""
    path = RESULTS_DIR / str(year)
    path.mkdir(parents=True, exist_ok=True)
    return path
