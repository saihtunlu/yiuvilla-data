from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login-/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/login-/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('account.urls')),
    path('api/', include('rest_registration.api.urls')),
    path('api/', include('permission.urls')),
    path('api/', include('file.urls')),
    path('api/', include('import.urls')),
    path('api/', include('sale.urls')),
    path('api/', include('customer.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
