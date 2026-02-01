from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, register_user, login_user, get_csrf_token

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/csrf/', get_csrf_token, name='csrf'),
]
