from rest_framework.routers import DefaultRouter
# from app.api.urls import user_router, group_router, event_router
from app.api.urls import event_router, user_router
from django.urls import path, include

router = DefaultRouter()
router.registry.extend(user_router.registry)
# router.registry.extend(group_router.registry)
router.registry.extend(event_router.registry)

urlpatterns = [
    path('', include(router.urls))
]