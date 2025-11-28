from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import restful_apis

router = DefaultRouter()

router.register(r'tags', restful_apis.TagViewSet, basename='tag')

urlpatterns = [

]

urlpatterns += (
    path('api/', include((router.urls, 'apps.tag'), namespace='api'), ),
)
