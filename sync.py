"""
sync.py -- Intervals.icu -> training.db sync script
Run at the start of each Cowork session to pull new data.

Usage:
    python sync.py                          (one athlete configured -> auto)
    python sync.py --athlete <name>         (multiple athletes configured)
    python sync.py --athlete <name> --history 730   (first sync: pull 2 years)

    Athlete names are discovered dynamically from your .env file --
    anything named ATHLETE_ID_<NAME> becomes a valid --athlete value
    (case-insensitive).

    --history only matters on first sync (empty DB). After that, sync
    resumes from the most recent activity date automatically.

Requires:
    pip install requests python-dotenv

Config:
    Set API_KEY and one or more ATHLETE_ID_<NAME> entries in a .env
    file (or as environment variables). Each athlete gets their own
    training.db stored in their athletes/<name>/ subdirectory.

    Example .env:
        API_KEY=your_api_key_here
        ATHLETE_ID_ME=i123456
        ATHLETE_ID_ALEX=i789012
"""

import os
import sqlite3
import argparse
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# -- Config --------------------------------------------------------------------

load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def discover_athletes() -> dict:
    """
    Scan the environment for ATHLETE_ID_<NAME> entries and return
    a {lowercase_name: athlete_id} dict. Skips entries with empty
    or placeholder-looking values (e.g. 'iXXXXXX' from the template).
    """
    athletes = {}
    for key, value in os.environ.items():
        if not key.startswith("ATHLETE_ID_"):
            continue
        if key == "ATHLETE_ID":  # reserved for MCP default, see .env
            continue
        name = key[len("ATHLETE_ID_"):].lower()
        if not name or not value:
            continue
        if value.strip().lower() in ("ixxxxxx", "iyyyyyy", "izzzzzz"):
            continue  # still on the template value
        athletes[name] = value.strip()
    return athletes


ATHLETES = discover_athletes()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://intervals.icu/api/v1"


def resolve_athlete(name: str):
    """Return (athlete_id, db_path) for the given athlete name."""
    athlete_id = ATHLETES.get(name.lower())
    if not athlete_id:
        configured = ", ".join(sorted(ATHLETES)) or "(none)"
        raise ValueError(
            f"No ATHLETE_ID found for '{name}'. "
            f"Configured athletes: {configured}. "
            f"Set ATHLETE_ID_{name.upper()} in your .env file."
        )
    db_path = os.path.join(SCRIPT_DIR, "athletes", name.lower(), "training.db")
    return athlete_id, db_path

# -- Database setup ------------------------------------------------------------

