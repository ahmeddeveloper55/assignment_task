# apps/search/services.py
from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class IndexableProgram(Protocol):
    id: int
    title: str
    description: str
    is_active: bool
    is_published: bool


@runtime_checkable
class IndexableEpisode(Protocol):
    id: int
    title: str
    description: str
    is_active: bool
    is_published: bool
    program_id: int


class SearchService:
    """
    Boundary between domain models (Program/Episode) and the search subsystem.

    For the assignment:
      - In a real system, these methods would push to Algolia/Elastic/etc.
    """

    @classmethod
    def index_program(cls, program: IndexableProgram) -> None:
        """
        Index or update a Program in the search index.

        """
        # Example stub implementation:
        #  logger.info("Indexing program in search", extra={"program_id": program.id})
        return None

    @classmethod
    def remove_program(cls, program_id: int) -> None:
        """
        Remove a Program from the search index by ID.
        """
        # logger.info("Removing program from search", extra={"program_id": program_id})
        return None

    @classmethod
    def index_episode(cls, episode: IndexableEpisode) -> None:
        """
        Index or update an Episode in the search index.
        """
        # logger.info("Indexing episode in search", extra={"episode_id": episode.id})
        return None

    @classmethod
    def remove_episode(cls, episode_id: int) -> None:
        """
        Remove an Episode from the search index by ID.
        """
        # logger.info("Removing episode from search", extra={"episode_id": episode_id})
        return None