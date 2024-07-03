from .views import ProfileViewSet, UserViewset
from rest_framework.routers import DefaultRouter

profile_router = DefaultRouter()
profile_router.register(r'profile', ProfileViewSet)

user_router = DefaultRouter()
user_router.register(r'users', UserViewset)