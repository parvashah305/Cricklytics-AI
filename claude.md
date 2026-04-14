# Cricklytics AI — Cursor Project Intelligence

> Real-Time Cricket Intelligence Platform
> Stack: Kafka → PySpark → MongoDB/Redis → Node.js → React
> This file is the single source of truth for every code decision in this project.

---

## Project Overview

Cricklytics AI is a production-grade Big Data streaming platform that processes live cricket match data ball-by-ball and generates advanced analytics in real time. It is NOT a basic score app. Every architectural decision must prioritize low latency, modularity, and scalability.

**Core pipeline:**
```
Cricket API → Kafka Producer → Kafka Topic → Spark Structured Streaming → MongoDB + Redis → Node.js API + Socket.IO → React Dashboard
```

---

## Directory Structure

```
cricklytics-ai/
├── producer/                        # Python Kafka producer
│   ├── main.py                      # Entry point — polls API, publishes events
│   ├── cricket_client.py            # Cricbuzz/RapidAPI HTTP client
│   ├── kafka_publisher.py           # Kafka producer logic
│   ├── schemas/
│   │   └── ball_event.avsc          # Avro schema for ball events
│   └── config.py                    # Config loader
│
├── spark-jobs/                      # PySpark streaming jobs
│   ├── main_stream.py               # Entry point — reads from Kafka, writes to MongoDB
│   ├── analytics/
│   │   ├── pressure_index.py        # Pressure Index computation
│   │   ├── win_probability.py       # Win probability model
│   │   ├── momentum.py              # Momentum shift detector
│   │   ├── player_impact.py         # Player Impact Score
│   │   └── commentary.py           # Rule-based commentary generator
│   ├── ml/
│   │   └── score_projector.py       # Spark MLlib score projection
│   ├── utils/
│   │   └── spark_session.py         # SparkSession factory
│   └── config.py
│
├── backend/                         # Node.js + Express + Socket.IO
│   ├── src/
│   │   ├── app.js                   # Express app setup
│   │   ├── server.js                # HTTP + Socket.IO server entry
│   │   ├── routes/
│   │   │   ├── matches.js           # Match state endpoints
│   │   │   ├── analytics.js         # Analytics endpoints
│   │   │   ├── players.js           # Player data endpoints
│   │   │   └── simulator.js         # What-If simulator endpoints
│   │   ├── controllers/
│   │   │   ├── matchController.js
│   │   │   ├── analyticsController.js
│   │   │   └── simulatorController.js
│   │   ├── models/
│   │   │   ├── Match.js             # Mongoose schema
│   │   │   ├── BallEvent.js
│   │   │   ├── Analytics.js
│   │   │   └── Player.js
│   │   ├── services/
│   │   │   ├── redisService.js      # Redis cache reads/writes
│   │   │   ├── socketService.js     # Socket.IO event emitters
│   │   │   └── mongoService.js      # MongoDB query helpers
│   │   ├── middleware/
│   │   │   ├── errorHandler.js
│   │   │   ├── rateLimiter.js
│   │   │   └── logger.js
│   │   └── config/
│   │       └── index.js
│   └── package.json
│
├── frontend/                        # React + Vite dashboard
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── store/                   # Redux Toolkit slices
│   │   │   ├── index.js
│   │   │   ├── matchSlice.js
│   │   │   ├── analyticsSlice.js
│   │   │   └── playerSlice.js
│   │   ├── hooks/
│   │   │   ├── useSocket.js         # Socket.IO connection hook
│   │   │   ├── useLiveMatch.js
│   │   │   └── useAnalytics.js
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   └── PageLayout.jsx
│   │   │   ├── scorecard/
│   │   │   │   ├── LiveScorecard.jsx
│   │   │   │   ├── BallTimeline.jsx
│   │   │   │   └── OverSummary.jsx
│   │   │   ├── analytics/
│   │   │   │   ├── WinProbabilityChart.jsx
│   │   │   │   ├── PressureGauge.jsx
│   │   │   │   ├── MomentumChart.jsx
│   │   │   │   ├── RunRateChart.jsx
│   │   │   │   └── PlayerImpactCard.jsx
│   │   │   ├── visualizers/
│   │   │   │   ├── WagonWheel.jsx   # D3.js shot direction plot
│   │   │   │   └── HeatmapField.jsx # D3.js batsman vulnerability
│   │   │   ├── commentary/
│   │   │   │   └── SmartCommentary.jsx
│   │   │   ├── simulator/
│   │   │   │   └── WhatIfSimulator.jsx
│   │   │   └── ui/                  # Reusable design system components
│   │   │       ├── GlowCard.jsx
│   │   │       ├── PulseIndicator.jsx
│   │   │       ├── AnimatedNumber.jsx
│   │   │       └── LiveBadge.jsx
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── MatchDetail.jsx
│   │   │   ├── PlayerProfile.jsx
│   │   │   └── Simulator.jsx
│   │   ├── styles/
│   │   │   ├── globals.css          # CSS variables, reset, base
│   │   │   ├── theme.css            # Full design token system
│   │   │   └── animations.css       # All keyframes
│   │   └── utils/
│   │       ├── formatters.js
│   │       └── calculations.js
│   ├── index.html
│   └── vite.config.js
│
├── docker/
│   ├── docker-compose.yml           # Full local stack
│   ├── kafka/
│   │   └── Dockerfile
│   ├── spark/
│   │   └── Dockerfile
│   └── nginx/
│       └── nginx.conf
│
├── scripts/
│   ├── seed_mock_data.py            # Seed MongoDB with mock match history
│   └── test_pipeline.sh             # End-to-end pipeline smoke test
│
├── .env.example
├── .cursorrules                     # See bottom of this file
└── README.md
```

