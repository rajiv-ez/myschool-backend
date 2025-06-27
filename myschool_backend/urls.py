
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/academic/', include('academic.urls')),
    path('api/infrastructure/', include('infrastructure.urls')),
    path('api/hr/', include('hr.urls')),
    #path('api/core/', include('core.urls')),
    path('api/teaching/', include('teaching.urls')),
    path('api/accounts/', include('users.urls')),
    path('api/accounting/', include('accounting.urls')),
    path('api/dms/', include('dms.urls')),
    path('api/library/', include('library.urls')),
    path('api/stocks/', include('stocks.urls')),
    path('api/config/', include('configurations.urls')),
]
