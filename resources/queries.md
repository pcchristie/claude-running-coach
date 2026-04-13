# training.db Query Reference

SQLite database path defined in SKILL.md. Connect via Python sqlite3 in Cowork.

Use these queries in Cowork via Python sqlite3 or direct SQL. Schema is
defined in sync.py — key tables: `activities`, `wellness`, `sync_log`.

---

## Schema Reference

### activities
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | Intervals.icu activity ID |
| date | TEXT | ISO datetime |
| name | TEXT | Activity name |
| type | TEXT | 'Run', 'Ride', 'Pilates', etc. |
| distance_m | REAL | Metres |
| duration_s | INTEGER | Seconds (elapsed) |
| moving_time_s | INTEGER | Seconds (moving) |
| avg_pace_per_km | REAL | Seconds per km |
| avg_hr | INTEGER | bpm |
| max_hr | INTEGER | bpm |
| avg_cadence | REAL | spm |
| elevation_gain_m | REAL | Metres |
| calories | INTEGER | — |
| rpe | INTEGER | 1–10 |
| feel | INTEGER | 1–5 |
| ctl | REAL | Fitness at time of activity |
| atl | REAL | Fatigue at time of activity |
| trimp | REAL | Training impulse |
| hr_load | REAL | HR-based load |
| pace_load | REAL | Pace-based load |
| intensity | REAL | Intensity factor (%) |
| avg_temp_c | REAL | °C |
| weight_kg | REAL | kg at time of activity |
| notes | TEXT | Description field |

### wellness
| Column | Type | Notes |
|--------|------|-------|
| date | TEXT PK | YYYY-MM-DD |
| ctl | REAL | Fitness |
| atl | REAL | Fatigue |
| ramp_rate | REAL | CTL change rate |
| ctl_load | REAL | Daily load |
| resting_hr | INTEGER | bpm |
| hrv | REAL | ms |
| sleep_hours | REAL | Hours |
| sleep_quality | INTEGER | 1–5 |
| sleep_score | REAL | Device score /100 |
| weight_kg | REAL | kg |
| steps | INTEGER | Daily steps |
| vo2max | REAL | ml/kg/min |

---

## Standard Queries

### Recent Training (Last 8 Weeks)
```sql
-- Weekly run volume
SELECT
  substr(date, 1, 7) AS month,
  strftime('%Y-W%W', date) AS week,
  COUNT(*) AS sessions,
  ROUND(SUM(distance_m) / 1000.0, 1) AS km,
  ROUND(SUM(moving_time_s) / 3600.0, 1) AS hours,
  ROUND(AVG(avg_hr), 0) AS avg_hr,
  ROUND(AVG(rpe), 1) AS avg_rpe
FROM activities
WHERE type = 'Run'
  AND date >= date('now', '-8 weeks')
GROUP BY week
ORDER BY week DESC;

-- Recent runs with pace
SELECT
  substr(date, 1, 10) AS date,
  name,
  ROUND(distance_m / 1000.0, 1) AS km,
  ROUND(avg_pace_per_km / 60.0, 2) AS pace_min_km,
  avg_hr,
  rpe,
  ctl,
  atl,
  ROUND(avg_temp_c, 0) AS temp_c
FROM activities
WHERE type = 'Run'
  AND date >= date('now', '-14 days')
ORDER BY date DESC;

-- Longest recent sessions
SELECT
  type,
  ROUND(MAX(distance_m) / 1000.0, 1) AS longest_km,
  ROUND(MAX(moving_time_s) / 3600.0, 1) AS longest_hours
FROM activities
WHERE date >= date('now', '-12 weeks')
GROUP BY type;
```

### Fitness & Load Trends
```sql
-- CTL/ATL trend (last 30 days)
SELECT
  date,
  ROUND(ctl, 1) AS ctl,
  ROUND(atl, 1) AS atl,
  ROUND(ctl - atl, 1) AS tsb,
  ROUND(ramp_rate, 2) AS ramp_rate,
  resting_hr,
  hrv
FROM wellness
WHERE date >= date('now', '-30 days')
ORDER BY date DESC;

-- Peak CTL ever recorded
SELECT
  date,
  ROUND(ctl, 1) AS peak_ctl
FROM wellness
ORDER BY ctl DESC
LIMIT 5;

-- Weekly load by week
SELECT
  strftime('%Y-W%W', date) AS week,
  ROUND(SUM(ctl_load), 0) AS total_load,
  ROUND(AVG(ctl), 1) AS avg_ctl,
  ROUND(AVG(atl), 1) AS avg_atl
FROM wellness
WHERE date >= date('now', '-12 weeks')
GROUP BY week
ORDER BY week DESC;
```

