from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class TenantLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key})


from rest_framework import viewsets
from .models import User, Staff, Tuteur, Eleve, RelationEleveTuteur
from .serializers import (
    UserSerializer, UserLiteSerializer, StaffSerializer, TuteurSerializer,
    EleveSerializer, RelationEleveTuteurSerializer,
    EleveDetailSerializer, StaffDetailSerializer, TuteurDetailSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Staff
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class StaffDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Staff.objects.select_related('user')
    serializer_class = StaffDetailSerializer 

# Tuteur
class TuteurViewSet(viewsets.ModelViewSet):
    queryset = Tuteur.objects.all()
    serializer_class = TuteurSerializer

class TuteurDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tuteur.objects.select_related('user')
    serializer_class = TuteurDetailSerializer

# Eleve
class EleveViewSet(viewsets.ModelViewSet):
    queryset = Eleve.objects.all()
    serializer_class = EleveSerializer

class EleveDetailViewSet(viewsets.ModelViewSet):
    queryset = Eleve.objects.select_related('user')
    serializer_class = EleveDetailSerializer

# RelationEleveTuteur
class RelationEleveTuteurViewSet(viewsets.ModelViewSet):
    queryset = RelationEleveTuteur.objects.all()
    serializer_class = RelationEleveTuteurSerializer