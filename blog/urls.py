from .views import BlogViewSets, CategoryViewsets
from rest_framework.routers import DefaultRouter

blog_router = DefaultRouter()
blog_router.register(r"blog", BlogViewSets)

category_router = DefaultRouter()
category_router.register(r"category", CategoryViewsets)
