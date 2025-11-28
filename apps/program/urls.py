from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import restful_apis

router = DefaultRouter()
router.register(r'programs', restful_apis.ProgramViewSet, basename='program')
router.register(r'discovery/programs', restful_apis.DiscoveryProgramViewSet, basename='discovery-program')

urlpatterns = []
urlpatterns += (
    path('api/', include((router.urls, 'apps.program'), namespace='api')),
)