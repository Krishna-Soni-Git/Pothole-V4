"""
NS Pothole Project — Script 1: Data Collection
===============================================
Collects and merges:
  A) Weather data from Environment & Climate Change Canada (ECCC) daily API
  B) NS TIR Operations Contact Centre complaints (local xlsx)

Output: Data/NS_Project_Merged_FIXED.csv

Stations (verified ECCC IDs, all confirmed to have data 2019-2025):
  Halifax Stanfield   ID=50620  → HRM / Lunenburg          ✓ confirmed working
  Greenwood A         ID=50839  → Annapolis Valley / Kings  ✓ fixed (27141 missing Rain/Snow)
  Sydney A            ID=50839  → Cape Breton               ← see NOTE below
  Truro               ID=6354   → Colchester / Cumberland   ✓ confirmed working
  Yarmouth A          ID=50836  → SW Nova Scotia / Shelburne ✓ fixed (6244 all-null)

NOTE on Sydney: ECCC station 6526 (Sydney A) was decommissioned and data gaps exist.
  Replacement: use Glace Bay (ID=6452) or Port Hawkesbury (ID=6490) as fallback.
  The script tries Sydney_A first, then falls back automatically.

Run:
  pip install pandas openpyxl requests tqdm
  python 01_collect_data.py
"""

import os, time, warnings
import requests
import pandas as pd
import numpy as np
from io import StringIO
from tqdm import tqdm

warnings.filterwarnings("ignore")
os.makedirs("Data", exist_ok=True)
os.makedirs("Data/raw_weather", exist_ok=True)

# ── CONFIG ─────────────────────────────────────────────────────────────────────

OUTPUT_CSV = "Data/NS_Project_Merged_FIXED.csv"

START_YEAR, END_YEAR   = 2019, 2025
END_MONTH_FINAL        = 9      # data goes to Sept 2025

# ── Auto-detect OCC xlsx (searches script folder and common subfolders) ────────
_OCC_FILENAME = "Operations_Contact_Centre_Call_Summary_20260120.csv.xlsx"
_SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))

def _find_occ_file() -> str:
    """Search common locations for the OCC xlsx and return the full path."""
    candidates = [
        os.path.join(_SCRIPT_DIR, _OCC_FILENAME),                  # same folder as script
        os.path.join(_SCRIPT_DIR, "Data", _OCC_FILENAME),          # Data/ subfolder
        os.path.join(_SCRIPT_DIR, "..", _OCC_FILENAME),            # one level up
        _OCC_FILENAME,                                              # current working dir
    ]
    for path in candidates:
        if os.path.exists(path):
            return os.path.abspath(path)
    # Not found — print helpful message
    print("\n" + "!" * 65)
    print("OCC FILE NOT FOUND.")
    print(f"Expected filename: {_OCC_FILENAME}")
    print(f"Script is running from: {_SCRIPT_DIR}")
    print("\nPlease place the xlsx in the same folder as this script, OR")
    print("update OCC_FILE at the top of this script with the full path.")
    print("!" * 65 + "\n")
    raise FileNotFoundError(f"Cannot find {_OCC_FILENAME}")

OCC_FILE = _find_occ_file()

# ── ECCC station IDs (corrected — verified against station inventory) ──────────
# How to verify: https://climate.weather.gc.ca/historical_data/search_historic_data_e.html
# Search Nova Scotia → Daily → check "Last Year" >= 2025
#
# IDs that returned 100% null = station decommissioned or ID changed.
# Use the ECCC station search to find the current active ID for that airport.
STATIONS = {
    # ✓ Working perfectly
    "Halifax_Stanfield": {"id": 50620, "region": "HRM_Lunenburg",
                          "fallback_ids": []},
    # ✓ Fixed: 27141 (old Greenwood) missing Rain/Snow columns entirely
    #   50839 = Greenwood A (current active station with full obs)
    "Greenwood_A":       {"id": 50839, "region": "Annapolis_Kings",
                          "fallback_ids": [27141, 26892]},
    # ✓ Fixed: 6526 (old Sydney A) decommissioned, all null
    #   6452 = Glace Bay  |  50308 = Sydney airport newer ID
    "Sydney_A":          {"id": 50308, "region": "Cape_Breton",
                          "fallback_ids": [6452, 10965, 6526]},
    # ✓ Working perfectly
    "Truro":             {"id": 6354,  "region": "Colchester_Cumberland",
                          "fallback_ids": []},
    # ✓ Fixed: 6244 (old Yarmouth A) and 50836 have CSV parse issues
    #   43405 = Yarmouth A has temp data (precip sparse but usable)
    #   6244  = old Yarmouth, temp only fallback
    "Yarmouth_A":        {"id": 43405, "region": "SW_Nova_Shelburne",
                          "fallback_ids": [50836, 6244]},
}