---

## Language & Runtime Rules

| Layer | Language | Runtime |
|---|---|---|
| Kafka Producer | Python 3.11+ | venv |
| Spark Jobs | Python 3.11+ (PySpark 3.5) | venv |
| Backend | JavaScript (ES Modules) | Node.js 20 LTS |
| Frontend | JavaScript + JSX | Node.js 20 LTS / Vite |

- Always use `async/await` — never raw `.then()` chains in Node.js
- Always use `f-strings` in Python — never `%` or `.format()`
- Never use `var` in JavaScript — always `const` / `let`
- All Python files must have type hints on function signatures
- All Node.js modules use ES module syntax (`import/export`), not CommonJS

---

## Environment Variables

Store all secrets in `.env`. Never hardcode. Load with `python-dotenv` in Python and `dotenv` in Node.

```env
# Cricket API
RAPIDAPI_KEY=
RAPIDAPI_HOST=cricbuzz-cricket.p.rapidapi.com

# Kafka
KAFKA_BROKER=localhost:9092
KAFKA_TOPIC_BALL_EVENTS=cricket.ball.events
KAFKA_TOPIC_ANALYTICS=cricket.analytics
KAFKA_GROUP_ID=cricklytics-spark

# MongoDB
MONGO_URI=mongodb://localhost:27017/cricklytics

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_TTL=30

# Backend
PORT=4000
NODE_ENV=development

# Spark
SPARK_MASTER=local[*]
SPARK_APP_NAME=CricklyticsStream
```

---

## Kafka Architecture

### Topic Design
```
cricket.ball.events     — raw ball-by-ball events from API
cricket.analytics       — computed analytics output from Spark
cricket.alerts          — momentum shifts, wickets, milestones
```

### Partitioning Strategy
- Partition by `match_id` — all events for a match land on the same partition
- This guarantees ordered processing per match in Spark

