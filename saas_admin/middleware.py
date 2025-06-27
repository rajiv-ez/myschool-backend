from django_tenants.utils import get_tenant
import logging

logger = logging.getLogger(__name__)

class TenantLoggerMiddleware:
    def __init__(self, get_response):
        print("TenantLoggerMiddleware init")
        self.get_response = get_response

    def __call__(self, request):
        print("TenantLoggerMiddleware call")
        tenant = get_tenant(request)
        logger.info(f"🔍 Requête entrante – Schéma actif : {tenant.schema_name}")
        response = self.get_response(request)
        return response
