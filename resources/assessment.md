# Athlete Assessment Guide

## Foundation vs Current Form

These are two different things — always assess both separately.

| Dimension | Timeframe | What it tells you |
|-----------|-----------|------------------|
| Athletic Foundation | Lifetime / 2+ years | True capability, training history, race experience |
| Current Form | Last 8–12 weeks | Starting point for the plan right now |

**Why it matters:** An athlete who ran a 3:06 marathon 8 months ago but has been
managing injuries is NOT a beginner. They have aerobic adaptation, movement
efficiency, mental toughness, and race experience. Their plan should focus on
rebuilding (faster progression possible) rather than building from scratch.

However: cardiovascular fitness rebuilds faster than tendons and connective
tissue. Never let "it feels easy" drive volume beyond what tissue can handle.

---

## Foundation vs Form Scenarios

| Scenario | Foundation | Current Form | Approach |
|----------|------------|--------------|----------|
| Marathon PB last year, injury since | Very strong | Low | Rebuild: faster progression OK |
| Consistent easy running, no races | Moderate | Moderate | Build specificity, add quality |
| Recent high fitness, life interruption | Strong | Moderate | Rebuild: body remembers |
| New to structured training | Low | Moderate | Conservative, everything is new |

---

## Interpreting Training Data

### Strength Signals
| Signal | Interpretation |
|--------|---------------|
| Long sessions at low HR | Excellent aerobic base |
| Low load per minute of training | Sport feels easy (strength) |
| High load per minute | Sport is hard (limiter) |
| Historical peaks >> recent activity | Dormant fitness, will return quickly |
| Recent activity well below historical | Rebuilding, not beginner |

### Limiter Identification
Compare average HR and RPE across session types. The sessions with disproportionately high HR or RPE for the distance/duration are the limiters.

For this athlete: running pace vs HR is the key indicator. Reference the
intensity analysis query in queries.md to check zone distribution.

---

## Validation Protocol

**Before writing any plan or pushing to calendar, present your assessment
and validate with the athlete. Never finalise without their confirmation.**

### What to Cover

1. **Foundation summary** — "Based on your history, here's what I see..."
2. **Current form** — "Right now, your data shows..."
3. **Strengths** — what the data says they're good at
4. **Limiters** — where the gap is
5. **Proposed approach** — what you're recommending and why
6. **Open questions** — injuries, constraints, goals, preferences

### Questions to Ask (as relevant)

- "Does this assessment match your own perception?"
- "Was the reduced training due to injury or life circumstances?" (affects progression rate)
- "Any injuries or constraints I should factor in?"
- "Do you have a specific time goal or is the primary focus just completing it well?"
- "Which days work best for the long run and quality sessions?"
- "Anything you love or hate about certain session types?"

### Example Validation Dialogue

```
Based on your data, here's my assessment:

Strengths:
- Aerobic base is solid — your easy runs show consistent Z2 HR for 
  60–75min sessions with low RPE
- Marathon experience — you've done the distance, you know how to race it

Limiters:
- Current CTL is significantly below what sub-3 marathon requires (55–70) — see ATHLETE.md
- Pace at threshold is slower than it will need to be — this is the main gap
- Calf requires careful load management throughout

Current plan approach:
- [Summarise block structure and priorities based on race calendar]

Before I push anything to the calendar:
1. Does this match your understanding of where you're at?
2. Any constraints on training days or volume I should know about?
3. How is the calf feeling right now — stable, improving, or worse?
```

---

## Reading Historical Data (Cowork/DB)

Use queries.md to pull:
- Peak CTL ever recorded (shows true capacity)
- Peak weekly volume (shows training ceiling)
- Preferred training days (infer from long run day patterns)
- Zone distribution (check 80/20 compliance)
- Load trend over last 8–12 weeks (foundation vs form gap)

### Inferring Long Run Day Preference
```sql
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
  COUNT(*) AS long_runs,
  ROUND(AVG(distance_m / 1000.0), 1) AS avg_km
FROM activities
WHERE type = 'Run'
  AND moving_time_s > 3600
GROUP BY strftime('%w', date)
ORDER BY long_runs DESC;
```

Use this before asking — suggest the pattern you see rather than asking from scratch.

---

## Why Validation Matters

- Data can mislead: low recent volume ≠ low ability
- Athletes know their bodies: prior injuries, burnout triggers, what they enjoy
- Buy-in matters: athletes follow plans they helped shape
- Context changes everything: "slow" runs might be deliberate, injury-related, or heat-affected

**Never push a plan to Intervals without explicit athlete confirmation.**
