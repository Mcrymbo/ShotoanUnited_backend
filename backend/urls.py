from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from accounts.views import CustomTokenObtainPairView

admin.site.site_header = "SUK Admin"
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='custom_jwt_create'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('app.urls')),
    path('api/', include('backend.api.urls')),
    path('activate/', include('app.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
