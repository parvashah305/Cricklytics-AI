# Cricklytics AI Task Tracker

Use this file as the single progress tracker.  
Rule: after each completed task, change `[ ]` to `[x]` and add a completion date note.

## Phase 1 - Foundation Scaffold (Completed)

- [x] Create root project structure (`backend`, `frontend`, `producer`, `spark-jobs`, `docker`)
- [x] Add `.env.example` with required config keys
- [x] Add Docker Compose baseline stack
- [x] Initialize backend Express + Socket.IO starter
- [x] Add Atlas-ready MongoDB connection bootstrap in backend
- [x] Initialize frontend React + Vite starter
- [x] Initialize producer mock Kafka publisher
- [x] Initialize Spark streaming consumer starter
- [x] Add root `.gitignore`
- [x] Add initial `README.md`

## Phase 2 - Data Ingestion + Persistence

- [x] Implement live Cricbuzz/RapidAPI polling client in producer
- [x] Publish normalized ball events to Kafka with `match_id` key partitioning
- [x] Add Kafka event schema validation in producer
- [x] Add Spark `foreachBatch` writer for MongoDB `ball_events`
- [x] Add Spark writer for `analytics` collection updates
- [ ] Add Redis invalidation after Spark writes per `match_id`

## Phase 3 - Backend API + Caching

- [ ] Add Mongoose models (`Match`, `BallEvent`, `Analytics`, `Player`)
- [ ] Add Redis service layer with TTL strategy
- [ ] Implement `/api/matches` routes from spec
- [ ] Implement `/api/players` routes from spec
- [ ] Implement `/api/simulator/whatif` route contract
- [ ] Ensure all responses follow standard envelope

## Phase 4 - Live Frontend Dashboard

- [ ] Build dashboard page layout with Dark Pitch design tokens
- [ ] Add Redux store slices (`match`, `analytics`, `player`, `ui`)
- [ ] Implement `useSocket` and `useLiveMatch` hooks
- [ ] Connect live scorecard + ball timeline components
- [ ] Add analytics components (win probability, pressure, momentum, run rate)
- [ ] Add smart commentary and momentum banner UI

## Phase 5 - Simulator + Quality + Release

- [ ] Implement what-if simulator UI and API integration
- [ ] Add backend tests for core endpoints
- [ ] Add Python tests for producer/spark analytics utilities
- [ ] Add lint/format scripts and run baseline checks
- [ ] Final end-to-end smoke test (producer -> kafka -> spark -> mongo/redis -> backend -> frontend)
- [ ] Prepare deployment-ready documentation
