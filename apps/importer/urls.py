# apps/importer/urls.py
from django.urls import path

from .views.restful_apis import ProgramImportAPIView, EpisodeImportAPIView

app_name = "importer"

urlpatterns = [
    path("api/programs/", ProgramImportAPIView.as_view(), name="program-importer"),
    path("api/episodes/", EpisodeImportAPIView.as_view(), name="episode-importer"),
]