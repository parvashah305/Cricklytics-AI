from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ProducerConfig:
    kafka_broker: str
    kafka_topic_ball_events: str
    rapidapi_key: str
    rapidapi_host: str
    match_id: str
    poll_interval_seconds: int


def load_config() -> ProducerConfig:
    return ProducerConfig(
        kafka_broker=os.getenv("KAFKA_BROKER", "localhost:9092"),
        kafka_topic_ball_events=os.getenv(
            "KAFKA_TOPIC_BALL_EVENTS", "cricket.ball.events"
        ),
        rapidapi_key=os.getenv("RAPIDAPI_KEY", ""),
        rapidapi_host=os.getenv("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com"),
        match_id=os.getenv("CRICBUZZ_MATCH_ID", ""),
        poll_interval_seconds=int(os.getenv("PRODUCER_POLL_INTERVAL_SECONDS", "5")),
    )
