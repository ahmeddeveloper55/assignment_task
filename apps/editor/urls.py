from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ..user import routers as user_routers
from .views import restful_apis

router = DefaultRouter()
profile_router = user_routers.ProfileRouter()
profile_router.register(r'profile', restful_apis.EditorProfileViewSet, basename='profile')

router.register(r'editors', restful_apis.EditorViewSet, basename='editor')


urlpatterns = [
    path('api/', include((router.urls + profile_router.urls, 'apps.editor'), namespace='api'), ),
]
