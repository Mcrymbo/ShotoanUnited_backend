from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from accounts.views import CustomTokenObtainPairView

admin.site.site_header = "SUK Admin"
admin.site.index_title = 'Admin'

urlpatterns = [
    path('backend/admin/', admin.site.urls),
    path('backend/auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='custom_jwt_create'),
    path('backend/auth/', include('djoser.urls')),
    path('backend/auth/', include('djoser.urls.jwt')),
    path('backend/auth/', include('djoser.urls.authtoken')),
    path('backend/api/', include('backend.api.urls')),
    path('backend/activate/', include('app.urls')),
    path('', include('app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
