# Load Management: CTL, ATL, TSB & Recovery

## Core Concepts

Training load is tracked via three metrics in Intervals.icu:

| Metric | Name | What it means |
|--------|------|--------------|
| CTL | Chronic Training Load (Fitness) | ~42-day rolling average of daily load |
| ATL | Acute Training Load (Fatigue) | ~7-day rolling average of daily load |
| TSB | Training Stress Balance (Form) | CTL − ATL = readiness |

### TSB Ranges

| TSB | State | Implication |
|-----|-------|-------------|
| +15 to +25 | Fresh/peaked | Race ready — may lose fitness if sustained |
| +5 to +15 | Rested | Good for quality sessions, minor events |
| −10 to +5 | Neutral | Normal training state |
| −10 to −30 | Fatigued | Building load, recovery needed soon |
| <−30 | Overreaching | High injury/burnout risk — reduce load immediately |

### ACWR Risk Thresholds

ACWR (Acute:Chronic Workload Ratio) = ATL / CTL. Intervals.icu tracks this
via ATL and CTL — no separate calculation needed.

| ACWR | Zone | Injury risk | Action |
|------|------|-------------|--------|
| <0.8 | Undertraining | Low but losing fitness | Consider increasing load |
| 0.8–1.3 | Sweet spot | ~4–5% | Optimal — continue progression |
| 1.3–1.5 | Caution | ~7–10% | Monitor closely, consider deload next week |
| >1.5 | Danger | 15–20%+ | Reduce load immediately |

Target ACWR by approach:
- Conservative: 0.8–1.2
- Moderate: 0.8–1.3
- Performance: 0.8–1.4 (brief spikes only, not sustained)

### Race Day TSB Targets

| Event | Target TSB | Taper length |
|-------|-----------|--------------|
| 10K | 0 to +10 | 5–7 days |
| Half Marathon | +5 to +15 | 10–14 days |
| Marathon | +10 to +20 | 14–21 days |
| 18km relay | +5 to +15 | 7–10 days |

---

## Critical Rules

### One Variable at a Time
Change only ONE training variable per block: frequency, volume, OR intensity.
Changing multiple simultaneously substantially increases injury risk.

- Weeks 1–4: Increase frequency (3 → 4 days/week), keep volume and intensity constant
- Weeks 5–8: Increase volume 10%/week, keep frequency and intensity constant
- Weeks 9–12: Add one quality session, keep volume and frequency constant

**Never:** New race week + more days + intervals all at once.

### Single-Session Spike Rule
No single run should exceed 110% of the longest run in the past 30 days.
Weekly ACWR can look fine while a single long run spikes dangerously.
Monitor individual session length, not just weekly totals.

Example: If longest run in last 30 days is 16km, next long run cap = 17.6km.

---

## Ramp Rate

How fast CTL is rising week on week.

| Athlete status | Safe ramp rate | Notes |
|----------------|---------------|-------|
| Beginner | +3–5 CTL/week | Conservative, high injury risk if exceeded |
| Intermediate | +5–7 CTL/week | Standard |
| Fit, rebuilding | +7–10 CTL/week | Body remembers faster |
| Post-illness/injury | +2–4 CTL/week | Rebuild slowly |
| Taper | Negative | Normal and expected |

---

## CTL Targets by Goal

| Goal | Target CTL at race week |
|------|------------------------|
| Complete marathon | 40–50 |
| Sub-3:30 marathon | 50–60 |
| Sub-3:00 marathon | 55–70 |
| Sub-2:50 marathon | 65–80 |
| 18km relay at pace | 30–40 |

---

## Weekly Load Targets by Phase

| Phase | % of peak load | Focus |
|-------|---------------|-------|
| Base (early) | 60–70% | Building volume |
| Base (late) | 75–85% | Volume + introducing intensity |
| Build | 90–100% | Peak volume, race-specific work |
| Peak/specific | 85–95% | Maintaining fitness, sharpening |
| Taper | 40–60% | Volume down, intensity maintained |
| Recovery week | 50–60% | Every 3–4 weeks |

---

## Loading Patterns

### 3:1 Loading (Standard)
- 3 weeks progressive load, 1 week recovery (−30–40% volume)
- Standard for most athletes in base/build phase

### 2:1 Loading (Injury-prone or returning)
- More frequent recovery
- Accept slower CTL build in exchange for reduced injury risk

### Recovery Week Structure
| Day | Prescription |
|-----|-------------|
| 1 | Complete rest or 30min Z1 |
| 2 | 45–60min Z2, easy |
| 3 | 30–45min Z2, easy |
| 4 | Rest |
| 5 | 45–60min Z2 + 3–4 short strides |
| 6 | Light session, assess readiness |
| 7 | If feeling good, ease back in |

Volume: −40–50% of normal week. No Z4+ work.

---

## Recovery Monitoring

### Objective Markers
**Resting HR:**
- Elevated 5–10bpm above baseline → accumulated fatigue
- Sustained >3 days → consider extending recovery
- Sudden drop below baseline → potential illness onset

**HRV:**
- Higher = better recovered
- 10%+ below 7-day rolling average → reduce intensity
- Suppressed >3 consecutive days → genuine recovery deficit

### Subjective Indicators (track in wellness)
| Metric | Warning sign |
|--------|-------------|
| Sleep quality | Poor for 2+ nights |
| Energy levels | Low getting up for 3+ days |
| Motivation | Dreading training (not just laziness) |
| Muscle soreness | Unusual localised soreness |
| Appetite | Suppressed (common in overreaching) |

**Warning pattern:** 2+ low scores for 3+ consecutive days → back off regardless of what the plan says.

---

## Post-Illness Return

- Expect 5–7 days of suppressed performance (elevated HR, reduced pace at same effort)
- Run to effort/HR, not to pace — don't chase pre-illness numbers
- ATL spikes quickly on return; CTL lags → TSB looks deceptively good early
- Do not "make up" lost training — just resume the plan

---

## Taper Protocol

### Marathon (3 Weeks)
| Week | Volume | Quality |
|------|--------|---------|
| −3 | −20% | Normal — last long run |
| −2 | −35% | One quality session, race-pace strides |
| −1 | −50% | Easy runs + strides only |

### Shorter Race (e.g. half marathon, relay)
| Week | Volume | Quality                          |
| ---- | ------ | -------------------------------- |
| −2   | −15%   | One race-pace stimulus           |
| −1   | −35%   | Easy + short strides, no quality |

---

## Warning Signs — Act On These

| Signal                             | Threshold               | Action                         |
| ---------------------------------- | ----------------------- | ------------------------------ |
| Resting HR elevated                | >10% above baseline     | Easy day or rest               |
| HRV suppressed                     | >3 consecutive days     | Reduce load                    |
| ATL >> CTL                         | ATL > CTL + 15          | Monitor, reduce if symptomatic |
| Ramp rate exceeded                 | >8 CTL/week             | Back off next week             |
| Injury/muscle awareness increasing | Any step up in symptoms | Reduce load, reassess          |
| 2+ subjective markers low          | 3+ consecutive days     | Back off regardless of plan    |
