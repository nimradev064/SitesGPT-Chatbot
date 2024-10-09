from django.shortcuts import render , get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import ChatbotFileURL ,  ChatbotDesign , QA ,Email, SMS, chatbot , WebsiteFileURL , Chat , Form , HumanAssistant , ReplySMS , ReplyEmail
from Auth.models import Auth
from .serializers import EmailSerializer, SmsSerializer, ChatbotFileURLSerializers , ChatbotDesignSerializer , ChatSerializer , chatbotserializer , WebURLSerializers , CreateChatSerializer , FormSerializer , HumanAssistantSerializer , EmailReplySerializer , SMSReplySerializer
from .Crud import uploadfile , textChunks ,  VectorEmbeddingsTrueEnable, VectorEmbeddingsFalseEnable, generate_wo_Design 
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import os
from langchain_chroma import Chroma
from django.conf import settings
import ast
from langchain_openai import OpenAIEmbeddings  # Updated import
from rest_framework.decorators import action
import datetime
from rest_framework_simplejwt.tokens import RefreshToken
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client

import logging
from django import forms 
from rest_framework import status
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import imaplib  # Import for IMAP
import smtplib  # Import for SMTP

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.parser import BytesParser
from email.policy import default
from rest_framework import status  # Import for status codes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import jwt
from jwt import DecodeError, ExpiredSignatureError
from time import sleep
from django.db import OperationalError
import os
from django.urls import get_resolver
import project.settings as settings  # Replace with your actual project name
import project.urls as urls          # Replace with your actual project name
from django.conf import settings as django_settings
from django.urls import get_resolver
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail


openai_api_key = os.getenv('openai_api_key')
print(openai_api_key)

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)


