from .models import Auth , ActivationCode
from rest_framework import serializers
import re



# class AuthSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Auth
#         fields=['Email' , 'Password' , 'UserName']

#         extra_kwargs = {
#             'Email': {'validators': [serializers.EmailField().run_validation]}
#         }

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ['Username' , 'Email', 'Password']


class LoginSerializer(serializers.Serializer):
    Email = serializers.EmailField(max_length=50, required=True)
    Password = serializers.CharField(write_only=True, required=True)



class ActivationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model=ActivationCode
        fields=['AuthID' , 'ActivationCode']