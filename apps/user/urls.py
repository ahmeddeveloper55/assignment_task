from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import restful_apis

router = DefaultRouter()

router.register(r'users', restful_apis.UserViewSet, basename='user')

urlpatterns = [
    path('api/', include((router.urls, 'apps.user'), namespace='api'), ),
]
