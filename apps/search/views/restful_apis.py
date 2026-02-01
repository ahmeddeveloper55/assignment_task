# apps/search/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..internal_search import search_internal_content
from ..external_search_api import YouTubeVideoSearchService


class SearchAPIView(APIView):
    """
    GET /api/search/

    Query parameters:
      - search_query: text query for search (required)
      - offset: pagination offset (optional, default 0)
      - limit: max results (optional, default 10)
      - country_code: optional ISO country code for SerpApi (e.g., 'us', 'sa')
      - language_code: optional language code for SerpApi (e.g., 'en', 'ar')

    Flow:
      1) Try internal DB search using `search_query`.
      2) If internal results exist → return them with source="internal".
      3) If internal results are empty → automatically search YouTube.
      4) If external returns videos → return them with source="external".
      5) If both fail → return empty results.
    """

    external_video_service_class = YouTubeVideoSearchService

    def get(self, request, *args, **kwargs):
        # Accept both 'search_query' and 'q' for flexibility
        search_text = (
            request.query_params.get("search_query", "").strip()
            or request.query_params.get("q", "").strip()
        )
        offset = int(request.query_params.get("offset", 0))
        limit = int(request.query_params.get("limit", 10))
        country_code = request.query_params.get("country_code", "").strip() or None
        language_code = request.query_params.get("language_code", "").strip() or None

        if not search_text:
            return Response(
                {
                    "query": "",
                    "source": "none",
                    "results": [],
                    "error": "search_query parameter is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1) Internal search (CMS/DB)
        internal_results = search_internal_content(search_text, limit=limit, offset=offset)

        if internal_results:
            return Response(
                {
                    "query": search_text,
                    "source": "internal",
                    "results": internal_results,
                },
                status=status.HTTP_200_OK,
            )

        # 2) External search (SerpApi YouTube) as automatic fallback
        external_service = self.external_video_service_class()
        external_results = external_service.search_by_query(
            query=search_text,
            country_code=country_code,
            language_code=language_code,
            limit=limit,
        )

        if external_results:
            return Response(
                {
                    "query": search_text,
                    "source": "external",
                    "results": [
                        {
                            "id": video.video_id,
                            "title": video.title,
                            "thumbnail_url": video.thumbnail_url,
                            "view_count": video.view_count,
                            "like_count": video.like_count,
                            "description": video.description,
                            "channel_name": video.channel_name,
                        }
                        for video in external_results
                    ],
                },
                status=status.HTTP_200_OK,
            )

        # 3) Nothing found in either source
        return Response(
            {
                "query": search_text,
                "source": "none",
                "results": [],
            },
            status=status.HTTP_200_OK,
        )