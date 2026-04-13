# Claude Running Coach

An AI running coach powered by Claude, grounded in your live Intervals.icu
training data. It tracks your fitness, plans workouts, manages injuries, and
pushes structured sessions directly to your Garmin via Intervals.icu.

## Overview 

This skill is designed a little differently to most skills. Whereas most skills are designed to be one large directory installed installed to the AppData folder and never looked at again, this is designed with two components:
1. A Claude Skill to drive the behaviour of Claude.
2. A shared working directory to act as the documentation and source of truth for Claude Coach - readable and writeable by the User.

As such, you install the .skill file as you would any other skill but maintain a Working Directory somewhere else on your machine. Both user and Claude continually update many of these documents as you progress.

Because of this it is recommended to use a suitable App to maintain your Claude Coach folder (i.e. one that makes it easy to navigate, read and write your suite of .md files). I use Obsidian but Claude Code, VS Code or any IDE works, too.

### Shared Working Directory Components

Your Shared Working Directory breaks down the following way.
1. /Athletes folder. Your Athlete folder contains two files: 
   1. ATHLETE.md contains information about you relevant to Claude Coach (physiological, training history, goals, injuries, preferences, etc.).
   2. AGENTS.md is the Coaching Plan itself (history, present, future). 
2. Resources files containing a summary of knowledge for Claude Coach to draw upon. These contain information about
   1. Running knowledge: Training, plans, workouts, load management etc. 
   2. Technical information to help Claude Coach do its job - the formatting required for Intervals.icu workouts to work properly, and sql queries to answer questions.
3. Scripts to enable Claude Coach to work (i.e. pull data from Intervals, store your access key). 

You would expect to be reading/writing to #1 fairly often, #2 occasionally, and #3 only on setup.

Note that you can manage multiple athletes by having one folder per athlete sitting under /athletes (though the primary user will need to have Coaching rights to the other Athletes in Intervals.icu)

## What's in this folder

```
claude-running-coach/
├── running-coach.skill    ← Install this in Claude (Cowork or Claude Code)
├── SKILL.md               ← The coaching instructions (reference copy)
├── resources/             ← Shared coaching frameworks (periodization, load management, etc.)
├── athletes/sample/       ← Templates for setting up your athlete profile
├── sync.py                ← Syncs Intervals.icu data to a local SQLite DB
├── run_sync.bat           ← Windows convenience script for sync.py
└── .env                   ← Template for API keys and athlete IDs (edit in place)
```

## Requirements

- Claude Desktop (Cowork) or Claude Code
- [**Intervals.icu MCP server**](https://github.com/mvilanova/intervals-mcp-server) — this is what lets Claude read your training
  data, push workouts to your calendar and perform analysis. Install it in Cowork (Settings →
  Connectors) or Claude Code (MCP config). Without it, the skill can't
  access Intervals.icu at all. Claude can help you install & configure it.
- Intervals.icu account (free tier works)
- Python 3 with `requests` and `python-dotenv` packages
- Strongly recommended: A Garmin or other device that syncs to Intervals.icu

## Setup

### 1. Install the Intervals.icu MCP server

The skill relies on the [Intervals.icu MCP server](https://github.com/mvilanova/intervals-mcp-server) for all live data access
(pulling activities, wellness data, calendar events) and for pushing
workouts to your calendar. Install it before anything else:

- **Cowork:** Settings → Connectors → search for "Intervals.icu" → Connect
- **Claude Code:** Add the Intervals.icu MCP server to your MCP config

As part of this you will need to fetch your Athlete ID and API Key from Intervals.icu. These are available at the bottom of the Settings page and should be entered into the .env file in the directory (you may need to Enable Hidden Files/Folders in your File Explorer to see this file).

Verify it's working by asking Claude to pull your recent activities.

### 2. Install the skill

Open the `running-coach.skill` file in Cowork or Claude Code. Click "Save skill"
to install it. This gives Claude the coaching instructions and triggers.

### 3. Set up your workspace

Copy this entire folder somewhere on your machine (e.g. your Documents folder,
an Obsidian vault, wherever you keep project files). This becomes your
"Claude Coach" workspace — open it as your project/workspace in Cowork or
Claude Code.

### 4. Configure Intervals.icu credentials

Open `.env` in the project folder and fill in:

1. **API key** — from Intervals.icu → Settings → API. Set `API_KEY=...`.
2. **Athlete IDs** — find yours in your profile URL (`intervals.icu/athlete/iXXXXXX`).
   Each athlete gets a line like `ATHLETE_ID_<NAME>=i123456`. The `<NAME>`
   part is whatever you want — it becomes the `--athlete` flag value.
   Add as many athletes as you need, delete the unused placeholder lines.
3. **Default athlete (optional)** — set `ATHLETE_ID=i123456` to the athlete
   ID the Intervals.icu MCP should use as a fallback when `athlete_id` is
   not passed explicitly. Usually your own ID.

Example:
```
API_KEY=abc123...
ATHLETE_ID_ME=i123456
ATHLETE_ID_ALEX=i789012
ATHLETE_ID=i123456
```

### 5. Run your first sync

If you configured one athlete:
```
python sync.py --history 730
```

If you configured several, specify which one:
```
python sync.py --athlete me --history 730
```

(The `--athlete` value is case-insensitive and must match the `<NAME>`
part of an `ATHLETE_ID_<NAME>` line in your `.env`.)

This pulls ~2 years of training history into a local SQLite database at
`athletes/<name>/training.db`. The `--history` flag is only needed on the
first run. After that, sync automatically resumes from your most recent
activity — no flags needed.

On Windows you can also double-click `run_sync.bat`, or run it from any
shell: `run_sync.bat --athlete me`.

### 6. Start coaching

Open your Claude Coach folder in Cowork or Claude Code and start talking
about your training. The skill triggers automatically when you mention
running, races, workouts, injuries, or fitness.

On your first session, Claude will run through an onboarding conversation
to set up your athlete profile — covering your background, goals, PBs,
injuries, and preferences. See `resources/onboarding.md` for the full protocol.

## If you're being coached by someone else

If a friend is coaching you through Claude (rather than self-coaching), they
need coach access to your Intervals.icu data. Go to Intervals.icu →
Settings → Coach and nominate their account. Their API key will then
work for your data too.

## Thank You
Leveraging the great work done by 

* [ColinEberhardt](https://github.com/ColinEberhardt/claude-coach)
* [LightAxe](https://github.com/LightAxe/claude-running-coach)
* [felixrieseberg](https://github.com/felixrieseberg/claude-coach)