### Ball Event Schema (Avro)
```json
{
  "type": "record",
  "name": "BallEvent",
  "fields": [
    { "name": "match_id",       "type": "string" },
    { "name": "innings",        "type": "int" },
    { "name": "over",           "type": "float" },
    { "name": "ball",           "type": "int" },
    { "name": "batsman",        "type": "string" },
    { "name": "bowler",         "type": "string" },
    { "name": "runs",           "type": "int" },
    { "name": "is_wicket",      "type": "boolean" },
    { "name": "is_boundary",    "type": "boolean" },
    { "name": "is_dot",         "type": "boolean" },
    { "name": "delivery_type",  "type": "string" },
    { "name": "timestamp",      "type": "long" }
  ]
}
```

### Producer Pattern
```python
# Always produce with match_id as the key for consistent partitioning
producer.produce(
    topic=KAFKA_TOPIC_BALL_EVENTS,
    key=event["match_id"],
    value=json.dumps(event).encode("utf-8"),
    callback=delivery_report
)
producer.flush()
```

---

## Spark Streaming Rules

- Always use **Spark Structured Streaming** — never DStream (legacy)
- Read from Kafka using `readStream` with `startingOffsets = "latest"` for live mode
- Use `foreachBatch` to write to MongoDB — never use direct stream sinks for Mongo
- Watermarking: use `withWatermark("timestamp", "10 seconds")` on all aggregations
- Trigger interval: `Trigger.ProcessingTime("2 seconds")` for near-real-time feel
- Checkpoint location: always set — required for fault tolerance

```python
# Standard Spark ↔ Kafka read pattern
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC_BALL_EVENTS) \
    .option("startingOffsets", "latest") \
    .load()
```

### Analytics Computation Rules

**Pressure Index formula:**
```
pressure = (
    (required_run_rate / current_run_rate) * 0.4 +
    (dot_ball_percentage / 100) * 0.3 +
    (wickets_fallen / total_wickets) * 0.3
) * 100
```
Clamp result to [0, 100]. Store as float with 2 decimal places.

**Win Probability:**
- Use historical match data to seed the model
- Update after every ball using current runs, wickets, overs remaining, required rate
- Output as float [0.0, 1.0] — frontend converts to percentage

**Momentum Shift Detection triggers:**
- 3 or more boundaries in an over
- 2 or more wickets in 5 balls
- 6 or more dot balls in an over
- Required run rate crosses 12

**Player Impact Score formula:**
```
batting_impact = (runs_scored / balls_faced) * strike_rate_weight + boundary_bonus
bowling_impact = wickets_taken * wicket_weight - (economy - 6) * economy_weight
impact = (batting_impact + bowling_impact) * match_context_multiplier
```
Match context multiplier increases in death overs and high-pressure situations.

---

## MongoDB Schema

### Collections

**matches**
```javascript
{
  _id: ObjectId,
  match_id: String,          // unique, indexed
  teams: { home: String, away: String },
  format: String,            // T20 | ODI | Test
  venue: String,
  status: String,            // live | completed | upcoming
  current_innings: Number,
  scorecard: {
    innings1: { runs: Number, wickets: Number, overs: Number },
    innings2: { runs: Number, wickets: Number, overs: Number }
  },
  created_at: Date,
  updated_at: Date
}
```

**ball_events**
```javascript
{
  _id: ObjectId,
  match_id: String,          // indexed
  innings: Number,
  over: Number,
  ball: Number,
  batsman: String,
  bowler: String,
  runs: Number,
  is_wicket: Boolean,
  is_boundary: Boolean,
  is_dot: Boolean,
  timestamp: Date
}
```

**analytics** (updated every ball by Spark)
```javascript
{
  _id: ObjectId,
  match_id: String,          // unique, indexed
  pressure_index: Number,
  win_probability: { home: Number, away: Number },
  current_run_rate: Number,
  required_run_rate: Number,
  momentum_state: String,    // rising | falling | stable | shift
  projected_score: Number,
  commentary: String,
  last_updated: Date
}
```

