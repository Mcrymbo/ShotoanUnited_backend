from .views import NewsViewSets
from rest_framework.routers import DefaultRouter

news_router = DefaultRouter()
news_router.register(r'news', NewsViewSets)