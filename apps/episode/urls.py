from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import restful_apis

router = DefaultRouter()
router.register(r'episodes', restful_apis.EpisodeViewSet, basename='episode')
router.register(r'discovery/episodes', restful_apis.PublicEpisodeViewSet, basename='discovery-episode')

urlpatterns = []
urlpatterns += (
    path('api/', include((router.urls, 'apps.episode'), namespace='api')),
)