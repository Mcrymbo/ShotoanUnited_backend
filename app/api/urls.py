from django.urls import path
from rest_framework.routers import DefaultRouter
# from .views import UserViewSet, GroupViewSet, EventViewSet
from .views import EventViewSet, UserViewSet

user_router = DefaultRouter()
user_router.register(r'users', UserViewSet)
# group_router = DefaultRouter()
# group_router.register(r'groups', GroupViewSet)
event_router = DefaultRouter()
event_router.register(r'events', EventViewSet)