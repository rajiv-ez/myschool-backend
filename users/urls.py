from users.views import TenantLoginView
from django.urls import path

urlpatterns = [
    path('login/', TenantLoginView.as_view()),
]
