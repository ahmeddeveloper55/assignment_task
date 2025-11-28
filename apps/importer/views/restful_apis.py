# apps/importer/views/restful_apis.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.program.serializers import ProgramSerializer
from apps.episode.serializers import EpisodeSerializer

from apps.importer.permissions import ImportAccessPermission
from apps.importer.services import ImportService

class ProgramImportAPIView(APIView):
    """
    Import or update a Program using ImportService.

    Supports two request shapes:

    1) Nested:
       {
         "source_code": "yt",
         "external_id": "hist-001",
         "program": { ... Program fields ... }
       }

    2) Flat:
       {
         "source_code": "yt",
         "external_id": "hist-001",
         ... Program fields directly here ...
       }
    """

    permission_classes = (ImportAccessPermission,)

    def post(self, request, *args, **kwargs):
        payload = request.data

        # meta fields
        source_code = payload.get("source_code") or payload.get("source")
        external_id = payload.get("external_id")

        # program payload: nested or flat
        if isinstance(payload.get("program"), dict):
            program_payload = payload["program"]
        else:
            meta_keys = {"source_code", "source", "external_id"}
            program_payload = {
                key: value
                for key, value in payload.items()
                if key not in meta_keys
            }

        errors = {}
        if not source_code:
            errors["source_code"] = ["This field is required."]
        if not external_id:
            errors["external_id"] = ["This field is required."]
        if not program_payload:
            errors["program"] = [
                "Program data is required (either nested under 'program' or as flat fields)."
            ]

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        program = ImportService.import_program(
            source_code=source_code,
            external_id=external_id,
            program_data=program_payload,
            request=request,
        )

        data = ProgramSerializer(program, context={"request": request}).data
        return Response(data, status=status.HTTP_201_CREATED)


class EpisodeImportAPIView(APIView):
    """
    Import or update an Episode for a given Program.

    Supports two request shapes:

    1) Nested:
       {
         "source_code": "yt",
         "external_id": "8SCQnB4A0xU",
         "program_id": "<program UUID>",
         "episode": { ... Episode fields ... }
       }

    2) Flat:
       {
         "source_code": "yt",
         "external_id": "8SCQnB4A0xU",
         "program_id": "<program UUID>",
         ... Episode fields directly here ...
       }
    """

    permission_classes = (ImportAccessPermission,)

    def post(self, request, *args, **kwargs):
        payload = request.data

        source_code = payload.get("source_code") or payload.get("source")
        external_id = payload.get("external_id")
        program_id = payload.get("program_id")

        # episode payload: nested or flat
        if isinstance(payload.get("episode"), dict):
            episode_payload = payload["episode"]
        else:
            meta_keys = {"source_code", "source", "external_id", "program_id"}
            episode_payload = {
                key: value
                for key, value in payload.items()
                if key not in meta_keys
            }

        errors = {}
        if not source_code:
            errors["source_code"] = ["This field is required."]
        if not external_id:
            errors["external_id"] = ["This field is required."]
        if not program_id:
            errors["program_id"] = ["This field is required."]
        if not episode_payload:
            errors["episode"] = [
                "Episode data is required (either nested under 'episode' or as flat fields)."
            ]

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        episode = ImportService.import_episode(
            source_code=source_code,
            external_id=external_id,
            program_id=program_id,
            episode_data=episode_payload,
            request=request,
        )

        data = EpisodeSerializer(episode, context={"request": request}).data
        return Response(data, status=status.HTTP_201_CREATED)