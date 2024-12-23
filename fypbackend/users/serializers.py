# from django.contrib.auth.models import User
# from rest_framework import serializers

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email']

# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'email']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         return user

from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Profile  

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['city', 'contact', 'role']  # Include additional fields

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)  # Nested serializer for Profile

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']  # Include Profile data

class RegisterSerializer(serializers.ModelSerializer):
    city = serializers.CharField(write_only=True, required=False)
    contact = serializers.CharField(write_only=True, required=False)
    role = serializers.ChoiceField(choices=[('customer', 'Customer'), ('admin', 'Admin')], write_only=True, default='customer')

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'city', 'contact', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = {
            'city': validated_data.pop('city', None),
            'contact': validated_data.pop('contact', None),
            'role': validated_data.pop('role', 'customer')
        }

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        Profile.objects.create(user=user, **profile_data)
        return user