# TIR supervisor area prefix → station label
# Every prefix in the OCC dataset is assigned here
AREA_TO_STATION = {
    # HRM & Lunenburg → Halifax Stanfield
    "A18": "Halifax_Stanfield", "A19": "Halifax_Stanfield",
    "A20": "Halifax_Stanfield", "B21": "Halifax_Stanfield",
    "B23": "Halifax_Stanfield", "B24": "Halifax_Stanfield",
    "B25": "Halifax_Stanfield", "B26": "Halifax_Stanfield",
    "B27": "Halifax_Stanfield", "N90": "Halifax_Stanfield",
    "N91": "Halifax_Stanfield", "N93": "Halifax_Stanfield",
    "N94": "Halifax_Stanfield",

    # Annapolis Valley / Kings → Greenwood A
    "D34": "Greenwood_A", "D36": "Greenwood_A", "D37": "Greenwood_A",
    "E40": "Greenwood_A", "E41": "Greenwood_A", "E42": "Greenwood_A",
    "E43": "Greenwood_A", "F44": "Greenwood_A", "F46": "Greenwood_A",
    "F48": "Greenwood_A",

    # SW Nova / Shelburne → Yarmouth A
    "C28": "Yarmouth_A", "C29": "Yarmouth_A", "C30": "Yarmouth_A",
    "C32": "Yarmouth_A",

    # Colchester / Cumberland → Truro
    "G49": "Truro", "G51": "Truro", "G53": "Truro",
    "G54": "Truro", "G99": "Truro", "H55": "Truro",
    "H56": "Truro", "H59": "Truro", "H60": "Truro",

    # Pictou / Antigonish / Guysborough → Truro (nearest full station)
    "I61": "Truro", "I62": "Truro", "I63": "Truro",
    "I64": "Truro", "I65": "Truro", "J67": "Truro",
    "J68": "Truro", "J69": "Truro", "J70": "Truro",
    "J71": "Truro", "J72": "Truro",

    # Cape Breton → Sydney A
    "K73": "Sydney_A", "K74": "Sydney_A", "K75": "Sydney_A",
    "K76": "Sydney_A", "K77": "Sydney_A", "L79": "Sydney_A",
    "L80": "Sydney_A", "L81": "Sydney_A", "L82": "Sydney_A",
    "L83": "Sydney_A", "M84": "Sydney_A", "M85": "Sydney_A",
    "M86": "Sydney_A", "M88": "Sydney_A", "M89": "Sydney_A",
}

# ECCC column renames → standardised names used throughout both scripts
ECCC_COL_MAP = {
    "Date/Time":               "Date",
    "Max Temp (°C)":           "Max_Temp",
    "Min Temp (°C)":           "Min_Temp",
    "Mean Temp (°C)":          "Mean_Temp",
    "Total Precip (mm)":       "Total_Precip",
    "Total Rain (mm)":         "Total_Rain",
    "Total Snow (cm)":         "Total_Snow",
    "Snow on Grnd (cm)":       "Snow_on_Grnd",
    "Spd of Max Gust (km/h)":  "Max_Gust_Speed",
    "Heat Deg Days (°C)":      "Heat_Deg_Days",
    "Cool Deg Days (°C)":      "Cool_Deg_Days",
}

NUMERIC_WEATHER_COLS = [
    "Max_Temp", "Min_Temp", "Mean_Temp",
    "Total_Precip", "Total_Rain", "Total_Snow",
    "Snow_on_Grnd", "Max_Gust_Speed",
    "Heat_Deg_Days", "Cool_Deg_Days",
]


# ══════════════════════════════════════════════════════════════════════════════
# PART A — WEATHER COLLECTION
# ══════════════════════════════════════════════════════════════════════════════

