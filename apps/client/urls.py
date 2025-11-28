from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ..user import routers as user_routers
from .views import restful_apis

router = DefaultRouter()
profile_router = user_routers.ProfileRouter()
profile_router.register(r'profile', restful_apis.ClientProfileViewSet, basename='profile')

router.register(r'clients', restful_apis.ClientViewSet, basename='client')

urlpatterns = [
    path('api/', include((router.urls + profile_router.urls, 'apps.client'), namespace='api'), ),
]
