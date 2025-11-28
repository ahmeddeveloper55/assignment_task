from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import token_refresh, token_verify

from .views import restful_apis

router = DefaultRouter()

router.register(r'login', restful_apis.LoginViewSet, basename='login')
router.register(r'password', restful_apis.PasswordViewSet, basename='password')

urlpatterns = [
    path('api/token/refresh/', token_refresh, name='refresh_jwt_token'),
    path('api/token/verify/', token_verify, name='verify_jwt_token'),
]

urlpatterns += (
    path('api/', include((router.urls, 'apps.auth'), namespace='api'), ),
)
