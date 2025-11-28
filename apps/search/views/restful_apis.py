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
      - q: text query for internal search (optional)
      - video_id: optional YouTube video ID for external fallback
      - country_code: optional ISO country code for SerpApi (e.g., 'us', 'sa')
      - language_code: optional language code for SerpApi (e.g., 'en', 'ar')

    Flow:
      1) Try internal DB search using `q`.
      2) If internal results exist → return them with source="internal".
      3) If internal results are empty and video_id is provided → call external.
      4) If external returns video → return it with source="external".
      5) If both fail → return empty results.
    """

    external_video_service_class = YouTubeVideoSearchService

    def get(self, request, *args, **kwargs):
        search_text = request.query_params.get("q", "").strip()
        video_id = request.query_params.get("video_id", "").strip()
        country_code = request.query_params.get("country_code", "").strip() or None
        language_code = request.query_params.get("language_code", "").strip() or None

        # 1) Internal search (CMS/DB)
        internal_results = search_internal_content(search_text)

        if internal_results:
            return Response(
                {
                    "query": search_text,
                    "source": "internal",
                    "results": internal_results,
                },
                status=status.HTTP_200_OK,
            )

        # 2) External search (SerpApi YouTube) as fallback
        if video_id:
            external_service = self.external_video_service_class()
            video_metadata = external_service.get_video_by_id(
                video_id=video_id,
                country_code=country_code,
                language_code=language_code,
            )

            if video_metadata is None:
                return Response(
                    {
                        "query": search_text,
                        "video_id": video_id,
                        "source": "external",
                        "results": [],
                        "error": "External search provider did not return a result.",
                    },
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            return Response(
                {
                    "query": search_text,
                    "video_id": video_metadata.video_id,
                    "source": "external",
                    "results": [
                        {
                            "id": video_metadata.video_id,
                            "title": video_metadata.title,
                            "thumbnail_url": video_metadata.thumbnail_url,
                            "view_count": video_metadata.view_count,
                            "like_count": video_metadata.like_count,
                            "description": video_metadata.description,
                            "channel_name": video_metadata.channel_name,
                        }
                    ],
                },
                status=status.HTTP_200_OK,
            )

        # 3) Nothing internal and no external video_id
        return Response(
            {
                "query": search_text,
                "source": "none",
                "results": [],
            },
            status=status.HTTP_200_OK,
        )