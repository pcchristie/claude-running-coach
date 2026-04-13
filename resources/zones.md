# Training Zones & Pace Reference

## HR Zones (Friel 7-Zone, LTHR-based)

Running zones are calculated from LTHR (Lactate Threshold Heart Rate) — the HR
sustainable for ~60 minutes in a race. More accurate than max HR.

| Zone | Name | % of LTHR | Purpose | Feel |
|------|------|-----------|---------|------|
| 1 | Recovery | <81% | Active recovery, warm-up/cool-down | Very easy, talk indefinitely |
| 2 | Aerobic | 81–89% | Base building, fat oxidation | Easy, full sentences |
| 3 | Tempo | 90–93% | Muscular endurance | Moderate, sentences only |
| 4 | Sub-threshold | 94–99% | Lactate tolerance | Hard, few words |
| 5a | Threshold | 100–102% | Threshold development | Very hard, ~60min race effort |
| 5b | VO2max | 103–106% | VO2max stimulus | Extremely hard, 3–8min max |
| 5c | Anaerobic | >106% | Neuromuscular power | Max effort, <3min |

Calculate zone values from the athlete's LTHR (see ATHLETE.md).

---

## Running Pace Zones (Daniels VDOT)

All pace zones derive from a single threshold pace (T) stored in ATHLETE.md.
This value should always match what Intervals.icu has configured, so planned
workouts and analysis reference the same number. Recalculate after every key
race or threshold test.

| Type           | Pace/km (relative to T) | Description                   | Session use                  |
| -------------- | ----------------------- | ----------------------------- | ---------------------------- |
| E (Easy)       | T + 60–70 sec/km        | Daily running, long runs      | 60–70% of volume             |
| M (Marathon)   | T + 15–25 sec/km        | Current marathon-pace work    | Tempo long runs, M-pace reps |
| T (Threshold)  | T                       | Comfortably hard, ~60min race | Cruise intervals, tempo runs |
| I (Interval)   | T − 15–20 sec/km        | Hard reps, ~5min efforts      | VO2max development           |
| R (Repetition) | T − 25–35 sec/km        | Very fast, short reps         | Speed, neuromuscular         |


---

## Field Testing

### Run LTHR Test (30-Minute)
1. Warm up 15min easy (Z1–2)
2. Run 30min at hardest sustainable effort
3. Average HR for the full 30min = LTHR
4. Cool down 10min easy
5. Average pace ≈ lactate threshold pace

Some coaches use the final 20min average to exclude early pacing errors.

### When to Retest
- Every 6–8 weeks during base/build phases
- After recovery weeks (when fresh)
- If perceived effort no longer matches prescribed zones
- After a significant race result (recalculate VDOT)

---

## Heat Adjustment (Hot Climate)

High ambient temperatures (25°C+) inflate HR by approximately 5–10bpm
compared to cool conditions. When assessing zone compliance:
- Allow the upper end of the zone range in heat
- Do not penalise for heat-elevated HR on easy days
- Use RPE alongside HR for intensity assessment in hot conditions
- Hydration status and acclimatisation affect this over time
