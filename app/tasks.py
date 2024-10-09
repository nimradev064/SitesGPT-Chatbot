import datetime
from .models import ChatbotFileURL , QA , chatbot , WebsiteFileURL , Chat
from .Crud import uploadfile , textChunks , VectorEmbeddings
from rest_framework.response import Response
from rest_framework import status
import datetime
from django.db import transaction



# @shared_task
# def process_vector_embedding(ChatbotID, Question):

#             ChatbotFileURLInstance = ChatbotFileURL.objects.filter(chatbotID=ChatbotID).first()
#             #  print(ChatbotFileURLInstance)
#             WebsiteFileURLInstance = WebsiteFileURL.objects.filter(chatbotID=ChatbotID).first()
#            # print(WebsiteFileURLInstance)

#             all_chunks = []
#             # print(all_chunks)
#             # Process file paths
#             if ChatbotFileURLInstance is not None:
#                 FilesList = ChatbotFileURLInstance.FilePath
#                # print(FilesList) 
#                 FilesList = eval(FilesList)
#                 for file_path in FilesList:
#                   try:
#                      # print(file_path)
#                       documents = uploadfile(file_path)
#                       Chunks = textChunks(documents)
#                       #print(Chunks)
#                       all_chunks.extend(Chunks)
#                   except Exception as e:
#                       print(f"Error processing file {file_path}: {e}")
#             #print(all_chunks)
#             # Process website URLs
#            # print(WebsiteFileURLInstance)
#             if WebsiteFileURLInstance is not None:
#                # print(WebsiteFileURLInstance)
#                 WebURLsList = WebsiteFileURLInstance.WebURL
#                # print(WebURLsList)
#                 #WebURLsList = eval(WebURLsList)
#                # print(WebURLsList)
#                 for web_url in WebURLsList:
#                    # print(web_url)
#                     documents = uploadfile(web_url)
#                     Chunks = textChunks(documents)
#                     all_chunks.extend(Chunks)

#             print(all_chunks)
#             db = VectorEmbeddings(all_chunks, Question)

#             if db is not None:
#                 try:
#                     print(db)
#                     ChatbotInstance = chatbot.objects.filter(ID=ChatbotID).first()
#                     print(ChatbotInstance)                
#                     if ChatbotInstance:
#                         ChatbotInstance.LastMessageAT = datetime.datetime.now()
#                         ChatbotInstance.chats = ChatbotID
#                         ChatbotInstance.messages += 1
#                         ChatbotInstance.save()

#                         data = {
#                           "Question": Question,
#                            "Answer": db.content  # Replace with your actual answer content
#                           }

#                         ChatInstance = Chat.objects.filter(chatbotID=ChatbotInstance).first()
#                         print(ChatInstance)
#                         if ChatInstance is not None:
#                            QAInstance = QA.objects.filter(chatID=ChatInstance).first()
#                            if QAInstance is not None:
#                             chathistory = QAInstance.QAL 
#                             chathistory.append(data)
#                             QAInstance.QAL = chathistory
#                             QAInstance.save()

#                            else:
#                                QAInstance = QA(chatID=ChatInstance, QAL=[data])
#                                QAInstance.save()
                           
#                            print(db.content)
#                            return Response({"Question": Question, "Answer": db.content}, status=200)
#                         else:

#                            return Response({"Error": "ChatInstance not found"}, status=400)

#                 except Exception as e:
#                     return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
#             else:
#                return Response({"Error": "No embeddings found"}, status=400)
               

# def process_vector_embedding(ChatbotID):
#     try:
#         ChatbotFileURLInstance = ChatbotFileURL.objects.filter(chatbotID=ChatbotID).first()
#         WebsiteFileURLInstance = WebsiteFileURL.objects.filter(chatbotID=ChatbotID).first()

#         all_chunks = []
#         print(ChatbotFileURLInstance)
#         # Process file paths
#         if ChatbotFileURLInstance is not None:
#             FilesList = eval(ChatbotFileURLInstance.FilePath)
#             for file_path in FilesList:
#                 try:
#                     documents = uploadfile(file_path)
#                     Chunks = textChunks(documents)
#                     all_chunks.extend(Chunks)
#                 except Exception as e:
#                     print(f"Error processing file {file_path}: {e}")

#         # Process website URLs
#         if WebsiteFileURLInstance is not None:
#             WebURLsList = WebsiteFileURLInstance.WebURL
#             for web_url in WebURLsList:
#                 try:
#                     documents = uploadfile(web_url)
#                     Chunks = textChunks(documents)
#                     all_chunks.extend(Chunks)
#                 except Exception as e:
#                     print(f"Error processing URL {web_url}: {e}")
        
#         db = VectorEmbeddings(all_chunks , ChatbotID)
#         print(db)
        
#         if db is None :
#             return {"Error": "No embeddings found"}
        
#         return {"Message": "embeddings found Sucessfully"}
#         # if db is not None:
#         #     try:
#         #         ChatbotInstance = chatbot.objects.filter(ID=ChatbotID).first()
#         #         if ChatbotInstance:
#         #             with transaction.atomic():
#         #                 ChatbotInstance.LastMessageAT = datetime.datetime.now()
#         #                 ChatbotInstance.chats = ChatbotID
#         #                 ChatbotInstance.messages += 1
#         #                 ChatbotInstance.save()

#         #                 data = {
#         #                     "Question": Question,
#         #                     "Answer": db['content']  # Extract the content from the db object
#         #                 }

#         #                 ChatInstance = Chat.objects.filter(chatbotID=ChatbotInstance).first()
#         #                 if ChatInstance is not None:
#         #                     QAInstance = QA.objects.filter(chatID=ChatInstance).first()
#         #                     if QAInstance is not None:
#         #                         chathistory = QAInstance.QAL
#         #                         chathistory.append(data)
#         #                         QAInstance.QAL = chathistory
#         #                         QAInstance.save()
#         #                     else:
#         #                         QAInstance = QA(chatID=ChatInstance, QAL=[data])
#         #                         QAInstance.save()
                            
#         #                     return {"Question": Question, "Answer": db['content']}
#         #                 else:
#         #                     return {"Error": "ChatInstance not found"}

#         #     except Exception as e:
#         #         return {"detail": str(e)}
#         # else:
#           # return {"Error": "No embeddings found"}

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return {"Error": "An error occurred during processing"}
