from rest_framework.authentication import TokenAuthentication
from .models import InstitutionAdminToken

class InstitutionAdminAuth(TokenAuthentication):
    model = InstitutionAdminToken

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from saas_admin.models import InstitutionAdminToken

class PublicTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if token and token.startswith("Token "):
            key = token.split(" ")[1]
            try:
                token_obj = InstitutionAdminToken.objects.select_related('user').get(key=key)
                return (token_obj.user, None)
            except InstitutionAdminToken.DoesNotExist:
                pass
        return None
