from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework.validators import ValidationError
from django.contrib.auth import authenticate


class SignupSerializer(serializers.ModelSerializer):
    def validate(self, data):
        user = User(**data)
        print(data)
        password = data.get("password")
        query = User.objects.all()
        email_exist = query.filter(email=data["email"]).exists()
        if email_exist:
            raise ValidationError("Email has already been used")
        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)
            raise exceptions.ValidationError(
                {"password": serializer_errors["errors"]}
            )
        return data

    class Meta:
        model = User
        fields = ["email", "name", "password"]


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        print(data)
        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('You are not authorized to perform this action')
                else:
                    data['user'] = user
                    
            else:
                raise serializers.ValidationError('Invalid username or password')
        else:
            raise serializers.ValidationError('Email and Password are required')
        return data
            
    class Meta:
        model = User
        fields = ["email", "password"]


class UserSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()
    class Meta:
        model = User
        exclude = ['password']
