
from rest_framework import viewsets, permissions
from institutions.models import Client, Domain
from institutions.serializers import ClientSerializer, DomainSerializer
from .serializers import InstitutionAdminSerializer
from .models import InstitutionAdmin, InstitutionAdminToken
from .authentication import InstitutionAdminAuth

class IsSaaSAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'institutionadmin')

class InstitutionAdminViewSet(viewsets.ModelViewSet):
    queryset = InstitutionAdmin.objects.all()
    serializer_class = InstitutionAdminSerializer
    authentication_classes = [InstitutionAdminAuth]
    permission_classes = [IsSaaSAdmin]

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from saas_admin.models import InstitutionAdmin
from django.contrib.auth.hashers import check_password
import logging
logger = logging.getLogger(__name__)

from rest_framework.permissions import AllowAny

from saas_admin.authentication import PublicTokenAuthentication

class PublicLoginView(APIView):
    authentication_classes = [PublicTokenAuthentication]
    permission_classes = [AllowAny]  # ← IMPORTANT
    def post(self, request):
        #raise Exception("🔥 TEST: Ceci est bien PublicLoginView")
        logger.info("✅ PublicLoginView appelée")
        email = request.data.get('email')
        password = request.data.get('password')
        print(f"request.data: {request.data}")
        print(f"Login et password: {email} {password}")

        try:
            user = InstitutionAdmin.objects.get(email=email)
            if check_password(password, user.password):
                token, _ = InstitutionAdminToken.objects.get_or_create(user=user)
                return Response({'token': token.key})
        except InstitutionAdmin.DoesNotExist:
            pass

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