class chatbotView(ModelViewSet):
    queryset = chatbot.objects.all()
    serializer_class = chatbotserializer

    def create(self, request):
        try:
            auth_header = request.headers.get('Authorization')

            if not auth_header:
                return Response({"detail": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)
            authHeader=auth_header[:6]
            print(authHeader)
            if auth_header[:6] == "Bearer" :
                token = auth_header.replace("Bearer", "", 1)  
                try:
                    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                    print(decoded_token)
                    AuthID = decoded_token.get("user_id")
                except ExpiredSignatureError:
                    return Response({"detail": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
                except DecodeError:
                    return Response({"detail": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
                
                Avater = request.data.get("Avater")
                AuthInstance = Auth.objects.filter(id=AuthID).first()
                if AuthInstance is None:
                    return Response({"detail": "User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

                Email = AuthInstance.Email
                createAT = datetime.datetime.now()
                data = {
                    "AuthID": AuthID,
                    "Avater": Avater,
                    "AuthEmail": Email,
                    "Role": "Owner",
                    "createAT": createAT,
                    "chats": 0,
                    "messages": 0
                }
                
                serializer = chatbotserializer(data=data)
                if serializer.is_valid():
                    user = serializer.save()
                    if user:
                        return Response({"detail": "Chatbot created successfully", "ChatbotID": user.ID}, status=status.HTTP_201_CREATED)
            
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def list(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk):
        try:
              AuthUser=Auth.objects.filter(id=pk).first()
              print(AuthUser)
              if AuthUser is None:
                return Response({"detail": "User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
           # Filter chatbots for the authenticated user
              chatbot_instance = chatbot.objects.filter(AuthID=AuthUser.id)

              if chatbot_instance.exists():
                 serialized_data = []
                 for auth_instance in chatbot_instance:
        # Retrieve the chatbot design associated with the chatbot instance
                    ChatBotDesignChatbotID = ChatbotDesign.objects.filter(chatbotID=auth_instance).first()
                    if ChatBotDesignChatbotID:
            # Fetch the ChatbotName if the chatbot design exists
                       ChatbotName = ChatBotDesignChatbotID.ChatbotName
            # Serialize the chatbot instance
                       serializer = chatbotserializer(auth_instance)
                       instance_data = serializer.data
            # Include the ChatbotName in the serialized data
                       instance_data['ChatbotName'] = ChatbotName
                       serialized_data.append(instance_data)
                    else:
                       # Serialize the chatbot instance without ChatbotName
                       serializer = chatbotserializer(auth_instance)
                       instance_data = serializer.data

                       serialized_data.append(instance_data)
    
                 response_data = {
                     "chatbot_instance": serialized_data
                   }
                 return Response(response_data, status=status.HTTP_200_OK)
              else:
                return Response({"detail": "No chatbot records found for this user"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class CreateChatbotDesign(ModelViewSet):
    queryset = ChatbotDesign.objects.all()
    serializer_class = ChatbotDesignSerializer

    def create(self, request):
        try:  
            chatbotID_id = request.data.get('chatbotID')
            chatbotIDInstance = chatbot.objects.filter(ID=chatbotID_id).first()
            if chatbotIDInstance is None:
                return Response({"detail": "Chatbot does not exist"}, status=status.HTTP_404_NOT_FOUND)
             
            ChatbotDesignIDInstance = chatbotIDInstance.ID
            ChatBotDesignChatbotID = ChatbotDesign.objects.filter(chatbotID=ChatbotDesignIDInstance).first()
            if ChatBotDesignChatbotID is not None:
                return Response({"detail": f"{chatbotID_id} Chatbot design already exists"}, status=status.HTTP_409_CONFLICT)

            serializer = ChatbotDesignSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"details": "Chatbot design created successfully" }, status=status.HTTP_201_CREATED)
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def list(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def retrieve(self, request, pk):
        try:
            auth_user=Auth.objects.filter(id=pk).first()
            print(auth_user)

            if auth_user is None:
                return Response({"detail": "User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

            # Retrieve the chatbot instance associated with the authenticated user
            chatbot_instance = chatbot.objects.filter(AuthID=auth_user.id)
            print(chatbot_instance)

            if chatbot_instance.exists():
               # Retrieve the chatbot design associated with the chatbot instance
                chatbot_design = ChatbotDesign.objects.filter(chatbotID__in=chatbot_instance).first()
                if chatbot_design is None:
                    return Response({"detail": "Chatbot design does not exist"}, status=status.HTTP_404_NOT_FOUND)

                retrievedesign = ChatbotDesignSerializer(chatbot_design)
                return Response(retrievedesign.data, status=status.HTTP_200_OK)

            else:
                return Response({"detail": "No chatbot records found for this user"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk):
        try:
            data = {
                "ChatbotName": request.data.get("ChatbotName"),
                "ChatbotAssistant": request.data.get("ChatbotAssistant"),
                "ChatbotColor": request.data.get("ChatbotColor"),
                "WidgetIcon": request.data.get("WidgetIcon"),
                "WidgetIconColor": request.data.get("WidgetIconColor"),
                "LogoURL": request.data.get("LogoURL"),
                "Avatar": request.data.get("Avatar"),
                "AvatarURL": request.data.get("AvatarURL"),
                "WelcomeMessage": request.data.get("WelcomeMessage"),
                "UnableRelevantResponse": request.data.get("UnableRelevantResponse"),
                "ToolTipsMessage": request.data.get("ToolTipsMessage"),
                "QuickPrompt": request.data.get("QuickPrompt"),
                "StartTime": request.data.get("StartTime"),
                "EndTime": request.data.get("EndTime"),
                "WorkingDays": request.data.get("WorkingDays"),
                "EmailNotifMessage": request.data.get("EmailNotifMessage")
            }
            
            print(pk)
            chatbot_design = ChatbotDesign.objects.filter(chatbotID_id=pk).first()
            if chatbot_design is None:
                return Response({"detail": "Chatbot design does not exist"}, status=status.HTTP_404_NOT_FOUND)

            update_serializer = ChatbotDesignSerializer(instance=chatbot_design, data=data, partial=True)
            if update_serializer.is_valid():
                update_serializer.save()
                return Response({"detail": "Chatbot design updated successfully"}, status=status.HTTP_200_OK)

            return Response({"detail": update_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self , request , pk):

        try:
            chatbot_design = ChatbotDesign.objects.filter(chatbotID_id=pk).first()
            
            if chatbot_design is None:
                    return Response({"detail": "Chatbot design does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            chatbot_design.delete()
            return  Response({"delete" : f"{chatbot_design.chatbotID} Delete successfully"} , status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def partial_update(self , request):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ChatbotFileURLView(ModelViewSet):
    queryset = ChatbotFileURL.objects.all()
    serializer_class = ChatbotFileURLSerializers

    def create(self, request):
        try:
            FilePath = request.data.get('FilePath')
            chatbotID = request.data.get("chatbotID")
            URLPath = request.data.get("URLPath")


            ChatbotInstance = chatbot.objects.filter(ID=chatbotID).first()
            print(ChatbotInstance)
            if ChatbotInstance is None:
                return Response({"detail": "Chatbot  does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
            
            ChatbotDesignInstance = ChatbotDesign.objects.filter(chatbotID_id=ChatbotInstance.ID).first()
            if ChatbotDesignInstance is None:
                return Response({"detail": "Chatbot  Design does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
            
            print(ChatbotDesignInstance.ID)
            chatbot_dir = f"static/files/{chatbotID}/"
            os.makedirs(chatbot_dir, exist_ok=True)
            
            if FilePath and not URLPath:
                ChatbotFileURLInstance = ChatbotFileURL.objects.filter(chatbotDesignID=ChatbotDesignInstance.ID).first()
                print(ChatbotFileURLInstance)
                if ChatbotFileURLInstance is None:
                    file_paths = []
                    file_path = f"{chatbot_dir}{FilePath}"
                    with open(file_path, 'wb+') as destination:
                        for chunk in FilePath.chunks():
                                destination.write(chunk)
                    file_paths.append(file_path)
                    serializer = ChatbotFileURLSerializers(data={
                        'chatbotID' : chatbotID,
                        'chatbotDesignID': ChatbotDesignInstance.ID,
                        'FilePath': file_paths
                    })

                    if serializer.is_valid():
                        serializer.save()
                        return Response({"detail": "New File Record saved in Chatbot successfully", "FilePathURL": file_paths}, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                else:
                    InitialFilePathList = ChatbotFileURLInstance.FilePath
                    FinalInitialFilePathList = ast.literal_eval(InitialFilePathList)

                    file_path = f"{chatbot_dir}{FilePath}"
                    if file_path in InitialFilePathList:
                            return Response({"detail": f"The file {file_path} already exists in the list."}, status=status.HTTP_400_BAD_REQUEST)
                    with open(file_path, 'wb+') as destination:
                        for chunk in FilePath.chunks():
                            destination.write(chunk)
                    FinalInitialFilePathList.append(file_path)

                    ChatbotFileURLInstance.FilePath = FinalInitialFilePathList
                    ChatbotFileURLInstance.save()

                    return Response({"detail": "File saved successfully", "FilePathURL": FinalInitialFilePathList}, status=status.HTTP_200_OK)
            
            elif not FilePath and URLPath:
                ChatbotWebURLInstance = WebsiteFileURL.objects.filter(chatbotDesignID=ChatbotDesignInstance.ID).first()
                print(ChatbotWebURLInstance)
                if ChatbotWebURLInstance is None:
                    URL_paths = []
                    
                    URL_paths.append(URLPath)
                    
                    print(URL_paths)
                    WebsiteFileURL_data = WebURLSerializers(data={
                        'chatbotID' : chatbotID,
                        'chatbotDesignID': ChatbotDesignInstance.ID,
                        'WebURL': URL_paths
                    })
                    if WebsiteFileURL_data.is_valid():
                        WebsiteFileURL_data.save()
                        return Response({"detail": "URL Save Successfully", "WEBPathURL": URL_paths}, status=status.HTTP_200_OK)
                    return Response({"detail" : WebsiteFileURL_data.errors} , status=status.HTTP_401_UNAUTHORIZED)
                
                InitialURLPathList = ChatbotWebURLInstance.WebURL
                print(type(InitialURLPathList))
                
                if URLPath in InitialURLPathList:
                    return Response({"detail": f"The URL {URLPath} already exists in the list."}, status=status.HTTP_400_BAD_REQUEST)
                
                InitialURLPathList.append(URLPath)

                ChatbotWebURLInstance.WebURL = InitialURLPathList
                ChatbotWebURLInstance.save()

                # Initialize URL_paths with the updated InitialURLPathList to avoid referencing before assignment
                URL_paths = InitialURLPathList

                return Response({"detail" : "URL Save Successfully" , "WEBPathURL": URL_paths} , status=status.HTTP_200_OK)
              
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'], url_path='file-paths')
    def retrieve_file_paths(self, request, pk=None):
        try:
            chatbot_file_url_record = ChatbotFileURL.objects.get(pk=pk)
            file_paths = ast.literal_eval(chatbot_file_url_record.FilePath)

            file_details = []
            for file_path in file_paths:
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    file_size_kb = file_size / 1024  # Convert to KB
                    file_name = os.path.basename(file_path)

                    file_creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %I:%M:%S %p')

                    file_details.append({
                        'file_name': file_name,
                        'file_path': file_path,
                        'file_size': f"{round(file_size_kb, 2)} kb" , 
                        'Last_Update': file_creation_time,

                    })
                else:
                    file_details.append({
                        'file_name': os.path.basename(file_path),
                        'file_path': file_path,
                        'file_size': 'File not found',
                        'Last_Update': "N/A",

                    })

            response_data = {
                'ID': chatbot_file_url_record.ID,
                'FileDetails': file_details,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ChatbotFileURL.DoesNotExist:
            return Response({"detail": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'], url_path='web-urls')
    def retrieve_web_urls(self, request, pk=None):
        try:
            website_file_url_record = WebsiteFileURL.objects.get(pk=pk)
            web_urls = website_file_url_record.WebURL

            response_data = {
                'ID': website_file_url_record.ID,
                'WebURL': web_urls,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except WebsiteFileURL.DoesNotExist:
            return Response({"detail": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['delete'], url_path='delete-file')
    def delete_file(self, request, pk=None):
        try:
            file_name = request.data.get('file_name')
            if not file_name:
                return Response({"detail": "file_name is required"}, status=status.HTTP_400_BAD_REQUEST)

            chatbot_file_url_record = ChatbotFileURL.objects.get(pk=pk)
            file_paths = ast.literal_eval(chatbot_file_url_record.FilePath)

            file_path_to_delete = None
            for file_path in file_paths:
                if os.path.basename(file_path) == file_name:
                    file_path_to_delete = file_path
                    break

            if file_path_to_delete and os.path.exists(file_path_to_delete):
                os.remove(file_path_to_delete)  # Delete the file from the file system
                file_paths.remove(file_path_to_delete)  # Remove the file path from the list
                chatbot_file_url_record.FilePath = str(file_paths)
                chatbot_file_url_record.save()  # Save the updated record

                return Response({"detail": "File deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "File not found or does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except ChatbotFileURL.DoesNotExist:
            return Response({"detail": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['delete'], url_path='delete-url')
    def delete_url(self, request, pk=None):
        try:
            url_to_delete = request.data.get('URLPath')
            print(url_to_delete)
            if not url_to_delete:
                return Response({"detail": "url is required"}, status=status.HTTP_400_BAD_REQUEST)

            website_file_url_record = WebsiteFileURL.objects.get(pk=pk)
            web_urls = website_file_url_record.WebURL

            if url_to_delete in web_urls:
                web_urls.remove(url_to_delete)
                website_file_url_record.WebURL = web_urls
                website_file_url_record.save()  # Save the updated record

                return Response({"detail": "URL deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "URL not found in the list"}, status=status.HTTP_404_NOT_FOUND)

        except WebsiteFileURL.DoesNotExist:
            return Response({"detail": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateChatView(ModelViewSet):
    queryset=Chat.objects.all()
    serializer_class = CreateChatSerializer

    def create(self, request):
        try:
            ChatbotID = request.data.get("chatbotID")

            ChatbotInstance = chatbot.objects.filter(ID=ChatbotID).first()
            
            if ChatbotInstance is None:
                return Response({"detail": "Chatbot  does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
            
            serlializer=CreateChatSerializer(data=request.data)
            if serlializer.is_valid():
                chat_instance = serlializer.save()

                return Response({"detail": "New Chat create successfully" , 'ChatID' : chat_instance.ID }, status=200)
            
            return Response({"detail": serlializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ChatView(ModelViewSet):
    queryset = QA.objects.all()
    serializer_class = ChatSerializer


    def create(self, request):
        try: 
            ChatbotID = request.data.get("ChatbotID")
            Question = request.data.get("Question")
            print("okay")
            ChatbotDesignInstance = ChatbotDesign.objects.filter(chatbotID_id=ChatbotID).first()
            print(ChatbotDesignInstance)
            if ChatbotDesignInstance is None:
                print(ChatbotDesignInstance)
                response=generate_wo_Design(Question)
                return Response({"Question": Question  , "Answer" : response})
   
            Enable=ChatbotDesignInstance.is_enabled
            if Enable == False:
                response=self.processchatNotEnable(ChatbotID ,Question)
                print(response)
                return response
            
            response=self.processchatEnable(ChatbotID ,Question)
            return response
   
        except Exception as e:
             return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def processchatEnable(self, ChatbotID, Question):
        try:
            ChatbotFileURLInstance = ChatbotFileURL.objects.filter(chatbotID=ChatbotID).first()
            WebsiteFileURLInstance = WebsiteFileURL.objects.filter(chatbotID=ChatbotID).first()

            all_chunks = []

            # Process file paths
            if ChatbotFileURLInstance is not None:
                FilesList = eval(ChatbotFileURLInstance.FilePath)
                for file_path in FilesList:
                    try:
                        documents = uploadfile(file_path)
                        Chunks = textChunks(documents)
                        all_chunks.extend(Chunks)
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")

            # Process website URLs
            if WebsiteFileURLInstance is not None:
                WebURLsList = WebsiteFileURLInstance.WebURL
                for web_url in WebURLsList:
                    documents = uploadfile(web_url)
                    Chunks = textChunks(documents)
                    all_chunks.extend(Chunks)
            
            db = VectorEmbeddingsTrueEnable(all_chunks, Question, ChatbotID)
            if db is not None:
                ChatbotInstance = chatbot.objects.filter(ID=ChatbotID).first()
                if ChatbotInstance:
                    ChatbotInstance.LastMessageAT = datetime.datetime.now()
                    ChatbotInstance.chats = ChatbotID
                    ChatbotInstance.messages += 1
                    ChatbotInstance.save()

                    data = {
                        "Question": Question,
                        "Answer": db  # Replace with your actual answer content
                    }

                    ChatInstance = Chat.objects.filter(chatbotID=ChatbotInstance).first()
                    if ChatInstance is not None:
                        QAInstance = QA.objects.filter(chatID=ChatInstance).first()
                        if QAInstance is not None:
                            chathistory = QAInstance.QAL
                            chathistory.append(data)
                            QAInstance.QAL = chathistory
                            QAInstance.save()
                        else:
                            QAInstance = QA(chatID=ChatInstance, QAL=[data])
                            QAInstance.save()
                        
                        return Response({"Question": Question, "Answer": db}, status=200)
                    else:
                        return Response({"Error": "Chat not found"}, status=400)
                else:
                    return Response({"Error": "Chatbot not found"}, status=400)
            else:
                return Response({"Error": "Failed to generate a response from VectorEmbeddingsFalseEnable"}, status=500)

        except Exception as e:
            return Response({"Error": str(e)}, status=500)
            
    def processchatNotEnable(self, ChatbotID, Question):
        try:
            ChatbotFileURLInstance = ChatbotFileURL.objects.filter(chatbotID=ChatbotID).first()
            WebsiteFileURLInstance = WebsiteFileURL.objects.filter(chatbotID=ChatbotID).first()

            all_chunks = []

            if ChatbotFileURLInstance is not None:
                FilesList = eval(ChatbotFileURLInstance.FilePath)
                for file_path in FilesList:
                    try:
                        documents = uploadfile(file_path)
                        Chunks = textChunks(documents)
                        all_chunks.extend(Chunks)
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")

            if WebsiteFileURLInstance is not None:
                WebURLsList = WebsiteFileURLInstance.WebURL
                for web_url in WebURLsList:
                    documents = uploadfile(web_url)
                    Chunks = textChunks(documents)
                    all_chunks.extend(Chunks)
            # print(all_chunks)
            # return Response({"Message": "True"}, status=200)            
            db = VectorEmbeddingsFalseEnable(all_chunks, Question, ChatbotID)
            # return Response({"Message": db}, status=200)            
            if db is not None:
                ChatbotInstance = chatbot.objects.filter(ID=ChatbotID).first()
                if ChatbotInstance:
                    ChatbotInstance.LastMessageAT = datetime.datetime.now()
                    ChatbotInstance.chats = ChatbotID
                    ChatbotInstance.messages += 1
                    ChatbotInstance.save()

                    data = {
                        "Question": Question,
                        "Answer": db  # Replace with your actual answer content
                    }

                    ChatInstance = Chat.objects.filter(chatbotID=ChatbotInstance).first()
                    if ChatInstance is not None:
                        QAInstance = QA.objects.filter(chatID=ChatInstance).first()
                        if QAInstance is not None:
                            chathistory = QAInstance.QAL
                            chathistory.append(data)
                            QAInstance.QAL = chathistory
                            QAInstance.save()
                        else:
                            QAInstance = QA(chatID=ChatInstance, QAL=[data])
                            QAInstance.save()
                        
                        return Response({"Question": Question, "Answer": db}, status=200)
                    else:
                        return Response({"Error": "Chat not found"}, status=400)
                else:
                    return Response({"Error": "Chatbot not found"}, status=400)
            else:
                return Response({"Error": "Failed to generate a response from VectorEmbeddingsFalseEnable"}, status=500)

        except Exception as e:
            return Response({"Error": str(e)}, status=500)


    def retrieve(self, request, pk):
        try:
            # Retrieve the chatbot record with the given primary key
            chatbot_instance = chatbot.objects.filter(ID=pk).first()
            
            if chatbot_instance:

                ChatBotDesignChatbotID = ChatbotDesign.objects.filter(chatbotID=chatbot_instance).first()
                if ChatBotDesignChatbotID is None:
                         return Response({"detail": f"{ChatBotDesignChatbotID.ID} Chatbot design does not  exists"}, status=status.HTTP_409_CONFLICT)
                ChatInstance = Chat.objects.filter(chatbotID=chatbot_instance).first()

                QAInstances = QA.objects.filter(chatID=ChatInstance)

                response_data = {
                    "Chatbot": {
                        "ID": chatbot_instance.ID,
                       "ChatBotName" : ChatBotDesignChatbotID.ChatbotName , 
                        "LastMessageAT": chatbot_instance.LastMessageAT,
                        "chats": chatbot_instance.chats,
                        "messages": chatbot_instance.messages
                    },
                    "QA": []
                }

                for qa_instance in QAInstances:
                    response_data["QA"].append({
                        "QA": qa_instance.QAL
                    })

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# ---------Human Assistant-------
class HumanAssistantButtonView(ModelViewSet):
    queryset = HumanAssistant.objects.all()
    serializer_class = HumanAssistantSerializer

    def create(self, request):
        try:
            chatID = request.data.get('chatID')
            ChatInstance = Chat.objects.filter(ID=chatID).first()
            if ChatInstance is None:
                return Response({"detail": "Chat does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            chatbot_id = ChatInstance.ID  
            print(chatbot_id)         
            ChatbotDesignInstance = ChatbotDesign.objects.filter(ID=chatbot_id).first()
            if ChatbotDesignInstance is None:
                return Response({"detail": "Chatbot Design does not exist"}, status=status.HTTP_404_NOT_FOUND)            

            EnableValue = ChatbotDesignInstance.is_enabled
            if EnableValue is False:
                return Response({"detail": "Human Assistant is not enabled"}, status=status.HTTP_404_NOT_FOUND)
            data = {"chatbotID" : ChatbotDesignInstance.chatbotID.ID , "chatID" : chatbot_id}
            print(data)
            HumanAssistantRecord=HumanAssistantSerializer(data=data)
            if HumanAssistantRecord.is_valid():
                HumanAssistantRecord.save()
                return Response({"detail": "Human Assistant activated"}, status=status.HTTP_200_OK)
            return Response({"detail": "Human Assistant Record Does not save"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---------UserPart----------
class UserFormView(ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def create(self, request):
        
        HumanAssistantID=request.data.get("HumanAssistantID")
        if HumanAssistantID is None:
            return Response({"detail" : "Human Assistant is Not Exist"} , status=status.HTTP_401_UNAUTHORIZED)

        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            form = serializer.save()
            method = request.data.get('method')

            if method == 'SMS':
                self.send_email(form ,method)
                # self.send_sms(form)
            elif method == 'Email':
                self.send_email(form , method)
            elif method == 'All':
                # self.send_sms(form)
                self.send_email(form ,method)
            else:
                return Response({'error': 'Invalid method'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Form sent successfully' , "FormID" : form.ID}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_sms(self, form):
        name = form.Name
        phone_number = form.Phone
        email = form.Email
        subject = form.Subject
        message_body = form.Message

        # Save SMS information in the database without sending the SMS
        SMS.objects.create(
            form=form,
            phone_number=phone_number,
            message_body=message_body,
            message_sid='mock_sid',  # Use a mock SID since the SMS is not being sent
            status='send'        # Set status as 'not_sent' or something relevant
        )

        # Print a message indicating that the SMS was not sent
        print(f"Message not sent, but record saved for: {phone_number}")
     
    
    def send_email(self, form , method):
        name = form.Name
        phone_number = form.Phone
        email = form.Email
        subject = form.Subject
        message_body = form.Message
        receiver_email = email

        try:
            Email.objects.create(
                form=form,
                recipient_email=receiver_email,
                subject=subject,
                message_body=message_body,
                status='Sent',
                method=method
            )

            print("Email sent successfully")

        except smtplib.SMTPAuthenticationError as e:
            print(f"Failed to send email: {e}")
            
            # Save failed email attempt
            Email.objects.create(
                form=form,
                recipient_email="",
                subject=subject,
                message_body=message_body,
                status='Failed'
            )

# ----------SMS+EMail-------------
    @action(detail=False, methods=['get'], url_path='all-messages')
    def get_all_messages(self, request):
        sms_records = SMS.objects.all()
        email_records = Email.objects.all()

        sms_data = [{'phone_number': sms.phone_number, 'message_body': sms.message_body, 'status': sms.status} for sms in sms_records]
        email_data = [{'recipient_email': email.recipient_email, 'subject': email.subject, 'message_body': email.message_body, 'status': email.status} for email in email_records]

        return Response({
            'sms': sms_data,
            'emails': email_data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='reply-email')
    def reply_to_email(self, request, pk=None):
        try:
            # Get the form by primary key (pk)
            form = Form.objects.get(pk=pk)

            # Assuming there's a related Email instance for this form, adjust according to your model relationships
            email_instance = Email.objects.filter(form=form).first()  # Get the first email related to the form

            if not email_instance:
                return Response({'error': 'No email found for this form.'}, status=status.HTTP_404_NOT_FOUND)

            # Get the recipient's email from the Email instance
            target_email = email_instance.recipient_email

            # Ensure the admin email is used for sending
            admin_email = 'Sitesgptchatbot@gmail.com'  # Admin email

            # Get the reply message from the request
            reply_message = request.data.get('message')
            if not reply_message:
                return Response({'error': 'Message content is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Sending the email using Django's send_mail function
            try:
                send_mail(
                    subject=f"Reply to your form submission - {email_instance.subject}",
                    message=reply_message,
                    from_email=admin_email,
                    recipient_list=[target_email],
                    fail_silently=False,
                )

                # Save the reply in the database
                ReplyEmail.objects.create(
                    EmailID=email_instance,  # Pass the Email instance here
                    recipient_email=target_email,
                    subject=f"Reply: {email_instance.subject}",
                    reply_body=reply_message,
                    status='Sent',
                )

                return Response({'message': 'Reply sent and saved successfully'}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': f"Failed to send reply: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Form.DoesNotExist:
            return Response({'error': 'Form not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['post'])
    def SMSReply(self, request, pk=None):
        try:
            # Get the form by primary key (pk)
            form = Form.objects.get(pk=pk)

            # Get the related SMS instance for the form (adjust according to your relationships)
            sms_instance = SMS.objects.filter(form=form).first()  # Fetch the SMS related to the form

            if not sms_instance:
                return Response({'error': 'No SMS found for this form.'}, status=status.HTTP_404_NOT_FOUND)

            # Extract the original phone number from the SMS instance
            original_phone_number = sms_instance.phone_number

            # The reply body from the request payload
            reply_body = request.data.get('message', '')

            # Twilio credentials (Ensure to keep your credentials secure)
            account_sid = 'ACec6747ab839821d0c9ae9580083017fd'
            auth_token = '13e9a79e98057da19f13c2e14755ce29'

            # Initialize Twilio Client
            client = Client(account_sid, auth_token)

            # The phone number from which the reply will be sent (Twilio number)
            from_number = '+14806305939'  # Your Twilio number
            
            # The phone number retrieved from the form to which the reply will be sent
            to_number = original_phone_number

            try:
                # Send the SMS reply using Twilio
                message = client.messages.create(
                    body=f"Reply:\n{reply_body}",
                    from_=from_number,
                    to=to_number
                )

                # Save the SMS reply details in the database
                ReplySMS.objects.create(
                    SMSID=sms_instance,  # Pass the SMS instance here
                    phone_number=to_number,
                    reply_body=message.body,
                    message_sid=message.sid,
                    status=message.status
                )

                print(f"Reply SMS sent with SID: {message.sid}")

                return Response({'message': 'SMS reply sent and saved successfully'}, status=status.HTTP_200_OK)

            except Exception as e:
                print(f"Failed to send SMS reply: {e}")
                return Response({'error': 'Failed to send SMS reply'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Form.DoesNotExist:
            return Response({'error': 'Form not found.'}, status=status.HTTP_404_NOT_FOUND)

    

    @action(detail=True, methods=['delete'], url_path='delete-sms')
    def delete_sms(self, request, pk=None):
        try:
            # Get the form by primary key (pk)
            form = Form.objects.get(pk=pk)

            # Get the related SMS instance for the form
            sms_instance = SMS.objects.filter(form=form).first()

            if not sms_instance:
                return Response({'error': 'No SMS found for this form.'}, status=status.HTTP_404_NOT_FOUND)

            # Delete the SMS instance
            sms_instance.delete()

            return Response({'message': 'SMS deleted successfully'}, status=status.HTTP_200_OK)

        except Form.DoesNotExist:
            return Response({'error': 'Form not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'], url_path='delete-email')
    def delete_email(self, request, pk=None):
        try:
            # Get the form by primary key (pk)
            form = Form.objects.get(pk=pk)

            # Get the related Email instance for the form
            email_instance = Email.objects.filter(form=form).first()

            if not email_instance:
                return Response({'error': 'No Email found for this form.'}, status=status.HTTP_404_NOT_FOUND)

            # Delete the Email instance
            email_instance.delete()

            return Response({'message': 'Email deleted successfully'}, status=status.HTTP_200_OK)

        except Form.DoesNotExist:
            return Response({'error': 'Form not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# ----------EmailDashboard-------
class EmailDashboard(ModelViewSet):

    queryset = Email.objects.all()
    serializer_class = EmailSerializer


# ------------SmsDashboard-------
class SmsDashboard(ModelViewSet):
    queryset = SMS.objects.all()
    serializer_class = SmsSerializer 
# -------AdminPart-------


class AdminFormView(ModelViewSet):
    
    # 1. Endpoint to fetch all ReplySMS records
    @action(detail=False, methods=['get'], url_path='fetch-sms-replies')
    def fetch_replysms(self, request):
        sms_replies = ReplySMS.objects.all()
        serializer = SMSReplySerializer(sms_replies, many=True)
        return Response(serializer.data)

    # 2. Endpoint to fetch all ReplyEmail records
    @action(detail=False, methods=['get'], url_path='fetch-email-replies')
    def fetch_replyemail(self, request):
        email_replies = ReplyEmail.objects.all()
        serializer = EmailReplySerializer(email_replies, many=True)
        return Response(serializer.data)

    # 3. Endpoint to fetch all ReplyEmail and ReplySMS records combined
    @action(detail=False, methods=['get'], url_path='fetch-all-replies')
    def fetch_all_replies(self, request):
        sms_replies = ReplySMS.objects.all()
        email_replies = ReplyEmail.objects.all()

        # Serializing both SMS and Email replies
        sms_serializer = SMSReplySerializer(sms_replies, many=True)
        email_serializer = EmailReplySerializer(email_replies, many=True)

        # Combining the results
        combined_results = {
            'sms_replies': sms_serializer.data,
            'email_replies': email_serializer.data
        }

        return Response(combined_results)

class LogoutView(ModelViewSet):

    def create(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

   
