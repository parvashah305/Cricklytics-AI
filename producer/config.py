from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ProducerConfig:
    kafka_broker: str
    kafka_topic_ball_events: str


def load_config() -> ProducerConfig:
    return ProducerConfig(
        kafka_broker=os.getenv("KAFKA_BROKER", "localhost:9092"),
        kafka_topic_ball_events=os.getenv(
            "KAFKA_TOPIC_BALL_EVENTS", "cricket.ball.events"
        ),
    )
