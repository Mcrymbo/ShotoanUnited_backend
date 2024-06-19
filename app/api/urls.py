from rest_framework.routers import DefaultRouter
from .views import EventViewSet

event_router = DefaultRouter()
event_router.register(r'events', EventViewSet)