**players**
```javascript
{
  _id: ObjectId,
  player_id: String,
  name: String,
  team: String,
  impact_score: Number,
  match_id: String,
  stats: {
    runs: Number, balls: Number, fours: Number, sixes: Number,
    wickets: Number, economy: Number, dot_balls: Number
  }
}
```

### Indexing Rules
- Always index `match_id` on every collection
- Compound index on `ball_events`: `{ match_id: 1, innings: 1, over: 1, ball: 1 }`
- TTL index on `analytics` is NOT set — we want full history

---

## Backend API Design

### REST Endpoints

```
GET  /api/matches                     — list all live matches
GET  /api/matches/:id                 — single match full state
GET  /api/matches/:id/scorecard       — scorecard only
GET  /api/matches/:id/analytics       — latest analytics snapshot
GET  /api/matches/:id/balls           — ball-by-ball history
GET  /api/players/:matchId            — all players for a match
GET  /api/players/:playerId/impact    — player impact score
POST /api/simulator/whatif            — what-if scenario input → recalculated analytics
```

### Response envelope — always use this shape:
```javascript
{
  success: true,
  data: { ... },
  meta: { timestamp: Date, match_id: String }
}
```

Error shape:
```javascript
{
  success: false,
  error: { code: String, message: String }
}
```

### Redis Caching Strategy
- Cache `analytics` per `match_id` with TTL of 30 seconds
- Cache `scorecard` per `match_id` with TTL of 5 seconds
- On cache miss → query MongoDB → write back to Redis → return
- On Spark write → always invalidate Redis key for that `match_id`

### Socket.IO Events

**Server → Client (emitted after every ball):**
```javascript
socket.emit("ball:update",     { match_id, ball_event })
socket.emit("analytics:update",{ match_id, analytics })
socket.emit("commentary:new",  { match_id, text, type })
socket.emit("momentum:shift",  { match_id, direction, trigger })
socket.emit("milestone",       { match_id, type, player, value })
```

**Client → Server:**
```javascript
socket.emit("match:subscribe",   { match_id })
socket.emit("match:unsubscribe", { match_id })
```

Rooms: each match gets its own Socket.IO room named `match:{match_id}`.

---

## Frontend Architecture

### State Management (Redux Toolkit)

```javascript
// store slices
matchSlice     — { liveMatches, activeMatch, scorecard, ballHistory }
analyticsSlice — { pressureIndex, winProbability, momentum, runRate, commentary }
playerSlice    — { players, impactScores }
uiSlice        — { isConnected, activeTab, isSimulatorOpen }
```

### Socket Hook Pattern
```javascript
// hooks/useSocket.js — always use this, never raw socket in components
const { isConnected, subscribe, unsubscribe } = useSocket()

// hooks/useLiveMatch.js — combines socket + redux dispatch
const { match, analytics, ballHistory } = useLiveMatch(matchId)
```

### Chart Update Rule
- All Recharts components must use `isAnimationActive={false}` for live data
- Only animate on initial mount, not on every ball update — prevents flickering
- D3 visualizers must use `.transition().duration(300)` for smooth updates

---

## UI Design System — "Dark Pitch" Theme

This is the most important section for frontend work. Every UI decision must follow this system.

### Concept
**"Dark Pitch"** — A premium dark cricket analytics dashboard inspired by the look of a floodlit stadium at night. Deep obsidian backgrounds, electric green accents (the pitch), amber warning tones (pressure), and ice-blue data overlays. The feel is: Bloomberg Terminal meets ESPN CricInfo, but cinematic.

### Font Stack
```css
--font-display: 'Bebas Neue', cursive;        /* Scorecard numbers, big stats */
--font-heading: 'Barlow Condensed', sans-serif; /* Section headers, labels */
--font-body: 'DM Sans', sans-serif;            /* Body text, commentary */
--font-mono: 'JetBrains Mono', monospace;      /* Ball-by-ball data, over grids */
```
Import from Google Fonts. These are NON-NEGOTIABLE — do not substitute with Inter, Roboto, or system fonts.