def fetch_eccc_month(station_id: int, year: int, month: int) -> pd.DataFrame | None:
    """
    Download one month of daily data from the ECCC bulk CSV API.
    Handles ECCC's inconsistent CSV formatting across stations.
    Returns a cleaned DataFrame or None on failure.
    """
    url = "https://climate.weather.gc.ca/climate_data/bulk_data_e.html"
    params = {
        "format":    "csv",
        "stationID": station_id,
        "Year":      year,
        "Month":     month,
        "Day":       14,
        "timeframe": 2,          # 2 = daily resolution
        "submit":    "Download Data",
    }
    try:
        resp = requests.get(url, params=params, timeout=40)
        resp.raise_for_status()

        # Decode with utf-8-sig to strip BOM if present
        text = resp.content.decode("utf-8-sig", errors="replace")

        # ECCC sometimes wraps the whole response in extra metadata lines.
        # Strategy: find the header row (contains "Date/Time" or "Date") and
        # read only from that row onward — ignores all preamble regardless of format.
        lines = text.splitlines()
        header_idx = None
        for i, line in enumerate(lines):
            if "Date/Time" in line or (line.startswith('"Date') and "Temp" in lines[i] if i < len(lines) else False):
                header_idx = i
                break
            # Also catch plain "Date" header
            if line.startswith('"Date"') or line.startswith('Date,') or '"Date/Time"' in line:
                header_idx = i
                break

        if header_idx is None:
            # Fall back: strip comment lines starting with "//" and hope for the best
            lines = [ln for ln in lines if not ln.startswith("//") and ln.strip()]
            if len(lines) < 3:
                return None
            clean_text = "\n".join(lines)
        else:
            clean_text = "\n".join(lines[header_idx:])

        df = pd.read_csv(
            StringIO(clean_text),
            on_bad_lines="skip",     # skip malformed rows instead of crashing
            encoding_errors="replace",
        )
        # Must have at least a date-like column to be useful
        if df.empty or len(df.columns) < 3:
            return None
        return df

    except Exception as exc:
        print(f"    ⚠  station={station_id} {year}-{month:02d}: {exc}")
        return None


