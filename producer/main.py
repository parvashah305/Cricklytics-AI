import json
import logging
import time
from typing import Any

from kafka import KafkaProducer

from config import load_config
from cricket_client import CricketApiClient, CricketApiConfig

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

REQUIRED_EVENT_FIELDS: dict[str, type] = {
    "event_id": str,
    "match_id": str,
    "innings": int,
    "over": float,
    "ball": int,
    "batsman": str,
    "bowler": str,
    "runs": int,
    "is_wicket": bool,
    "is_boundary": bool,
    "is_dot": bool,
    "delivery_type": str,
    "timestamp": int,
}


def make_mock_ball_event() -> dict[str, Any]:
    now_ms = int(time.time() * 1000)
    return {
        "event_id": f"demo-match-1:1:1.1:1:{now_ms}",
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
        "timestamp": now_ms,
    }


def validate_event_schema(event: dict[str, Any]) -> tuple[bool, str]:
    for field, expected_type in REQUIRED_EVENT_FIELDS.items():
        if field not in event:
            return False, f"missing field: {field}"

        value = event[field]
        if expected_type is float:
            if not isinstance(value, (float, int)):
                return False, f"invalid type for {field}: expected float-compatible"
        elif not isinstance(value, expected_type):
            return False, f"invalid type for {field}: expected {expected_type.__name__}"

    if not event["match_id"].strip():
        return False, "match_id cannot be empty"
    if event["innings"] <= 0:
        return False, "innings must be positive"
    if event["ball"] < 0:
        return False, "ball cannot be negative"
    if event["runs"] < 0:
        return False, "runs cannot be negative"
    if event["timestamp"] <= 0:
        return False, "timestamp must be positive epoch milliseconds"

    return True, "ok"


def extract_latest_ball_event(payload: dict[str, Any], fallback_match_id: str) -> dict[str, Any]:
    """
    Build a best-effort normalized event from Cricbuzz commentary payload.
    Falls back to a safe placeholder if live fields are absent.
    """
    commentary_list = payload.get("commentaryList", [])
    if not commentary_list:
        return {}

    latest = commentary_list[0] if commentary_list else {}
    over_number = float(latest.get("overNumber", 0.0))
    runs = int(latest.get("runs", 0))
    wicket = bool(latest.get("isWicket", False))
    batsman = str(latest.get("batsmanName", "Unknown Batter"))
    bowler = str(latest.get("bowlerName", "Unknown Bowler"))
    innings = int(latest.get("inningsId", 1))
    ball_number = int(latest.get("ballNbr", 0))
    event_id = f"{fallback_match_id}:{innings}:{over_number}:{ball_number}"

    return {
        "event_id": event_id,
        "match_id": fallback_match_id,
        "innings": innings,
        "over": over_number,
        "ball": ball_number,
        "batsman": batsman,
        "bowler": bowler,
        "runs": runs,
        "is_wicket": wicket,
        "is_boundary": runs in (4, 6),
        "is_dot": runs == 0,
        "delivery_type": "legal",
        "timestamp": int(time.time() * 1000),
    }


def main() -> None:
    config = load_config()
    producer = KafkaProducer(bootstrap_servers=config.kafka_broker)
    cricket_client = CricketApiClient(
        CricketApiConfig(api_key=config.rapidapi_key, api_host=config.rapidapi_host)
    )

    last_event_id = ""
    while True:
        try:
            payload = cricket_client.fetch_match_commentary(config.match_id)
            event = extract_latest_ball_event(payload, config.match_id)
            if not event:
                logger.info("no live ball event available yet")
            else:
                event_id = str(event.get("event_id", ""))
                if event_id and event_id != last_event_id:
                    valid, reason = validate_event_schema(event)
                    if not valid:
                        logger.warning("event failed schema validation: %s", reason)
                        time.sleep(config.poll_interval_seconds)
                        continue
                    producer.send(
                        topic=config.kafka_topic_ball_events,
                        key=event["match_id"].encode("utf-8"),
                        value=json.dumps(event).encode("utf-8"),
                    )
                    producer.flush()
                    last_event_id = event_id
                    logger.info("published live event %s", event_id)
                else:
                    logger.info("skipping duplicate event %s", event_id)
        except Exception as error:
            logger.warning("live polling failed, using mock event: %s", error)
            event = make_mock_ball_event()
            valid, reason = validate_event_schema(event)
            if not valid:
                logger.warning("mock event failed schema validation: %s", reason)
                time.sleep(config.poll_interval_seconds)
                continue
            producer.send(
                topic=config.kafka_topic_ball_events,
                key=event["match_id"].encode("utf-8"),
                value=json.dumps(event).encode("utf-8"),
            )
            producer.flush()
            logger.info("published fallback mock ball event")

        time.sleep(config.poll_interval_seconds)


if __name__ == "__main__":
    main()