### Color Tokens
```css
:root {
  /* Backgrounds — layered depth */
  --bg-void:        #050508;   /* Outermost page background */
  --bg-base:        #0a0b12;   /* Main surface */
  --bg-surface:     #10121e;   /* Cards, panels */
  --bg-elevated:    #181b2d;   /* Hover states, modals */
  --bg-overlay:     #1f2338;   /* Tooltips, popovers */

  /* Pitch Green — primary accent */
  --green-dim:      #0d3320;
  --green-muted:    #1a5c38;
  --green-base:     #22c55e;   /* Primary action color */
  --green-bright:   #4ade80;   /* Highlights, active states */
  --green-glow:     rgba(34, 197, 94, 0.15);  /* Glow effects */

  /* Amber — pressure / warning */
  --amber-dim:      #3d2200;
  --amber-muted:    #92400e;
  --amber-base:     #f59e0b;
  --amber-bright:   #fbbf24;
  --amber-glow:     rgba(245, 158, 11, 0.15);

  /* Ice Blue — data / analytics */
  --blue-dim:       #0c1a3d;
  --blue-muted:     #1e40af;
  --blue-base:      #3b82f6;
  --blue-bright:    #60a5fa;
  --blue-glow:      rgba(59, 130, 246, 0.15);

  /* Coral Red — wickets / danger */
  --red-base:       #ef4444;
  --red-bright:     #f87171;
  --red-glow:       rgba(239, 68, 68, 0.15);

  /* Text hierarchy */
  --text-primary:   #f0f2ff;
  --text-secondary: #8b90a8;
  --text-muted:     #4a4f6a;
  --text-inverse:   #050508;

  /* Borders */
  --border-subtle:  rgba(255,255,255,0.04);
  --border-soft:    rgba(255,255,255,0.08);
  --border-base:    rgba(255,255,255,0.12);
  --border-accent:  rgba(34, 197, 94, 0.3);

  /* Glows and shadows */
  --shadow-card:    0 4px 24px rgba(0,0,0,0.4), 0 1px 4px rgba(0,0,0,0.3);
  --shadow-glow-green: 0 0 20px rgba(34, 197, 94, 0.25), 0 0 60px rgba(34, 197, 94, 0.08);
  --shadow-glow-amber: 0 0 20px rgba(245, 158, 11, 0.25);
  --shadow-glow-blue:  0 0 20px rgba(59, 130, 246, 0.25);

  /* Spacing system */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;

  /* Border radius */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-xl: 24px;

  /* Transitions */
  --transition-fast:   150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base:   250ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow:   400ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-spring: 500ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### Core Component Patterns

**GlowCard** — primary container for all analytics panels:
```css
.glow-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  transition: border-color var(--transition-base), box-shadow var(--transition-base);
}
.glow-card:hover {
  border-color: var(--border-accent);
  box-shadow: var(--shadow-card), var(--shadow-glow-green);
}
```

**LiveBadge** — pulsing live indicator:
```css
.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.3);
  border-radius: 999px;
  padding: 3px 10px;
  font-family: var(--font-heading);
  font-size: 11px;
  letter-spacing: 0.1em;
  color: var(--green-bright);
  text-transform: uppercase;
}
.live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--green-base);
  animation: live-pulse 1.5s ease-in-out infinite;
}
@keyframes live-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.8); }
}
```

**Stat number display** — all big numbers on dashboard:
```css
.stat-value {
  font-family: var(--font-display);
  font-size: clamp(36px, 5vw, 64px);
  line-height: 1;
  letter-spacing: 0.02em;
  color: var(--text-primary);
}
.stat-label {
  font-family: var(--font-heading);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-top: 4px;
}
```

**Ball timeline chips:**
```css
.ball-chip {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 600;
  border: 1px solid var(--border-soft);
  background: var(--bg-elevated);
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}
.ball-chip.boundary { background: var(--green-dim);  border-color: var(--green-muted); color: var(--green-bright); }
.ball-chip.six      { background: var(--green-dim);  border-color: var(--green-base);  color: var(--green-base); box-shadow: var(--shadow-glow-green); }
.ball-chip.wicket   { background: rgba(239,68,68,0.1); border-color: var(--red-base); color: var(--red-bright); }
.ball-chip.dot      { background: var(--bg-base);    color: var(--text-muted); }
.ball-chip.wide,
.ball-chip.no-ball  { background: var(--amber-dim);  border-color: var(--amber-muted); color: var(--amber-bright); }
```

### Animation System

Define all keyframes in `animations.css`. Import in `globals.css`.

```css
/* Page load — staggered reveal for dashboard panels */
@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* New ball event — flash green briefly */
@keyframes ballFlash {
  0%   { background: var(--bg-surface); }
  30%  { background: var(--green-dim); border-color: var(--green-muted); }
  100% { background: var(--bg-surface); }
}