### Wellness & Recovery
```sql
-- Recent wellness snapshot
SELECT
  date,
  resting_hr,
  hrv,
  ROUND(sleep_hours, 1) AS sleep_hrs,
  sleep_quality,
  sleep_score,
  ROUND(weight_kg, 1) AS weight_kg,
  steps
FROM wellness
WHERE date >= date('now', '-14 days')
ORDER BY date DESC;

-- Resting HR trend (illness detection)
SELECT
  date,
  resting_hr,
  ROUND(ctl, 1) AS ctl
FROM wellness
WHERE resting_hr IS NOT NULL
  AND date >= date('now', '-30 days')
ORDER BY date DESC;

-- Days with suppressed HRV
SELECT
  date,
  hrv,
  resting_hr,
  ctl_load
FROM wellness
WHERE hrv IS NOT NULL
  AND date >= date('now', '-30 days')
ORDER BY hrv ASC;
```

### Historical Foundation
```sql
-- Lifetime run stats
SELECT
  COUNT(*) AS total_runs,
  ROUND(SUM(distance_m) / 1000.0, 0) AS total_km,
  ROUND(MAX(distance_m) / 1000.0, 1) AS longest_km,
  MIN(substr(date, 1, 10)) AS first_run,
  MAX(substr(date, 1, 10)) AS last_run
FROM activities
WHERE type = 'Run';

-- Peak training weeks (by load)
SELECT
  strftime('%Y-W%W', date) AS week,
  ROUND(SUM(ctl_load), 0) AS weekly_load,
  ROUND(SUM(ctl_load * 3600.0 / 1000.0), 0) AS approx_km
FROM wellness
GROUP BY week
ORDER BY weekly_load DESC
LIMIT 10;

-- Training day preferences (run)
SELECT
  CASE strftime('%w', date)
    WHEN '0' THEN 'Sunday'
    WHEN '1' THEN 'Monday'
    WHEN '2' THEN 'Tuesday'
    WHEN '3' THEN 'Wednesday'
    WHEN '4' THEN 'Thursday'
    WHEN '5' THEN 'Friday'
    WHEN '6' THEN 'Saturday'
  END AS day,
  COUNT(*) AS sessions,
  ROUND(AVG(distance_m / 1000.0), 1) AS avg_km
FROM activities
WHERE type = 'Run'
GROUP BY strftime('%w', date)
ORDER BY sessions DESC;
```

### Intensity Analysis
```sql
-- HR distribution on easy runs
SELECT
  CASE
    WHEN avg_hr < 129 THEN 'Z1 Recovery'
    WHEN avg_hr < 146 THEN 'Z2 Aerobic'
    WHEN avg_hr < 158 THEN 'Z3 Tempo'
    WHEN avg_hr < 172 THEN 'Z4 Threshold'
    ELSE 'Z5 VO2max'
  END AS zone,
  COUNT(*) AS runs,
  ROUND(AVG(distance_m / 1000.0), 1) AS avg_km
FROM activities
WHERE type = 'Run'
  AND date >= date('now', '-8 weeks')
  AND avg_hr IS NOT NULL
GROUP BY zone
ORDER BY avg_hr;

-- Pace vs HR correlation (heat effect)
SELECT
  substr(date, 1, 10) AS date,
  ROUND(avg_pace_per_km / 60.0, 2) AS pace_min_km,
  avg_hr,
  ROUND(avg_temp_c, 0) AS temp_c,
  rpe
FROM activities
WHERE type = 'Run'
  AND date >= date('now', '-8 weeks')
ORDER BY date DESC;
```

---

## Querying training.db — Approach

**Compose queries fresh for each question.** Every question the athlete asks
deserves a query tailored to it — that's the point of having a full-schema
DB and an LLM. The standard queries above are starting points, not a library
of canned answers. Default to ad-hoc.

### Python Skeleton

```python
import sqlite3, sys
from pathlib import Path

athlete = (sys.argv[1] if len(sys.argv) > 1 else "pcc").lower()
db = Path(__file__).resolve().parent.parent / "athletes" / athlete / "training.db"
conn = sqlite3.connect(db)
cur = conn.cursor()

# -- the query for THIS question --
rows = cur.execute("""
    SELECT ...
""").fetchall()
for r in rows:
    print(r)

conn.close()
```

### Gotchas

- Resolve the DB path relative to the script location. Never hardcode absolute paths.
- Some activity types (Workout, Pilates, strength) have NULL `distance` and `moving_time`. Use `COALESCE(..., 0)` in aggregates, or filter by `type = 'Run'` for running only.
- Nested API fields (zone_times, custom_zones, etc.) are stored as JSON text. Use `json_extract(col, '$.path')` in SQLite or deserialise in Python.
- If the question is about streams, intervals/laps, or calendar events, the DB doesn't have those — use MCP tools instead (see SKILL.md Data Tools table).
