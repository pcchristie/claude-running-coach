# ATHLETE.md — [Full Name] ([ATHLETE])

_Stable profile — update only when facts change: new PB, metric update, injury
status change, new race added. Do not record training decisions or session notes here._

---

## Intervals.icu

| Field | Value |
|-------|-------|
| Athlete ID | iXXXXXX |

---

## Biometrics

_Ask: current weight, do they know their LTHR (or schedule a test), resting HR
(best measured first thing in the morning over several days), any VO2max reading
from their watch._

| Metric | Value |
|--------|-------|
| Weight | ~XXkg |
| LTHR | XXX bpm (verified / unverified — test scheduled YYYY-MM-DD) |
| VO2max | XX ml/kg/min (Garmin estimate) |
| Resting HR baseline | XX–XX bpm |

---

## Personal Bests

_Ask for all distances run. Note whether PBs are recent (within 12 months = usable
for VDOT/pace zone calculations) or older (contextual only — fitness may have changed)._

| Event | Time | Date | Course/Notes |
|-------|------|------|--------------|
| 5K | — | — | — |
| 10K | — | — | — |
| Half Marathon | — | — | — |
| Marathon | — | — | — |

---

## Threshold Pace

_Single value — this is the seed for all Daniels VDOT paces below. Keep it
in sync with the threshold pace stored in Intervals.icu so planned workouts
and analysis use the same reference._

| Metric | Value | Last updated | Next review |
|--------|-------|--------------|-------------|
| Threshold pace | X:XX/km | YYYY-MM-DD (source: race / test / estimate) | After [next key race or test] |
| LTHR | XXX bpm | YYYY-MM-DD (source: field test / lab / Garmin) | After [next test opportunity] |

### Daniels VDOT Paces
_Derived from threshold pace above using `resources/zones.md`. Recalculate
whenever threshold changes. Mark as ESTIMATE if based on speculative
threshold rather than tested data._

| Type | Pace/km | Use |
|------|---------|-----|
| E (Easy) | X:XX–X:XX | Daily easy running |
| M (Marathon) | X:XX–X:XX | Marathon-pace work |
| T (Threshold) | X:XX | Comfortably hard, ~60min race effort |
| I (Interval) | X:XX–X:XX | Hard reps, ~5 min efforts |
| R (Repetition) | X:XX–X:XX | Short fast reps, full recovery |

---

## Race Schedule

_Ask: next planned race (date, distance, location/course profile), any other races
in the next 6–12 months. Establish which is the A race (fully tapered, priority)
vs B races (good effort, may not taper fully) vs C races (fitness markers, run through)._

| Race | Date | Distance | Target | Priority |
|------|------|----------|--------|----------|
| — | — | — | — | A/B/C |

---

## Training Setup

Are they already on Intervals.icu or do they need to be set up?_

- Platform: Intervals.icu (calendar = single source of truth)
- Location: [City] — note local climate factors (heat, elevation)

### Fixed Weekly Commitments

_Ask: what days/times are non-negotiable? Work shifts, family, other sport/classes,
social commitments that affect training days. Also ask about preferred training time
(morning, evening, lunch) and any days they simply cannot run._

| Day | Commitment | Notes |
|-----|-----------|-------|
| — | — | — |

### Preferred Running Days

_Ask which days they prefer to run and how many days per week is realistic._

| Day | Availability | Notes |
|-----|-------------|-------|
| Monday | — | — |
| Tuesday | — | — |
| Wednesday | — | — |
| Thursday | — | — |
| Friday | — | — |
| Saturday | — | — |
| Sunday | — | — |

---

## Injuries & Constraints

_Ask: any current injuries or niggles (even minor)? Any recurring issues in the
last 12 months? Any surgeries, chronic conditions, or movement restrictions?
Any clinician instructions (physio, GP) that affect training?_

| Issue | Status | Management |
|-------|--------|------------|
| — | — | — |

**Notes:**
- [Any constraints that affect session design — e.g. no back-to-back hard days,
  avoid downhill running, needs warm-up time etc.]

---

## Training Background

_Ask: how long have they been running? Have they followed a structured plan before?
What has worked / not worked? Highest weekly mileage they have sustained comfortably?
Any experience with HR or pace zone training?_

- Running experience: [X years, brief background]
- Peak sustained mileage: [~Xkm/week]
- Zone training experience: [None / some / experienced]

---

## Lifestyle Factors

_Ask: how is their sleep generally? How would they rate current life stress (1–10)?
Do they do other sport or exercise (gym, Pilates, cycling, etc.)? Any dietary
restrictions relevant to fuelling long runs or recovery?_

- Sleep: [generally good / variable / poor]
- Life stress: [low / moderate / high]
- Cross-training: [type and frequency]
- Nutrition notes: [any restrictions or relevant habits]

---

## Coaching Preferences

_Ask: do they prefer to train by HR, pace, or feel (RPE)? How do they like to
receive feedback — after every session, weekly summary, only when something is wrong?
Are they data-driven or do they prefer simple instructions? What style of feedback do they like? Firm, soft, in between?_

- Intensity preference: [HR / Pace / RPE]
- Feedback preference: [weekly / post-session / as needed]
- Data engagement: [high / moderate / low]
- Feedback style: [firm / soft / in-between]

---

## External Files

_Ask: do they maintain any files outside of Claude Coach that are relevant to
coaching? E.g. PB records, race calendars, competitor lists, pace calculators,
checklists, training logs. Record paths and when to reference them._

| File | Path | Format | When to read |
|------|------|--------|--------------|
| — | — | — | — |
