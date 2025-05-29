from django_tenants.middleware.main import TenantMainMiddleware
from django.utils.deprecation import MiddlewareMixin
import environ

env = environ.Env()
environ.Env.read_env()

class BypassTenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host().split(':')[0]
        if host == env('HOST_NAME', default='localhost'):
            request.tenant = None  # Bypass tenant resolution
        else:
            return TenantMainMiddleware().process_request(request)
