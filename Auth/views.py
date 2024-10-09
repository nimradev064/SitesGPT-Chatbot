from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.hashers import make_password , check_password
from .models import Auth , ActivationCode
from .serializer import AuthSerializer , LoginSerializer , ActivationCodeSerializer
from .utils import generate_jwt_token  , decode_jwt_token
from rest_framework.permissions import IsAuthenticated 
import pandas as pd
import os
from django.conf import settings
import jwt
from rest_framework.authtoken.models import Token  # Import Token model
from django.shortcuts import get_object_or_404



class RegisterView(ModelViewSet):
    queryset = Auth.objects.all()
    serializer_class = AuthSerializer

    def create(self, request):
        try:
            Username = request.data.get("Username")
            Email = request.data.get("Email")
            Password = request.data.get("Password")

            if Auth.objects.filter(Email=Email).exists():
                return Response({"detail": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            

            hashed_password = make_password(Password)
            register_data = {"Username": Username, "Email": Email, "Password": hashed_password}

            serializer = AuthSerializer(data=register_data)
            if serializer.is_valid():
                user = serializer.save()
                if user is not None:
                    return Response({"detail": "Registered successfully" , "UserID" : user.id}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ActivationCodeView(ModelViewSet):
    queryset = ActivationCode.objects.all()
    serializer_class = ActivationCodeSerializer

    def create(self, request):
        AuthID = request.data.get('AuthID')
        ActivationCode = request.data.get('ActivationCode')

        try:
            # Construct the file path
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, "ActivationCodes.xlsx")
            
            # Read the Excel file
            excelfile = pd.read_excel(file_path)
            excelfile.columns = ['ActivationCode']
            activation_codes = excelfile['ActivationCode'].tolist()  
            if ActivationCode in activation_codes:
                print(ActivationCode)
                # Valid activation code, attempt registration
                register_data = {"AuthID": AuthID, "ActivationCode": ActivationCode}
                serializer = ActivationCodeSerializer(data=register_data)
                
                if serializer.is_valid():
                    serializer.save()
                    return Response({"detail": "Activation Code Verified Successfully"}, status=status.HTTP_200_OK)
                
                return Response({"detail": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # If activation code is not valid, check if AuthID exists and delete if necessary
            auth_instance = Auth.objects.filter(id=AuthID).first()
            if auth_instance is not None:
                auth_instance.delete()
                return Response({"detail": "Invalid Activation Code"}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({"detail": "Activation code not found"}, status=status.HTTP_404_NOT_FOUND)

        except FileNotFoundError:
            return Response({"detail": "ActivationCodes.xlsx file not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def list(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




class Login(ModelViewSet):
    queryset = Auth.objects.all()
    serializer_class = LoginSerializer


    def create(self, request):
        try:
            Email = request.data.get("Email")
            Password = request.data.get("Password")

            LoginUser=Auth.objects.filter(Email=Email).first()
            print(LoginUser)
            if LoginUser is None:
                return Response({"detail" : "User Does not exist"} , status=status.HTTP_400_BAD_REQUEST)
            ID=LoginUser.pk
            DBPassword=LoginUser.Password
            VarifyPassword=check_password(Password , DBPassword)
            if VarifyPassword:
                Token=generate_jwt_token(ID , Email)
                return Response({"detail" : "Login in Sucessfully" , "Token" : Token , "AuthID"  : LoginUser.pk }  , status=200)
            return Response({"detail": "Password does not correct"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def list(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
