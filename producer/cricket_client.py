import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class CricketApiConfig:
    api_key: str
    api_host: str


class CricketApiClient:
    def __init__(self, config: CricketApiConfig) -> None:
        self._config = config

    def fetch_match_commentary(self, match_id: str) -> dict[str, Any]:
        """
        Fetch raw live commentary payload from the RapidAPI Cricbuzz endpoint.
        """
        if not self._config.api_key:
            raise ValueError("RAPIDAPI_KEY is missing")
        if not match_id:
            raise ValueError("CRICBUZZ_MATCH_ID is missing")

        query = urlencode({"matchId": match_id})
        url = f"https://{self._config.api_host}/mcenter/v1/{match_id}/comm?{query}"
        request = Request(
            url=url,
            headers={
                "X-RapidAPI-Key": self._config.api_key,
                "X-RapidAPI-Host": self._config.api_host,
            },
            method="GET",
        )

        try:
            with urlopen(request, timeout=10) as response:
                body = response.read().decode("utf-8")
                if not body.strip():
                    return {}
                return json.loads(body)
        except HTTPError as error:
            raise RuntimeError(f"RapidAPI HTTP error: {error.code}") from error
        except URLError as error:
            raise RuntimeError(f"RapidAPI network error: {error.reason}") from error
