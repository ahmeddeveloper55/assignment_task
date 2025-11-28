# apps/search/services/external_search_api.py
from dataclasses import dataclass
from typing import Optional

import requests

from .serpapi_client import SerpApiClient


@dataclass
class VideoMetadata:
    video_id: str
    title: str
    thumbnail_url: str
    view_count: Optional[int]
    like_count: Optional[int]
    description: Optional[str]
    channel_name: Optional[str]


class YouTubeVideoSearchService:
    """
    External video search service.
    - Uses SerpApi with `youtube_video` engine.
    - Maps JSON response to VideoMetadata.
    If engine/provider changes, you modify this class, not the view.
    """

    ENGINE_NAME = "youtube_video"

    def __init__(self, serpapi_client: Optional[SerpApiClient] = None) -> None:
        self._client = serpapi_client or SerpApiClient()

    def get_video_by_id(
        self,
        video_id: str,
        country_code: Optional[str] = None,
        language_code: Optional[str] = None,
    ) -> Optional[VideoMetadata]:
        engine_params = {"v": video_id}

        if country_code:
            # serpapi uses gl (geo location)
            engine_params["gl"] = country_code

        if language_code:
            # serpapi uses hl (host language)
            engine_params["hl"] = language_code

        try:
            raw_response = self._client.search(self.ENGINE_NAME, engine_params)
        except requests.RequestException:
            return None

        metadata_block = raw_response.get("search_metadata") or {}
        if metadata_block.get("status") != "Success":
            return None

        description_block = raw_response.get("description") or {}
        channel_block = raw_response.get("channel") or {}

        return VideoMetadata(
            video_id=video_id,
            title=raw_response.get("title") or "",
            thumbnail_url=raw_response.get("thumbnail") or "",
            view_count=raw_response.get("extracted_views"),
            like_count=raw_response.get("extracted_likes"),
            description=description_block.get("content"),
            channel_name=channel_block.get("name"),
        )