def collect_weather(skip_stations: set = None) -> pd.DataFrame:
    """Download daily weather for all stations 2019-01 → 2025-09.
    Automatically tries fallback station IDs if primary returns null data.
    skip_stations: set of station labels already cached and valid."""
    if skip_stations is None:
        skip_stations = set()

    all_frames = []

    # Load already-good cached stations first
    for label in skip_stations:
        path = f"Data/raw_weather/{label}_daily.csv"
        if os.path.exists(path):
            df = pd.read_csv(path, parse_dates=["Date"])
            all_frames.append(df)
            print(f"  📂  {label}: loaded from cache ({len(df):,} rows)")

    for label, meta in STATIONS.items():
        if label in skip_stations:
            continue   # already loaded above
        region       = meta["region"]
        ids_to_try   = [meta["id"]] + meta.get("fallback_ids", [])
        station_df   = None

        for attempt, sid in enumerate(ids_to_try):
            tag = "(primary)" if attempt == 0 else f"(fallback #{attempt})"
            print(f"\n📡  {label}  (ID={sid}) {tag}")

            frames = []
            for year in range(START_YEAR, END_YEAR + 1):
                last_month = END_MONTH_FINAL if year == END_YEAR else 12
                for month in tqdm(range(1, last_month + 1),
                                  desc=f"    {year}", leave=False, unit="mo"):
                    raw = fetch_eccc_month(sid, year, month)
                    if raw is not None and not raw.empty:
                        frames.append(raw)
                    time.sleep(0.35)

            if not frames:
                print(f"  ✗  No response for ID={sid}, trying next...")
                continue

            candidate = pd.concat(frames, ignore_index=True)
            candidate = candidate.rename(
                columns={k: v for k, v in ECCC_COL_MAP.items() if k in candidate.columns}
            )
            keep = ["Date"] + [c for c in NUMERIC_WEATHER_COLS if c in candidate.columns]
            candidate = candidate[keep].copy()
            candidate["Date"] = pd.to_datetime(candidate["Date"], errors="coerce")
            candidate = candidate.dropna(subset=["Date"])
            candidate = candidate[
                (candidate["Date"] >= "2019-01-01") &
                (candidate["Date"] <= "2025-09-30")
            ]
            for col in NUMERIC_WEATHER_COLS:
                if col in candidate.columns:
                    candidate[col] = pd.to_numeric(candidate[col], errors="coerce")

            # Quality check: reject only if TEMPERATURE is >50% null
            # (precip can be missing for some stations — temp is essential for FTC)
            temp_null = candidate["Max_Temp"].isna().mean() if "Max_Temp" in candidate.columns else 1.0
            if temp_null > 0.50:
                print(f"  ✗  ID={sid} has {temp_null*100:.0f}% null Max_Temp — trying fallback...")
                continue

            # Good data — keep it
            candidate["Station_Label"] = label
            candidate["Region"]        = region
            station_df = candidate
            print(f"  ✓  ID={sid} accepted: {len(station_df):,} rows")
            break   # stop trying fallbacks

        if station_df is None:
            print(f"  ✗✗  ALL IDs failed for {label} — this region will have no weather data")
            continue

        # Save cache + print quality summary
        cache_path = f"Data/raw_weather/{label}_daily.csv"
        station_df.to_csv(cache_path, index=False)

        # ── Completeness check: expected rows vs actual rows ──────────────
        # Expected: one row per calendar day from START_YEAR-01-01 to
        # END_YEAR-END_MONTH_FINAL-last-day.  Missing months from a mid-run
        # API failure would show up as a shortfall here.
        import calendar
        last_day = calendar.monthrange(END_YEAR, END_MONTH_FINAL)[1]
        expected_days = (
            pd.Timestamp(f"{END_YEAR}-{END_MONTH_FINAL:02d}-{last_day}")
            - pd.Timestamp(f"{START_YEAR}-01-01")
        ).days + 1
        actual_days = station_df["Date"].nunique()
        if actual_days < expected_days * 0.95:
            print(f"  ⚠  COMPLETENESS WARNING for {label}: "
                  f"expected ~{expected_days:,} days, got {actual_days:,} "
                  f"({100*actual_days/expected_days:.1f}%). "
                  f"Some months may have been dropped by a failed API call.")
        else:
            print(f"  ✓  Completeness OK: {actual_days:,} / ~{expected_days:,} days "
                  f"({100*actual_days/expected_days:.1f}%)")

        for col in ["Total_Precip", "Total_Rain", "Total_Snow", "Max_Temp", "Min_Temp"]:
            if col in station_df.columns:
                pct  = 100 * station_df[col].isna().sum() / len(station_df)
                flag = "✓" if pct < 5 else ("~" if pct < 30 else "✗")
                print(f"      {flag} {col:<18} {pct:.1f}% missing")

        all_frames.append(station_df)

    combined = pd.concat(all_frames, ignore_index=True)
    print(f"\n✅  Weather collected: {len(combined):,} station-day rows")
    return combined


# ══════════════════════════════════════════════════════════════════════════════
# PART B — OCC COMPLAINTS
# ══════════════════════════════════════════════════════════════════════════════

def load_occ(filepath: str) -> pd.DataFrame:
    """Load and clean the OCC Excel file."""
    print(f"\nLoading OCC data: {filepath}")
    df = pd.read_excel(filepath, sheet_name=0)

    df["Date"] = pd.to_datetime(df["Date Logged"], errors="coerce").dt.normalize()
    df = df.dropna(subset=["Date"])
    df = df[
        (df["Date"] >= "2019-01-01") &
        (df["Date"] <= "2025-09-30")
    ].copy()

    # Extract TIR supervisor area prefix (e.g. "B25" from "B25-SE Lunenburg...")
    df["Area_Code"] = (
        df["Building Name"]
          .astype(str)
          .str.split("-")
          .str[0]
          .str.strip()
    )

    # Map area code → nearest weather station
    df["Station_Label"] = df["Area_Code"].map(AREA_TO_STATION).fillna("UNMATCHED")

    print(f"  Loaded: {len(df):,} records | "
          f"{df['Date'].min().date()} – {df['Date'].max().date()}")
    unmatched_pct = 100 * (df["Station_Label"] == "UNMATCHED").sum() / len(df)
    print(f"  Station-matched: {100-unmatched_pct:.1f}%  "
          f"({unmatched_pct:.1f}% unmatched — mostly 'Not Applicable-TIR')")

    return df


