# Cricklytics AI

Initial scaffold for your real-time cricket intelligence platform based on `claude.md`.

## What is set up

- `docker/docker-compose.yml` for Kafka, Zookeeper, MongoDB, Redis, Spark
- `backend/` Express + Socket.IO starter with API envelope and basic match routes
- `frontend/` React + Vite starter with Dark Pitch baseline styling
- `producer/` Python Kafka producer mock event publisher
- `spark-jobs/` Structured Streaming starter to consume Kafka events
- `.env.example` with all required environment keys

## Quick start

1. Start infra:
   - `docker compose -f docker/docker-compose.yml up -d`
2. Backend:
   - `cd backend && npm install && npm run dev`
3. Frontend:
   - `cd frontend && npm install && npm run dev`
4. Producer:
   - Create Python venv, install `kafka-python`, then run `python producer/main.py`
5. Spark:
   - Run `spark-submit spark-jobs/main_stream.py`

## Next implementation milestones

1. Replace mock producer event with live Cricbuzz/RapidAPI polling
2. Add Spark analytics modules (win probability, momentum, player impact, commentary)
3. Persist stream output to MongoDB via `foreachBatch`
4. Add Redis cache + Mongo models/services in backend
5. Build full dashboard pages and socket hooks in frontend
