from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import restful_apis


router = DefaultRouter()
router.register(r'categories', restful_apis.CategoryViewSet, basename='category')

urlpatterns = [
    path('api/', include((router.urls , 'apps.category'), namespace='api'), ),
]
