from django.contrib import admin
from django.urls import path, include
import saas_admin.urls as saas_urls
from saas_admin.views import PublicLoginView

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('api/admin/login/', PublicLoginView.as_view(), name='public-login'),
    path('api/core/', include('core.urls')),
    #path('api/admin/', include('saas_admin.urls')),
    path('api/', include(saas_urls)),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
