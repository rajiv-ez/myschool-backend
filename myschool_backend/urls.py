
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/academique/', include('academic.urls')),
    path('api/infra/', include('infrastructure.urls')),
    path('api/hr/', include('hr.urls')),
    #path('api/core/', include('core.urls')),
    path('api/teaching/', include('teaching.urls')),
    path('api/accounts/', include('users.urls')),
]
