import json
import logging
import time
from typing import Any

from kafka import KafkaProducer

from config import load_config

logger = logging.getLogger(__name__)


def make_mock_ball_event() -> dict[str, Any]:
    return {
        "match_id": "demo-match-1",
        "innings": 1,
        "over": 1.1,
        "ball": 1,
        "batsman": "Demo Batter",
        "bowler": "Demo Bowler",
        "runs": 1,
        "is_wicket": False,
        "is_boundary": False,
        "is_dot": False,
        "delivery_type": "legal",
        "timestamp": int(time.time() * 1000),
    }


def main() -> None:
    config = load_config()
    producer = KafkaProducer(bootstrap_servers=config.kafka_broker)
    event = make_mock_ball_event()
    producer.send(
        topic=config.kafka_topic_ball_events,
        key=event["match_id"].encode("utf-8"),
        value=json.dumps(event).encode("utf-8"),
    )
    producer.flush()
    logger.info("published mock ball event")


if __name__ == "__main__":
    main()