/* Wicket — red flash */
@keyframes wicketFlash {
  0%, 100% { background: var(--bg-surface); }
  20%, 60% { background: rgba(239, 68, 68, 0.12); border-color: var(--red-base); }
}

/* Number counter roll — for AnimatedNumber component */
@keyframes numberRoll {
  from { transform: translateY(-100%); opacity: 0; }
  to   { transform: translateY(0);     opacity: 1; }
}

/* Pressure gauge needle */
@keyframes needleSweep {
  from { transform: rotate(var(--from-angle)); }
  to   { transform: rotate(var(--to-angle)); }
}

/* Score projection shimmer */
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position:  200% center; }
}

/* Momentum wave */
@keyframes momentumWave {
  0%, 100% { transform: scaleY(1); }
  50%       { transform: scaleY(1.4); }
}

/* Commentary slide in */
@keyframes commentaryIn {
  from { opacity: 0; transform: translateX(-12px); }
  to   { opacity: 1; transform: translateX(0); }
}

/* Connection pulse (Socket.IO status) */
@keyframes connectionPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
  50%       { box-shadow: 0 0 0 8px rgba(34, 197, 94, 0); }
}
```

### Dashboard Grid Layout

Use CSS Grid — not flexbox — for the main dashboard layout.

```css
.dashboard-grid {
  display: grid;
  grid-template-columns: 320px 1fr 300px;
  grid-template-rows: auto 1fr auto;
  gap: var(--space-lg);
  height: 100vh;
  padding: var(--space-lg);
}

/* Responsive breakpoints */
@media (max-width: 1280px) {
  .dashboard-grid { grid-template-columns: 280px 1fr; }
  .right-panel { display: none; }
}
@media (max-width: 768px) {
  .dashboard-grid { grid-template-columns: 1fr; grid-template-rows: auto; }
}
```

### Background Texture

Apply to `body` — creates the stadium atmosphere:
```css
body {
  background-color: var(--bg-void);
  background-image:
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(34, 197, 94, 0.08) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(59, 130, 246, 0.05) 0%, transparent 50%),
    url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.015'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}
```

### Recharts Theme Config

Pass this config to all Recharts chart components:

```javascript
export const chartTheme = {
  background: 'transparent',
  textColor: '#8b90a8',
  fontSize: 11,
  fontFamily: 'JetBrains Mono, monospace',
  axis: {
    domain: { line: { stroke: 'rgba(255,255,255,0.08)', strokeWidth: 1 } },
    ticks: { line: { stroke: 'rgba(255,255,255,0.08)' }, text: { fill: '#4a4f6a', fontSize: 10 } }
  },
  grid: { line: { stroke: 'rgba(255,255,255,0.04)', strokeDasharray: '4 4' } },
  tooltip: {
    container: {
      background: '#181b2d',
      border: '1px solid rgba(255,255,255,0.1)',
      borderRadius: '8px',
      color: '#f0f2ff',
      fontSize: '12px',
      fontFamily: 'DM Sans, sans-serif'
    }
  }
}
```

Win Probability line: stroke `#22c55e`, strokeWidth 2, dot fill `#22c55e`
Pressure Index line: stroke `#f59e0b`, strokeWidth 2
Run Rate area: fill `rgba(59, 130, 246, 0.1)`, stroke `#3b82f6`

