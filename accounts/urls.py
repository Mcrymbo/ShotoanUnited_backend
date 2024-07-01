from .views import ProfileViewSet
from rest_framework.routers import DefaultRouter

profile_router = DefaultRouter()
profile_router.register(r'profile', ProfileViewSet)