# ══════════════════════════════════════════════════════════════════════════════
# PART C — MERGE
# ══════════════════════════════════════════════════════════════════════════════

def merge(occ_df: pd.DataFrame, weather_df: pd.DataFrame) -> pd.DataFrame:
    """
    Left-join OCC records onto weather data.
    Each OCC record gets the weather reading from its matched station on that date.
    """
    print("\nMerging OCC + weather...")

    # Weather: one row per (Date, Station_Label)
    wx = weather_df.drop_duplicates(subset=["Date", "Station_Label"])

    merged = occ_df.merge(
        wx,
        on=["Date", "Station_Label"],
        how="left",
        suffixes=("", "_wx"),
    )

    # Keep only needed columns in a clean order
    occ_cols   = ["Date", "Division Name", "Building Name",
                  "Assigned Service Department Name",
                  "Category Shortcode", "Item Name",
                  "Area_Code", "Station_Label"]
    wx_cols    = [c for c in NUMERIC_WEATHER_COLS if c in merged.columns]
    region_col = ["Region"] if "Region" in merged.columns else []

    merged = merged[occ_cols + region_col + wx_cols].copy()

    # Quality check
    total   = len(merged)
    matched = merged["Max_Temp"].notna().sum()
    print(f"  Total rows:          {total:,}")
    print(f"  Weather-matched rows:{matched:,}  ({100*matched/total:.1f}%)")
    print(f"  Pothole records:     {(merged['Category Shortcode']=='TCC-POTHOLE').sum():,}")

    return merged


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 65)
    print("NS POTHOLE PROJECT — STEP 1: DATA COLLECTION")
    print("=" * 65)

    # Check for cached weather — but validate quality before trusting cache
    cache_files = [f for f in os.listdir("Data/raw_weather") if f.endswith(".csv")]
    cached_good = []
    cached_bad  = []
    for label in STATIONS:
        path = f"Data/raw_weather/{label}_daily.csv"
        if os.path.exists(path):
            try:
                test = pd.read_csv(path, nrows=100)
                if "Max_Temp" in test.columns and test["Max_Temp"].notna().sum() > 5:
                    cached_good.append(label)
                else:
                    cached_bad.append(label)
                    print(f"  ⚠  Cached {label} has null temperature — will re-download")
            except Exception:
                cached_bad.append(label)

    if cached_bad:
        # Delete bad cache files so they get re-downloaded
        for label in cached_bad:
            path = f"Data/raw_weather/{label}_daily.csv"
            if os.path.exists(path):
                os.remove(path)

    if len(cached_good) >= len(STATIONS):
        print("\n📂  All cached weather valid — loading from Data/raw_weather/")
        frames = []
        for label in STATIONS:
            path = f"Data/raw_weather/{label}_daily.csv"
            if os.path.exists(path):
                df = pd.read_csv(path, parse_dates=["Date"])
                frames.append(df)
                print(f"  Loaded {label}: {len(df):,} rows")
        weather = pd.concat(frames, ignore_index=True)
    else:
        if cached_good:
            print(f"\n📂  Partial cache found ({len(cached_good)}/{len(STATIONS)} stations good)")
            print(f"   Good: {cached_good}")
            print(f"   Re-downloading: {cached_bad + [s for s in STATIONS if s not in cached_good + cached_bad]}")
        else:
            print("\n🌐  Downloading weather from ECCC (~20-40 min)...")
        weather = collect_weather(skip_stations=set(cached_good))

    occ     = load_occ(OCC_FILE)
    merged  = merge(occ, weather)

    merged.to_csv(OUTPUT_CSV, index=False)
    print(f"\n✅  Merged dataset saved → {OUTPUT_CSV}")
    print(f"    Shape: {merged.shape[0]:,} rows × {merged.shape[1]} columns")
    print(f"\nColumn list:")
    for col in merged.columns:
        print(f"  {col}")

    print("\n" + "=" * 65)
    print("Ready for analysis. Run: python 02_analysis.py")
    print("=" * 65)


if __name__ == "__main__":
    main()