### D3 Wagon Wheel Colors
```javascript
const shotColors = {
  boundary_four: '#22c55e',
  boundary_six:  '#4ade80',
  single:        '#3b82f6',
  double:        '#60a5fa',
  dot:           '#4a4f6a',
  wicket:        '#ef4444'
}
```

### Component Animation Rules

1. **On mount:** use `animation: fadeSlideUp 400ms ease both` with staggered `animation-delay` per card (0ms, 80ms, 160ms, 240ms...)
2. **On new ball:** trigger `ballFlash` animation on the scorecard row and ball timeline
3. **On wicket:** trigger `wicketFlash` on entire scorecard panel
4. **On momentum shift:** show a full-width banner with `commentaryIn` animation
5. **AnimatedNumber component:** when a number changes, animate the old value out (translateY -100%) and new value in (translateY from +100%) — gives a slot machine / ticker effect
6. **Never animate layout properties** (width, height, top, left) — only transform and opacity for 60fps performance
7. **Use `will-change: transform`** on elements that animate frequently (pressure gauge needle, win probability line)

---

## Docker Compose Services

```yaml
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    ports: ["2181:2181"]
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on: [zookeeper]
    ports: ["9092:9092"]
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"

  mongodb:
    image: mongo:7.0
    ports: ["27017:27017"]
    volumes: ["mongo_data:/data/db"]

  redis:
    image: redis:7.2-alpine
    ports: ["6379:6379"]

  spark-master:
    build: ./docker/spark
    ports: ["8080:8080", "7077:7077"]

volumes:
  mongo_data:
```

---

## Code Quality Rules

### Python
- Use `black` for formatting (line length 88)
- Use `ruff` for linting
- Use `pytest` for all tests
- Every analytics function must have a docstring with formula explanation
- Log using `structlog` — never `print()`

### JavaScript / Node.js
- Use `eslint` with `eslint-config-airbnb-base`
- Use `prettier` for formatting (single quotes, no semicolons, 2-space indent)
- Use `jest` for backend tests
- Use `winston` for structured logging — never `console.log()` in production code
- Always validate request bodies with `joi` or `zod`

### React
- Functional components only — no class components
- Custom hooks for ALL data fetching and socket logic — never directly in JSX
- PropTypes or JSDoc on all component props
- Use React.memo on heavy chart components
- `key` prop on all list renders — use `ball_id` or `match_id`, never array index

---

## Error Handling

### Python (Producer + Spark)
```python
try:
    result = risky_operation()
except KafkaException as e:
    logger.error("kafka_error", error=str(e), match_id=match_id)
    raise
except Exception as e:
    logger.error("unexpected_error", error=str(e))
    raise
```

### Node.js
```javascript
// All async route handlers wrapped with this pattern:
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next)

// Global error handler in app.js always returns standard envelope
```

---

## Performance Rules

