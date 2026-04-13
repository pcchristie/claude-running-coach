# Intervals.icu Workout Description Syntax

Reference for writing structured workout descriptions that Intervals.icu
can parse into workout steps and export as a FIT file to Garmin.

---

## How to Push Workouts via MCP

Use `add_or_update_event` with the description-only form of `workout_doc`.
Do NOT use the `steps` array — put the entire workout as text in `description`:

```json
{
  "workout_doc": {
    "description": "Optional free-text note about the session\n\nWarmup\n- 15m 71-79% Pace\n\nMain Set 5x\n- 1km 106-112% Pace\n- 90s 62-68% Pace\n\nCooldown\n- 10m 71-79% Pace"
  }
}
```

The description text IS the workout. Intervals.icu parses it into structured
steps and sends them to the athlete's Garmin as a guided workout.

Using the `steps` array approach is possible but produces inferior rendering
(step names appear after intensity targets, ranges not supported). Avoid it.

### Correct parameter names — get this wrong and the update silently corrupts the event

The `add_or_update_event` MCP tool has a narrow schema and **silently ignores
unknown top-level parameters**:

| Want to set | Correct parameter | Wrong names that FAIL silently |
|---|---|---|
| Event date | `start_date` (YYYY-MM-DD, e.g. `"2026-05-11"`) | `start_date_local`, `date` |
| Workout body | `workout_doc` as `{"description": "..."}` | top-level `description`, `workout_description` |
| Workout name | `name` | `title` |
| Sport | `workout_type` (`"Run"`, `"Ride"`, etc.) | `sport`, `activity_type` |
| Category | **not accepted** — tool always treats it as WORKOUT | `category` |

**Why this matters:** the MCP returns `"Successfully updated event id: X"`
even when your unknown parameters were dropped. And `start_date` **defaults
to today** when omitted — so if you pass `start_date_local` thinking you're
setting the date, the tool ignores it, defaults `start_date` to today, and
**silently moves your event to today's date**. Description ignored, name
ignored. The only signal is a successful-looking response.

**Always re-fetch after updating** with `get_events` filtered to the expected
date range to verify both date and description.

**Minimum call template for an update:**
```
add_or_update_event(
    event_id=<id>,
    athlete_id=<id>,
    start_date="YYYY-MM-DD",
    workout_type="Run",
    name="...",
    workout_doc={"description": "..."}
)
```

---

## Keep a Workout in One Metric (strongly recommended)

**Prescribe every step in the SAME metric family** — all Pace, all HR/LTHR,
or all Power. Mixing is technically valid syntax but Intervals.icu treats the
whole workout as executing in one "primary" metric for downstream calculation,
which breaks several things:

- **Chart display** — the event chart picks one y-axis (bpm OR min/km). Steps in the other metric render as gaps (not zero — missing entirely).
- **Planned load** — only the primary-metric steps contribute to load. Off-metric steps count as zero. Load, intensity %, and fitness-curve impact are all understated.
- **Time in zones** — same thing: off-metric step time shows as unaccounted.
- **Post-activity compliance** — partial comparison between actuals and planned.

