from rest_framework import serializers
from django.contrib.auth.models import User

from django.db import transaction
from . models import Profile
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

MAX_IMAGE_SIZE = 2 * 1024 * 1024   # 2 MB


class RegisterSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)
    mobile_number = serializers.CharField(max_length=15)
    date_of_birth = serializers.DateField()
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = fields = [
            'username', 'email', 'password',
            'mobile_number', 'date_of_birth', 'profile_picture',
        ]

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_profile_picture(self, image):
        if image.size > MAX_IMAGE_SIZE:
            raise serializers.ValidationError(
                "image size must be less than 2 GB"
            )
        return image
    
    def validate(self, attrs):
        if len(attrs['mobile_number'])<5:
            raise serializers.ValidationError(
                "Invalid Mobile Number"
            )
        return attrs

        
    def create(self, validated_data):
        profile_data = {
            'mobile_number' : validated_data.pop('mobile_number'),
            'date_of_birth': validated_data.pop('date_of_birth'),
            'profile_picture': validated_data.pop('profile_picture', None)
        }
        with transaction.atomic():
            user= User.objects.create_user(**validated_data)
            Profile.objects.create(user=user, **profile_data)

        return user


class LoginUserSerializer(serializers.Serializer):
    username= serializers.CharField()
    password=serializers.CharField(write_only=True)

class ProfieSerializer(serializers.ModelSerializer):
    pass