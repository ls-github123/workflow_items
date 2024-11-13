from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import CustomUser
from .tokens import TokenObtainPairSerializer