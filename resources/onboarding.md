# New Athlete Onboarding Protocol

_Run once only when setting up a new athlete. Not part of regular session flow._

When a new athlete is mentioned and no ATHLETE.md exists for them, run this
protocol before anything else. The goal is to populate ATHLETE.md and AGENTS.md
with enough information to coach them from day one.

---

## 1. Intake Conversation

Have a natural conversation covering these topics. Do not fire all questions at
once -- work through them conversationally, one area at a time. Use the athlete's
answers to follow up intelligently rather than rigidly following the list.

**Identity & Background**
- Full name and preferred name
- Age
- How long have they been running, and how did they get into it?
- Current training frequency (days/week) and typical session distances

**Physical Profile**
- Current weight
- Do they know their LTHR? If not, schedule a field test (30-min time trial,
  avg HR of last 20 minutes = LTHR estimate)
- Resting HR (ideally measured first thing in the morning over a few days)
- Any VO2max estimate from their watch?

**Personal Bests**
- All distances raced: 5K, 10K, HM, marathon, others
- When was each PB set? (recent = usable for VDOT; older = contextual only)
- Were conditions representative (flat course, good day, not a warm-up race)?

**Injury History**
- Any current injuries or niggles, even minor?
- Any recurring issues in the last 12 months?
- Any surgeries, chronic conditions, or clinician instructions affecting training?
- Any movement restrictions or things that reliably cause problems?

**Goals & Motivation**
- Why are they running? What keeps them motivated?
- What is their next race? (date, distance, course profile)
- What is a realistic goal for that race? What would be a stretch goal?
- What is their 12--18 month dream outcome?

**Race Schedule**
- All races planned in the next 6--12 months
- Which is the A race (fully tapered, highest priority)?
- Any B or C races (good efforts / fitness markers)?

**Schedule Preferences, Availability & Lifestyle**
- How many days per week can they realistically run?
- Any soft or hard commitments or running preferences (e.g. long run on Sunday, group runs on certain days, club events)?
- - Any fixed commitments that affect specific days (work, family, other sport)?
- What cross-training is available or already happening?
- How is their sleep generally? How would they rate current life stress (1--10)?
- Any dietary restrictions relevant to fuelling or recovery?

**Training History & Preferences**
- Have they followed a structured plan before? What methodology?
- What has worked well? What has not?
- Highest weekly mileage sustained comfortably?
- Any experience with HR or pace zone training?
- Do they prefer training by HR, pace, or feel (RPE)?
- How do they like to receive feedback -- after every session, weekly, or only
  when something needs attention?

**Technical Setup**
- What watch/device do they train with?
- Does their watch support guided workouts from Intervals.icu?
- Are they already on Intervals.icu? If so, what is their athlete ID?
- If not, they need to create an account and share their athlete ID

---

## 2. Populate the Files

Using answers from the intake conversation:
1. Copy `athletes/sample/ATHLETE_SAMPLE.md` to `athletes/[ATHLETE]/ATHLETE.md`
2. Fill in all fields -- use the inline prompts in the sample file as a guide
3. Calculate VDOT paces from most recent reliable PB using `resources/zones.md`
4. Mark LTHR as unverified if no field test has been done; schedule the test
5. Copy `athletes/sample/AGENTS_SAMPLE.md` to `athletes/[ATHLETE]/AGENTS.md`
6. Fill in Current Status and Decisions Log from the onboarding conversation
7. Add a Next Session Prompt for anything not yet resolved (e.g. LTHR test result)
8. Ask if the athlete maintains any external files (PB records, race calendars,
   competitor lists, pace calculators, checklists, etc.). If so, record the file
   paths and usage context in the "External Files" section of their ATHLETE.md.

---

## 3. Technical Setup

### Environment File
1. Copy `.env.example` to `.env` in the Claude Coach root directory (if not already done)
2. Add the new athlete's Intervals.icu ID: `ATHLETE_ID_[NAME]=iXXXXXX`
   - Find the athlete ID in their Intervals.icu profile URL: `intervals.icu/athlete/iXXXXXX`
3. Ensure `API_KEY` is set — found in Intervals.icu → Settings → API
4. Add the new athlete name to the `ATHLETES` dict in `sync.py`

### Coach Access (only if coaching someone else)
If the person using Claude Coach is coaching a different athlete (not themselves),
the athlete must nominate them as coach in Intervals.icu (Settings → Coach).
This allows the coach's API key to access the athlete's data. If the user is
self-coaching, this step is unnecessary — their own API key already has access.

### Intervals.icu MCP
Ensure the Intervals.icu MCP server is connected in Cowork or Claude Code.
Without it, live data pulls (`get_activities`, `get_events`, `get_wellness_data`)
won't work. The MCP is used for both reading data and pushing workouts to the calendar.

### Initial Data Sync
1. Run `sync.py --athlete [name] --history 730` to pull ~2 years of history into training.db
   - The `--history` flag only matters on the first sync (empty DB). After that,
     sync automatically resumes from the most recent activity date.
2. Pull `get_activities`, `get_events`, and `get_wellness_data` via MCP to review baseline
3. Note current CTL and recent training load in AGENTS.md

---

## 4. Proceed to First Session

With files populated and data pulled, proceed as a normal coaching session:
present your assessment, discuss the first block approach, agree methodology,
and confirm before pushing anything to the calendar.
