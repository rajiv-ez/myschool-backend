from rest_framework import serializers
from .models import User, Staff, Tuteur, Eleve, RelationEleveTuteur

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserLiteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # 🔑 Important
    class Meta:
        model = User
        exclude = ['password', 'last_login', 'user_permissions', 'groups']

    def create(self, validated_data):
        return User.objects.create_user(password='password', **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# Staff
class StaffSerializer(serializers.ModelSerializer):
    #user = UserLiteSerializer()
    class Meta:
        model = Staff
        fields = '__all__'
        #depth = 1

class StaffDetailSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer()
    class Meta:
        model = Staff
        fields = '__all__'
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        staff = Staff.objects.create(user=user, **validated_data)
        return staff

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        
# Tuteur
class TuteurSerializer(serializers.ModelSerializer):
    #user = UserLiteSerializer()
    class Meta:
        model = Tuteur
        fields = '__all__'
        #depth = 1

class TuteurDetailSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer()
    class Meta:
        model = Tuteur
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        tuteur = Tuteur.objects.create(user=user, **validated_data)
        return tuteur

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# Eleve
class EleveSerializer(serializers.ModelSerializer):
    #user = UserLiteSerializer()
    class Meta:
        model = Eleve
        fields = '__all__'
        #depth = 1

class EleveDetailSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer()
    class Meta:
        model = Eleve
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(password='password', **user_data)
        eleve = Eleve.objects.create(user=user, **validated_data)
        return eleve

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# RelationEleveTuteur
class RelationEleveTuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationEleveTuteur
        fields = '__all__'
        #depth = 1