Per intervals.icu dev on forum: _"The workout builder allows steps using a combination of power, HR and pace but the whole workout is assumed to be executed using only one of those."_ ([source](https://forum.intervals.icu/t/load-calculations-for-mixed-hr-and-power-planned/115803))

Garmin FIT export and on-watch behaviour is believed to be fine per-step
(each step exports with its own target) but verify in-app before relying on it.

**Practical rule:** prescribe ONE metric family per `workout_doc`. This is a
hard constraint of Intervals.icu — not a style choice. The choice of _which_
metric is informed, in priority order:

1. **Athlete preference (highest priority).** If the athlete has a globally
   applicable preference recorded in `ATHLETE.md` (e.g. "trains to HR only",
   "power meter always", "avoids pace targets on easy runs"), use that metric
   regardless of session type.
2. **Session purpose (default when the above don't settle it).** Pick the
   metric that best matches what the session is trying to achieve. Use
   `resources/workouts.md` as the reference for session types and targets.
   Rough defaults in the absence of other signals: race-specific / tempo /
   interval sessions tend to be prescribed in Pace; aerobic development /
   long / recovery sessions tend to be prescribed in HR. These are
   tendencies, not rules — workouts.md is the source of truth for session
   design. 

Mixing metrics within one workout is OK only as a last resort when conversion
data isn't available; accept the load/chart limitations and document why.

Use the athlete's `ATHLETE.md` Pace Zones table and `resources/zones.md` to
convert between HR % and Pace %.

### Strides — the one accepted exception

Strides (20s fast-but-controlled bursts within an easy run) are the one place
single-metric compliance cannot be cleanly achieved:

- **HR doesn't work**: 20s is too short for HR to respond. `20s 95% LTHR` is physiologically nonsense; the athlete hits the target only after the burst is over.
- **Pace works but mixes metrics**: putting `20s 110-120% Pace` inside an LTHR easy run triggers the mixed-metric penalty (chart gap, load exclusion, zone exclusion) on the stride steps.
- **Free-text (no intensity target) behaves identically to mixed-Pace**: a stride step with only duration + cue text (e.g. `20s Fast stride — controlled, ~90% effort`) renders as a chart gap, contributes zero to planned load, and is excluded from planned time-in-zones, same as a mixed-Pace step would be. Free-text does NOT escape the penalty.

**Canonical pattern for easy + strides sessions**: use the free-text form anyway. Not because it saves load calcs (it doesn't) but because the prescribed target matches reality:

```
- 5km 81-89% LTHR

Strides 4x
- 20s Fast stride — controlled, ~90% effort, not a sprint
- 60s 60-80% LTHR
```

Rationale:
- The easy run and recovery are LTHR-targeted (correct — HR discipline matters on the aerobic portion).
- The stride step has duration + cue only. No fake pace target the athlete won't execute to; no fake HR target that can't be reached in 20s.
- Load cost of excluding strides: ~1–3 TSS per session. Noise-level for a neuromuscular sharpener.
- Planned time-in-zones will show all Z1/Z2 on easy + strides sessions. That is the honest planned aerobic load. Actual time-in-zones post-execution WILL include Z4/Z5 from the strides because Intervals records real HR spikes regardless of the plan.

Document this exception in AGENTS.md if the athlete or context pushes back, but default to this pattern.

---

## Basic Line Format

```
- [cue text] [duration OR distance] [intensity target]
```

- **Cue text** — any text before the first duration/distance; shown on Garmin
- **Duration** — `15m`, `90s`, `1h`, `5m30s`, `5'`, `30"`, `1'30"`
- **Distance** — `1km`, `0.5km`, `10km`, `1mi`
- **Intensity** — see targets below

**CRITICAL: `m` = minutes, NOT meters. Use `km` for distances.**
```
- 15m 71-79% Pace       ← 15 minutes easy   ✓
- 1km 106-112% Pace     ← 1000m hard        ✓
- 1000m 106-112% Pace   ← WRONG, use 1km    ✗
```

---

## Intensity Targets (Running)

**NOTE: If opting for a range (Pace, HR, LTHR etc.) instead of single value, you MUST use a hyphen ("-") NOT an em-dash or en-dash for the range.**

### Pace (recommended for all running steps)
```
- 1km 106-112% Pace        ← range as % of threshold pace
- 15m 71-79% Pace          ← range
- 90s 65% Pace             ← single value
- 2km Z2 Pace              ← zone notation
- 1mi Z4 Pace              ← zone with imperial distance
- 6km 4:28-4:32/km Pace    ← absolute pace (use sparingly)
```
Percentages are relative to **threshold pace** (T-pace = 100%).
Derive pace percentages from current VDOT paces in `ATHLETE.md` and `resources/zones.md`.

### Heart Rate (alternative)
```
- 15m 81-89% LTHR          ← percent of LTHR
- 1mi Z1 HR                ← HR zone
- 10m 90-95% LTHR
```

---

## Section Headers

Section headers have NO `-` prefix. They appear as labels on Garmin.

```
Warmup          ← standard warmup header
Main Set 5x     ← repeat block (5 repetitions)
5x              ← standalone repeat (no label)
Cooldown        ← standard cooldown header
```

Leave a **blank line before and after** every section header and repeat block.

---

## Repeat Blocks

```
Main Set 5x
- 1km 106-112% Pace
- 90s 62-68% Pace

```

Or without a label:
```
5x
- 1km 106-112% Pace
- 90s 62-68% Pace

```

Garmin shows cues like "Main Set 1/5", "Main Set 2/5" etc.
**Nested repeats are not supported.**

---

## Common Running Workout Templates

### Easy / Recovery Run
```
- Easy run 45m Z1-Z2 Pace
```

### Tempo Run (continuous)
```
Warmup
- 15m Z1-Z2 Pace

Tempo
- 20m 95-105% Pace

Cooldown
- 10m Z1 Pace
```

### Cruise Intervals (T-pace)
```
Warmup
- 15m Z1-Z2 Pace

Main Set 4x
- 5m 95-105% Pace
- 1m Z1 Pace

Cooldown
- 10m Z1 Pace
```

### VO2max Intervals (I-pace)
```
Warmup
- 15m Z1-Z2 Pace

Main Set 5x
- 1km 106-112% Pace
- 90s Z1 Pace

Cooldown
- 10m Z1 Pace
```

### Repetitions (R-pace)
```
Warmup
- 15m Z1-Z2 Pace

Main Set 8x
- 0.4km 114-120% Pace
- 2m Z1 Pace

Cooldown
- 10m Z1 Pace
```

### Long Run with Marathon Pace Finish
```
Warmup
- 5km Z1-Z2 Pace

Main Set 2x
- 6km 90-95% Pace
- 2km Z1-Z2 Pace

Cooldown
- 2km Z1 Pace
```

### Ramp Step
```
- 10m ramp 60-85% Pace
```

---

## Ramps
```
- 10m ramp 60-80% Pace      ← pace ramp over 10 minutes
- 10m ramp 50%-75%          ← power ramp (cycling)
```

---

## Formatting Notes

- Blank lines between sections improve readability and are required for correct parsing
- Keywords are case-insensitive (`Warmup` = `warmup`)
- Free text anywhere in a step — everything before the first duration/distance becomes the Garmin cue
- Markdown (`**bold**`, `# Header`, tables) is allowed for display but ignored by the parser
- "Press lap" cues (`Press lap`) can be added as text cues for manual lap triggers
- You must use a hyphen ("-") NOT an em-dash or en-dash for a range (e.g. LTHR range)

---

## Sources

- [Workout Builder Syntax Quick Guide](https://forum.intervals.icu/t/workout-builder-syntax-quick-guide/123701)
- [Intervals.icu Workout Markdown Format Rules](https://forum.intervals.icu/t/intervals-icu-workout-markdown-format-rules/115629)
- Validated 2026-04-06 against live events on athlete calendar
