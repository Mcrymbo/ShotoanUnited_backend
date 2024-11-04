from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('backend/register/<slug:slug>/', views.register_event, name='register_event'),
]