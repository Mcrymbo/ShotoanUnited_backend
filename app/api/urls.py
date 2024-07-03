from rest_framework.routers import DefaultRouter
from .views import EventViewSet, MessageViewSet

event_router = DefaultRouter()
event_router.register(r'events', EventViewSet)

message_router = DefaultRouter()
message_router.register(r'message', MessageViewSet)