def init_db(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS activities (
            id TEXT PRIMARY KEY,
            date TEXT,
            name TEXT,
            type TEXT,
            distance_m REAL,
            duration_s INTEGER,
            moving_time_s INTEGER,
            avg_pace_per_km REAL,
            avg_hr INTEGER,
            max_hr INTEGER,
            avg_cadence REAL,
            elevation_gain_m REAL,
            calories INTEGER,
            rpe INTEGER,
            feel INTEGER,
            ctl REAL,
            atl REAL,
            trimp REAL,
            hr_load REAL,
            pace_load REAL,
            intensity REAL,
            avg_temp_c REAL,
            weight_kg REAL,
            notes TEXT,
            synced_at TEXT
        );

        CREATE TABLE IF NOT EXISTS wellness (
            date TEXT PRIMARY KEY,
            ctl REAL,
            atl REAL,
            ramp_rate REAL,
            ctl_load REAL,
            resting_hr INTEGER,
            hrv REAL,
            sleep_hours REAL,
            sleep_quality INTEGER,
            sleep_score REAL,
            weight_kg REAL,
            steps INTEGER,
            vo2max REAL,
            synced_at TEXT
        );

        CREATE TABLE IF NOT EXISTS sync_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            synced_at TEXT,
            activities_added INTEGER,
            wellness_added INTEGER,
            oldest_date TEXT,
            newest_date TEXT
        );
    """)
    conn.commit()

# -- Helpers -------------------------------------------------------------------

def get_last_synced_date(conn, history_days: int = 90) -> str:
    """Return the most recent activity date in the DB, or history_days ago."""
    row = conn.execute("SELECT MAX(date) FROM activities").fetchone()
    if row and row[0]:
        last = datetime.fromisoformat(row[0][:10])
        start = last - timedelta(days=2)
        return start.strftime("%Y-%m-%d")
    else:
        return (datetime.now() - timedelta(days=history_days)).strftime("%Y-%m-%d")

def pace_per_km(distance_m, duration_s):
    if not distance_m or distance_m == 0:
        return None
    return (duration_s / distance_m) * 1000

def format_pace(secs_per_km) -> str:
    if secs_per_km is None:
        return "--"
    mins = int(secs_per_km // 60)
    secs = int(secs_per_km % 60)
    return f"{mins}:{secs:02d}/km"

# -- API calls -----------------------------------------------------------------

def fetch_activities(athlete_id: str, start_date: str, end_date: str) -> list:
    url = f"{BASE_URL}/athlete/{athlete_id}/activities"
    params = {"oldest": start_date, "newest": end_date}
    resp = requests.get(url, auth=("API_KEY", API_KEY), params=params)
    resp.raise_for_status()
    return resp.json()

def fetch_wellness(athlete_id: str, start_date: str, end_date: str) -> list:
    url = f"{BASE_URL}/athlete/{athlete_id}/wellness"
    params = {"oldest": start_date, "newest": end_date}
    resp = requests.get(url, auth=("API_KEY", API_KEY), params=params)
    resp.raise_for_status()
    return resp.json()

# -- Sync functions ------------------------------------------------------------

def sync_activities(conn, athlete_id: str, start_date: str, end_date: str) -> int:
    print(f"  Fetching activities {start_date} -> {end_date}...")
    activities = fetch_activities(athlete_id, start_date, end_date)
    added = 0

    for a in activities:
        activity_id = str(a.get("id", ""))
        date_str = (a.get("start_date_local") or a.get("start_date") or "")[:19]
        distance = a.get("distance") or 0
        duration = a.get("elapsed_time") or a.get("moving_time") or 0
        moving_time = a.get("moving_time") or duration

        row = {
            "id": activity_id,
            "date": date_str,
            "name": a.get("name"),
            "type": a.get("type"),
            "distance_m": distance,
            "duration_s": duration,
            "moving_time_s": moving_time,
            "avg_pace_per_km": pace_per_km(distance, moving_time),
            "avg_hr": a.get("average_heartrate"),
            "max_hr": a.get("max_heartrate"),
            "avg_cadence": a.get("average_cadence"),
            "elevation_gain_m": a.get("total_elevation_gain"),
            "calories": a.get("calories"),
            "rpe": a.get("perceived_exertion"),
            "feel": a.get("feel"),
            "ctl": a.get("ctl"),
            "atl": a.get("atl"),
            "trimp": a.get("trimp"),
            "hr_load": a.get("hr_load"),
            "pace_load": a.get("pace_load"),
            "intensity": a.get("intensity"),
            "avg_temp_c": a.get("average_temp"),
            "weight_kg": a.get("athlete_weight"),
            "notes": a.get("description"),
            "synced_at": datetime.now().isoformat(),
        }

        conn.execute("""
            INSERT OR REPLACE INTO activities VALUES (
                :id, :date, :name, :type, :distance_m, :duration_s,
                :moving_time_s, :avg_pace_per_km, :avg_hr, :max_hr,
                :avg_cadence, :elevation_gain_m, :calories, :rpe, :feel,
                :ctl, :atl, :trimp, :hr_load, :pace_load, :intensity,
                :avg_temp_c, :weight_kg, :notes, :synced_at
            )
        """, row)
        added += 1

    conn.commit()
    print(f"  + {added} activities synced")
    return added

def sync_wellness(conn, athlete_id: str, start_date: str, end_date: str) -> int:
    print(f"  Fetching wellness {start_date} -> {end_date}...")
    wellness = fetch_wellness(athlete_id, start_date, end_date)
    added = 0

    for w in wellness:
        date = w.get("id")
        if not date:
            continue

        row = {
            "date": date,
            "ctl": w.get("ctl"),
            "atl": w.get("atl"),
            "ramp_rate": w.get("rampRate"),
            "ctl_load": w.get("ctlLoad"),
            "resting_hr": w.get("restingHR"),
            "hrv": w.get("hrv"),
            "sleep_hours": w.get("sleepSecs") / 3600 if w.get("sleepSecs") else None,
            "sleep_quality": w.get("sleepQuality"),
            "sleep_score": w.get("sleepScore"),
            "weight_kg": w.get("weight"),
            "steps": w.get("steps"),
            "vo2max": w.get("vo2max"),
            "synced_at": datetime.now().isoformat(),
        }

        conn.execute("""
            INSERT OR REPLACE INTO wellness VALUES (
                :date, :ctl, :atl, :ramp_rate, :ctl_load, :resting_hr,
                :hrv, :sleep_hours, :sleep_quality, :sleep_score,
                :weight_kg, :steps, :vo2max, :synced_at
            )
        """, row)
        added += 1

    conn.commit()
    print(f"  + {added} wellness entries synced")
    return added

# -- Summary query -------------------------------------------------------------

def print_recent_summary(conn, days=14):
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = conn.execute("""
        SELECT date, name, type, distance_m, avg_pace_per_km, avg_hr, ctl, atl, rpe
        FROM activities
        WHERE date >= ? AND type = 'Run'
        ORDER BY date DESC
    """, (cutoff,)).fetchall()

    print(f"\n  Recent runs (last {days} days):")
    for r in rows:
        date, name, typ, dist, pace, hr, ctl, atl, rpe = r
        dist_km = f"{dist/1000:.1f}km" if dist else "--"
        pace_str = format_pace(pace)
        hr_str = f"{int(hr)}bpm" if hr else "--"
        ctl_str = f"CTL {ctl:.1f}" if ctl else ""
        rpe_str = f"RPE {rpe}" if rpe else ""
        print(f"    {date[:10]}  {name or typ:<20}  {dist_km:<8}  {pace_str:<10}  {hr_str:<8}  {ctl_str}  {rpe_str}")

# -- Main ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Sync Intervals.icu data to training.db")
    parser.add_argument(
        "--athlete",
        default=None,
        help=(
            "Which athlete to sync (case-insensitive). "
            "Must match an ATHLETE_ID_<NAME> entry in your .env. "
            "Optional if only one athlete is configured."
        ),
    )
    parser.add_argument(
        "--history",
        type=int,
        default=90,
        help="Days of history to pull on first sync when DB is empty (default: 90)"
    )
    args = parser.parse_args()

    if not ATHLETES:
        raise ValueError(
            "No athletes configured. Add at least one ATHLETE_ID_<NAME> "
            "entry to your .env file (and replace the iXXXXXX placeholder "
            "with a real Intervals.icu athlete ID)."
        )

    athlete_name = args.athlete
    if athlete_name is None:
        if len(ATHLETES) == 1:
            athlete_name = next(iter(ATHLETES))
        else:
            configured = ", ".join(sorted(ATHLETES))
            raise ValueError(
                f"Multiple athletes configured ({configured}). "
                f"Specify one with --athlete <name>."
            )

    athlete_id, db_path = resolve_athlete(athlete_name)

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    if not API_KEY:
        raise ValueError("API_KEY must be set in .env or environment")

    print(f"\n{'='*60}")
    print(f"  Intervals.icu -> training.db sync")
    print(f"  Athlete: {athlete_name.upper()} ({athlete_id})")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    conn = sqlite3.connect(db_path)
    init_db(conn)

    start_date = get_last_synced_date(conn, history_days=args.history)
    end_date = datetime.now().strftime("%Y-%m-%d")

    print(f"\n  Sync window: {start_date} -> {end_date}")

    acts_added = sync_activities(conn, athlete_id, start_date, end_date)
    well_added = sync_wellness(conn, athlete_id, start_date, end_date)

    conn.execute("""
        INSERT INTO sync_log (synced_at, activities_added, wellness_added, oldest_date, newest_date)
        VALUES (?, ?, ?, ?, ?)
    """, (datetime.now().isoformat(), acts_added, well_added, start_date, end_date))
    conn.commit()

    print_recent_summary(conn)

    total_acts = conn.execute("SELECT COUNT(*) FROM activities").fetchone()[0]
    total_well = conn.execute("SELECT COUNT(*) FROM wellness").fetchone()[0]
    oldest = conn.execute("SELECT MIN(date) FROM activities").fetchone()[0]
    print(f"\n  DB totals: {total_acts} activities, {total_well} wellness entries")
    print(f"  History from: {oldest[:10] if oldest else 'n/a'}")
    print(f"{'='*60}\n")

    conn.close()

if __name__ == "__main__":
    main()