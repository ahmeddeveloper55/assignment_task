# apps/search/services/serpapi_client.py
from typing import Any, Dict, Optional

import requests
from django.conf import settings


class SerpApiClient:
    """
    Generic client for SerpApi.
    - Knows how to call SerpApi with any engine.
    - Does not know anything about YouTube, videos, etc.
    """

    BASE_URL = "https://serpapi.com/search"

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or getattr(settings, "SERPAPI_API_KEY", "")
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY is not configured")

    def search(self, engine_name: str, engine_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a SerpApi search for a given engine and params.
        """
        request_params = {
            "engine": engine_name,
            "api_key": self.api_key,
            **engine_params,
        }

        response = requests.get(self.BASE_URL, params=request_params, timeout=3)
        response.raise_for_status()
        return response.json()