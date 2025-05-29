from rest_framework import serializers
from .models import InstitutionAdmin

class InstitutionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionAdmin
        fields = ['id', 'email', 'full_name']