1. **Never query MongoDB in a Socket.IO event handler** — always read from Redis cache
2. **Spark writeStream batch size** should not exceed 100 events per micro-batch
3. **React chart components** must use `React.memo` — they re-render on every ball
4. **MongoDB queries** must always use indexed fields — never full collection scans
5. **Kafka consumer** lag should be monitored — alert if lag exceeds 50 messages
6. **Frontend bundle** — lazy load the D3 wagon wheel and heatmap components (they're heavy)

---

## What-If Simulator Logic

Accept POST body:
```json
{
  "match_id": "string",
  "scenario": {
    "next_n_balls": [4, 1, 0, 6, 1, "W"],
    "override_batsman": "optional player name"
  }
}
```

1. Fetch current match state from Redis
2. Apply scenario ball-by-ball on a cloned state object (never mutate real state)
3. Recompute pressure index, win probability, and run rate on the simulated state
4. Return simulated analytics alongside the real current analytics for comparison
5. Never persist simulated data to MongoDB

---

## Smart Commentary Rules

Commentary is generated rule-based in `analytics/commentary.py`. Rules in priority order:

| Trigger | Commentary Template |
|---|---|
| Wicket | `"{bowler} strikes! {batsman} walks back — {team} in trouble at {score}/{wickets}"` |
| Six | `"MAXIMUM! {batsman} sends that one into the stands. The crowd goes wild!"` |
| Four | `"FOUR! {batsman} finds the gap perfectly."` |
| 3+ dots in a row | `"The pressure is mounting — {batsman} hasn't scored in {n} balls. Required rate climbing."` |
| RRR > 12 | `"This is a steep ask now. {team} need {rrr} an over with {wickets} wickets in hand."` |
| Momentum shift | `"MOMENTUM SHIFT! {n} boundaries in the last over. The game has swung dramatically."` |
| Win prob > 80% | `"{team} are in the driver's seat now — {prob}% win probability."` |
| 50 / 100 milestone | `"FIFTY UP for {batsman}! A crucial innings when {team} needed it most."` |

Always append match context: `(Over {over}, {score}/{wickets}, RRR: {rrr})`

---

## Git Conventions

Branch naming: `feature/kafka-producer`, `fix/spark-memory-leak`, `chore/docker-compose`
Commit format: `type(scope): message` — e.g. `feat(spark): add pressure index calculator`
Types: `feat`, `fix`, `chore`, `refactor`, `test`, `docs`
Never commit `.env` — only `.env.example`

---

## .cursorrules (copy this to project root as `.cursorrules`)

```
You are an expert engineer on the Cricklytics AI project — a production Big Data cricket analytics platform.

STACK: Python 3.11 (Kafka producer, PySpark 3.5), Node.js 20 ESM (Express + Socket.IO), React 18 + Vite (frontend), MongoDB 7, Redis 7, Apache Kafka, Docker Compose.

ARCHITECTURE: Cricket API → Kafka Producer → Kafka Topic → Spark Structured Streaming → MongoDB + Redis → Node.js API → React Dashboard.

ALWAYS:
- Follow the directory structure in claude.md exactly
- Use the Dark Pitch theme (CSS variables) for ALL frontend components
- Use Bebas Neue for stat numbers, Barlow Condensed for headers, DM Sans for body, JetBrains Mono for data
- Use Spark Structured Streaming (not DStream)
- Partition Kafka topics by match_id
- Use Redis cache before querying MongoDB in hot paths
- Return the standard API envelope { success, data, meta }
- Emit Socket.IO events in the format defined in claude.md
- Log with structlog (Python) or winston (Node) — never print/console.log
- Add type hints to all Python functions
- Use ES module syntax in Node.js

NEVER:
- Use CommonJS require() in Node.js
- Use DStream in Spark (legacy)
- Use class components in React
- Hardcode API keys or connection strings
- Use array index as React key prop
- Query MongoDB directly in Socket.IO handlers (use Redis)
- Animate layout properties — only transform and opacity
- Use Inter, Roboto, Arial, or system-ui fonts in the frontend
- Use purple gradient on white background (generic AI aesthetic)
- Use console.log in production code paths

ANALYTICS FORMULAS: Always use the exact formulas defined in claude.md for Pressure Index, Win Probability, Player Impact Score, and Momentum detection.

UI PHILOSOPHY: Dark stadium cinematic feel. Every component should feel like a premium sports broadcast overlay. Glowing green accents for positive events, amber for pressure, red for wickets.
```