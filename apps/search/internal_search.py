# apps/search/internal_search.py

from django.db.models import Q

from apps.program.models import Program
from apps.episode.models import Episode


def search_internal_content(query: str, limit: int = 10, offset: int = 0):
    """
    Simple internal search:

    - Looks into Program and Episode models.
    - Searches in title + short/long description/body.
    - Returns a flat list of results with a `kind` key
      so the caller knows if it's a program or an episode.
    """
    if not query:
        return []

    # Normalize pagination window
    start = max(offset, 0)
    end = start + max(limit, 1)

    # Programs: search title + short_description + long_description
    program_qs = (
        Program.objects.filter(
            Q(is_active=True),
            Q(is_published=True),
            Q(
                Q(title__icontains=query)
                | Q(short_description__icontains=query)
                | Q(long_description__icontains=query)
            ),
        )
        .select_related("category")
        .order_by("-publish_date", "-id")
        .values(
            "id",
            "title",
            "short_description",
            "slug",
            "cover_image_url",
            "type",
            "language",
            "publish_date",
        )
    )

    program_rows = list(program_qs[start:end])

    program_results = [
        {
            "kind": "program",
            "id": row["id"],
            "title": row["title"],
            "description": row["short_description"],
            "slug": row["slug"],
            "cover_image_url": row["cover_image_url"],
            "type": row["type"],
            "language": row["language"],
            "publish_date": row["publish_date"],
        }
        for row in program_rows
    ]

    # Episodes: search title + short_description + body
    episode_qs = (
        Episode.objects.filter(
            Q(is_published=True),
            Q(program__is_active=True),
            Q(program__is_published=True),
            Q(
                Q(title__icontains=query)
                | Q(short_description__icontains=query)
                | Q(body__icontains=query)
            ),
        )
        .select_related("program", "program__category")
        .order_by("-publish_date", "-id")
        .values(
            "id",
            "title",
            "short_description",
            "slug",
            "thumbnail_url",
            "media_type",
            "publish_date",
            "program__slug",
        )
    )

    episode_rows = list(episode_qs[start:end])

    episode_results = [
        {
            "kind": "episode",
            "id": row["id"],
            "title": row["title"],
            "description": row["short_description"],
            "slug": row["slug"],
            "thumbnail_url": row["thumbnail_url"],
            "media_type": row["media_type"],
            "publish_date": row["publish_date"],
            "program_slug": row["program__slug"],
        }
        for row in episode_rows
    ]


    return program_results + episode_results