# apps/search/urls.py
from django.urls import path

from apps.search.views.restful_apis import SearchAPIView

app_name = "search"

urlpatterns = [
    path("api/searches/", SearchAPIView.as_view(), name="search"),
]