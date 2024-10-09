# from langchain_community.document_loaders.csv_loader import CSVLoader
# from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, UnstructuredPowerPointLoader, UnstructuredExcelLoader, WebBaseLoader
# from langchain_openai import OpenAIEmbeddings  # Updated import
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores.chroma import Chroma
# from langchain_openai import ChatOpenAI
# import os 
# from rest_framework import status
# from langchain_community.document_loaders import UnstructuredHTMLLoader
# from dotenv import load_dotenv


# load_dotenv()


# # # Access the environment variable
# # openai_api_key = os.getenv("openai_api_key")
# # if not openai_api_key:
# #     raise ValueError("OpenAI API key not found in environment variables")

# #embeddings = OpenAIEmbeddings(openai_api_key="sk-proj-vvj1NAr8SpVDaJUin5JCT3BlbkFJcc7WT3pBiHfhLYad3yVw")

# embeddings = OpenAIEmbeddings(openai_api_key="sk-proj-y99IZKF1wm7RP8LNrXTHT3BlbkFJFsixwoUdfdodMuzczisE")

# # def uploadfile(file_path):
# #     try:
# #         print(file_path)
# #         if file_path.startswith(('http://', 'https://', 'www.')):
# #             print("Loading from website:", file_path)
# #             loader = WebBaseLoader(file_path) 
# #         else:
# #             file_name = file_path.split('/')[-1]
# #             file_extension = file_name.split(".")[-1].lower()
# #             loader = None  
# #             if file_extension == 'pdf':
# #                 loader = PyPDFLoader(file_path)
# #             elif file_extension == 'csv':
# #                 loader = CSVLoader(file_path, encoding="utf-8", csv_args={'delimiter': ','})
# #             elif file_extension in ['doc', 'docx']:
# #                 loader = Docx2txtLoader(file_path)
# #             elif file_extension == 'txt':
# #                 loader = TextLoader(file_path)
# #             elif file_extension in ['ppt' , 'pptx']:
# #                 loader = UnstructuredPowerPointLoader(file_path)
# #             elif file_extension in ['xlsx' , 'xls']:
# #                 loader = UnstructuredExcelLoader(file_path)
# #             elif file_extension == 'html':
# #                 loader = UnstructuredHTMLLoader(file_path)
# #             else:
# #                 return Response({"detail":"Unsupported file type: {}".format(file_extension)} ,status=status.HTTP_400_BAD_REQUEST )       
# # #        print(loader)
# #         documents = loader.load()
# #         return documents
    
# #     except Exception as e:
# #         print(f"An error occurred: {e}")
# #         return None





# # def textChunks(documents):
# #     try:
# #         text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
# #         text_chunks = text_splitter.split_documents(documents)
# #         return text_chunks
# #     except Exception as e:
# #         print(f"An error occurred: {e}")
# #         return None



# # def VectorEmbeddings(chunks , query):
# #     try:
# #        # print(chunks)
# #        # Filter out any chunks with None as page_content
# #         valid_chunks = [chunk for chunk in chunks if chunk.page_content is not None]
# #        # print(valid_chunks)
# #         if not valid_chunks:
# #             return {"error": "No valid documents to process."}
# #        # print(valid_chunks)
# #       # Initialize vector store
# #         vector_storage = Chroma(persist_directory="vectordb", embedding_function=embeddings)

# #         # Add valid chunks to vector store
# #         vector_storage.add_documents(valid_chunks)

# #         # Perform similarity search
# #         docs = vector_storage.similarity_search(query, k=3)
# #         print(docs)
               
# #         # print(chunks)
# #         # Initialize vector store
# #        # vector_storage = Chroma(persist_directory="vectordb", embedding_function=embeddings)
# #        # print(vector_storage)
# #         # Add chunks to vector store
# #        # vector_storage.add_documents(valid_chunks)

# #         # docs = vector_storage.similarity_search(query, k=3)
# #         # print(docs)
# #         content = "\n".join([x.page_content for x in docs])

# #         qa_prompt = "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer.\n----------------"
# #         input_text = qa_prompt + "\nContext:" + content + "\nUser question:\n" + query

# #         llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key="sk-proj-y99IZKF1wm7RP8LNrXTHT3BlbkFJFsixwoUdfdodMuzczisE")

# #         # Prepare the input as a list of messages
# #         messages = [{"role": "system", "content": input_text}]

# #         # Get the response from the LLM
# #         response = llm.invoke(messages)

# #         return response
# #     except Exception as e:
# #         print(f"An error occurred: {e}")
# #         return None

# # Function to handle file uploads and load content
# def uploadfile(file_path):
#     try:
#         if file_path.startswith(('http://', 'https://', 'www.')):
#             loader = WebBaseLoader(file_path) 
#         else:
#             file_name = file_path.split('/')[-1]
#             file_extension = file_name.split(".")[-1].lower()
#             loader = None  
#             if file_extension == 'pdf':
#                 loader = PyPDFLoader(file_path)
#             elif file_extension == 'csv':
#                 loader = CSVLoader(file_path, encoding="utf-8", csv_args={'delimiter': ','})
#             elif file_extension in ['doc', 'docx']:
#                 loader = Docx2txtLoader(file_path)
#             elif file_extension == 'txt':
#                 loader = TextLoader(file_path)
#             elif file_extension in ['ppt' , 'pptx']:
#                 loader = UnstructuredPowerPointLoader(file_path)
#             elif file_extension in ['xlsx' , 'xls']:
#                 loader = UnstructuredExcelLoader(file_path)
#             elif file_extension == 'html':
#                 loader = UnstructuredHTMLLoader(file_path)
#             else:
#                 return {"detail":"Unsupported file type: {}".format(file_extension), "status": status.HTTP_400_BAD_REQUEST} 

#         documents = loader.load()
#         return documents
    
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# # Function to split text into chunks
# def textChunks(documents):
#     try:
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
#         text_chunks = text_splitter.split_documents(documents)
#         return text_chunks
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# # # Function to generate vector embeddings
# # def VectorEmbeddings(chunks):
# #     try: 

# #         valid_chunks = [chunk for chunk in chunks if chunk.page_content is not None]
# #         if not valid_chunks:
# #             return {"error": "No valid documents to process."}

# #         vector_storage = Chroma(persist_directory="vectordb", embedding_function=embeddings)
# #         vector_storage.add_documents(valid_chunks)
# #         # docs = vector_storage.similarity_search(query, k=3)

# #         # content = "\n".join([x.page_content for x in docs])
        
# #         return {"Vectordb" : vector_storage}    
    
    
# #         # qa_prompt = "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer.\n----------------"
# #         # input_text = qa_prompt + "\nContext:" + content + "\nUser question:\n" + query

# #         # llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key="sk-proj-y99IZKF1wm7RP8LNrXTHT3BlbkFJFsixwoUdfdodMuzczisE")
# #         # messages = [{"role": "system", "content": input_text}]
# #         # response = llm.invoke(messages)
# #         # print(response)
# #         # return {"content": response}
# #     except Exception as e:
# #         print(f"An error occurred: {e}")
# #         return None



# def VectorEmbeddings(chunks , ChatbotID):
#     try:
#         valid_chunks = [chunk for chunk in chunks if chunk.page_content is not None]
#         if not valid_chunks:
#             return {"error": "No valid documents to process."}

#         vector_storage = Chroma(persist_directory=f"vectordb/{ChatbotID}", embedding_function=embeddings)
#         vector_storage.add_documents(valid_chunks)
        
#         return {"Vectordb": vector_storage}    
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return {"error": str(e)}
    




# def generate_response(vector_storage , query):
#     try:
#         docs = vector_storage.similarity_search(query, k=3)
#         print(docs)
#         content = "\n".join([x.page_content for x in docs])

#         qa_prompt = "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer.\n----------------"
#         input_text = qa_prompt + "\nContext:" + content + "\nUser question:\n" + query

#         llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key="sk-proj-y99IZKF1wm7RP8LNrXTHT3BlbkFJFsixwoUdfdodMuzczisE")
#         messages = [{"role": "system", "content": input_text}]
#         response = llm.invoke(messages)
#         response=response.content
#         return response
    
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return {"error": str(e)}
    

# def generate_rw_Design(query):
#     try:

#         qa_prompt = "Use the following pieces of context to answer the user's question. If you don't have sufficient information to provide an accurate answer, simply state that you don't know, and avoid making up information."
#         input_text = qa_prompt  + "\nUser question:\n" + query

#         llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key="sk-proj-y99IZKF1wm7RP8LNrXTHT3BlbkFJFsixwoUdfdodMuzczisE")
#         messages = [{"role": "system", "content": input_text}]
#         response = llm.invoke(messages)
#         response=response.content
#         return response

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return {"error": str(e)}



import faiss
import numpy as np
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, UnstructuredPowerPointLoader, UnstructuredExcelLoader, WebBaseLoader
from langchain_openai import OpenAIEmbeddings  # Updated import
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
import os 
from rest_framework import status
from langchain_community.document_loaders import UnstructuredHTMLLoader
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('openai_api_key')
print(openai_api_key)

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

def uploadfile(file_path):
    try:
        if file_path.startswith(('http://', 'https://', 'www.')):
            loader = WebBaseLoader(file_path) 
        else:
            file_name = file_path.split('/')[-1]
            file_extension = file_name.split(".")[-1].lower()
            loader = None  
            if file_extension == 'pdf':
                loader = PyPDFLoader(file_path)
            elif file_extension == 'csv':
                loader = CSVLoader(file_path, encoding="utf-8", csv_args={'delimiter': ','})
            elif file_extension in ['doc', 'docx']:
                loader = Docx2txtLoader(file_path)
            elif file_extension == 'txt':
                loader = TextLoader(file_path , encoding = 'UTF-8')
            elif file_extension in ['ppt' , 'pptx']:
                loader = UnstructuredPowerPointLoader(file_path)
            elif file_extension in ['xlsx' , 'xls']:
                loader = UnstructuredExcelLoader(file_path)
            elif file_extension == 'html':
                loader = UnstructuredHTMLLoader(file_path)
            else:
                return {"detail":"Unsupported file type: {}".format(file_extension), "status": status.HTTP_400_BAD_REQUEST} 

        documents = loader.load()
        return documents
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def textChunks(documents):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=160)
        text_chunks = text_splitter.split_documents(documents)
        return text_chunks
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def VectorEmbeddingsTrueEnable(chunks ,query ,ChatbotID):
    try:
        valid_chunks = [chunk for chunk in chunks if chunk.page_content is not None]
        if not valid_chunks:
            return {"error": "No valid documents to process."}

        # Step 1: Initialize embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vectors = [embeddings.embed_query(chunk.page_content) for chunk in valid_chunks]
        vector_matrix = np.array(vectors)

        # Step 2: Set up FAISS index
        d = vector_matrix.shape[1]
        index = faiss.IndexFlatL2(d)  # L2 distance (Euclidean)
        index.add(vector_matrix)

        # Step 3: Perform a similarity search to retrieve the top k relevant documents
        query_vector = embeddings.embed_query(query)
        distances, indices = index.search(np.array([query_vector]), k=3)
        relevant_docs = [valid_chunks[i].page_content for i in indices[0]]
        content = "\n".join(relevant_docs)
        print(content)  # For debugging purposes

        # Step 4: Construct a refined and detailed prompt
        qa_prompt = (
            "Use the following pieces of context to answer the user's questions in a helpful, friendly, and clever manner. "
            "If the context directly answers the user's questions, provide clear, precise, and relevant answers using the exact details available, "
            "without speculation or unnecessary generalizations. "
            "Ensure each question is addressed individually with a clear and thoughtful focus, making the conversation both engaging and informative. "
            "If the context does not contain the answer, simply state that you don't have the knowledge of this question.And Advise the user to contact the Human Assistant for further information."
        )

        # Step 5: Combine the context and user query into the input text
        input_text = f"{qa_prompt}\n\nContext:\n{content}\n\nUser question:\n{query}"

        # Step 6: Set up the language model with the given parameters
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)

        # Step 7: Prepare the message payload for the model
        messages = [{"role": "system", "content": input_text}]

        # Step 8: Invoke the model and get the response
        response = llm.invoke(messages)
        response_text = response.content

        return response_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}   
    
def VectorEmbeddingsFalseEnable(chunks, query, ChatbotID):
    try:
        valid_chunks = [chunk for chunk in chunks if chunk.page_content is not None]
        if not valid_chunks:
            return {"error": "No valid documents to process."}

        # Step 1: Initialize embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vectors = [embeddings.embed_query(chunk.page_content) for chunk in valid_chunks]
        vector_matrix = np.array(vectors)

        # Step 2: Set up FAISS index
        d = vector_matrix.shape[1]
        index = faiss.IndexFlatL2(d)  # L2 distance (Euclidean)
        index.add(vector_matrix)

        # Step 3: Perform a similarity search to retrieve the top k relevant documents
        query_vector = embeddings.embed_query(query)
        distances, indices = index.search(np.array([query_vector]), k=3)
        relevant_docs = [valid_chunks[i].page_content for i in indices[0]]
        content = "\n".join(relevant_docs)
        print(content)  # For debugging purposes

        # Step 4: Construct a refined and detailed prompt
        qa_prompt = (
            "Use the following pieces of context to answer the user's questions in a helpful, friendly, and clever manner. "
            "If the context directly answers the user's questions, provide clear, precise, and relevant answers using the exact details available, "
            "without speculation or unnecessary generalizations. "
            "Ensure each question is addressed individually with a clear and thoughtful focus, making the conversation both engaging and informative. "
            "If the context does not contain the answer, simply state that you don't have the knowledge of this question."
        )

        # Step 5: Combine the context and user query into the input text
        input_text = f"{qa_prompt}\n\nContext:\n{content}\n\nUser question:\n{query}"

        # Step 6: Set up the language model with the given parameters
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)

        # Step 7: Prepare the message payload for the model
        messages = [{"role": "system", "content": input_text}]

        # Step 8: Invoke the model and get the response
        response = llm.invoke(messages)
        response_text = response.content

        return response_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}   
# def VectorEmbeddingsFalseEnable(chunks ,query ,ChatbotID):
#     try:
#         valid_chunks = [chunk for chunk in chunks if chunk.page_content is not None]
#         if not valid_chunks:
#             return {"error": "No valid documents to process."}
        
#         # Step 1: Initialize vector storage and add documents
#         vector_storage = Chroma(persist_directory=f"vectordb/{ChatbotID}", embedding_function=embeddings)
#         vector_storage.add_documents(valid_chunks)

#         # Step 2: Perform a similarity search to retrieve the top k relevant documents
#         docs = vector_storage.similarity_search(query, k=3)
#         content = "\n".join([x.page_content for x in docs])
#         print(content)  # For debugging purposes

#         # Step 3: Construct a refined and detailed prompt
#         qa_prompt = (
#             "Use the following pieces of context to answer the user's questions in a helpful, friendly, and clever manner. "
#             "If the context directly answers the user's questions, provide clear, precise, and relevant answers using the exact details available, "
#             "without speculation or unnecessary generalizations. "
#             "Ensure each question is addressed individually with a clear and thoughtful focus, making the conversation both engaging and informative. "
#             "If the context does not contain the answer, simply state that you don't have the knowledge of this question."
#         )

#         # Step 4: Combine the context and user query into the input text
#         input_text = f"{qa_prompt}\n\nContext:\n{content}\n\nUser question:\n{query}"

#         # Step 5: Set up the language model with the given parameters
#         llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)

#         # Step 6: Prepare the message payload for the model
#         messages = [{"role": "system", "content": input_text}]

#         # # Step 7: Invoke the model and get the response
#         # response = llm.invoke(messages)
#         # response_text = response.content

#         # vector_storage = Chroma(persist_directory=f"vectordb/{ChatbotID}", embedding_function=embeddings)
#         # vector_storage.add_documents(valid_chunks)
#         # docs = vector_storage.similarity_search(query, k=3)
#         # content = "\n".join([x.page_content for x in docs])
#         # print(content)
#         # # Step 2: Construct a refined and detailed prompt
#         # qa_prompt = (
#         #     "Use the following pieces of context to answer the user's questions in a helpful, friendly, and clever manne. If the context directly answers the user's questions, provide clear, precise, and relevant answers using the exact details available, without speculation or unnecessary generalizations. Ensure each question is addressed individually with a clear and thoughtful focus, making the conversation both engaging and informative."
#         # )

#         # # Step 3: Combine the context and user query into the input text
#         # input_text = f"{qa_prompt}Context:\n{content}\n\nUser question:\n{query}"

#         # # Step 4: Set up the language model with the given parameters
#         # llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)

#         # # Step 5: Prepare the message payload for the model
#         # messages = [{"role": "system", "content": input_text}]
#         # docs = vector_storage.similarity_search(query, k=3)
#         # print(docs)
#         # content = "\n".join([x.page_content for x in docs])

#         # qa_prompt = "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't Have the Knowledge of  this question, don't try to make up an answer.\n----------------"
#         # input_text = qa_prompt + "\nContext:" + content + "\nUser question:\n" + query

#         # llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)
#         # messages = [{"role": "system", "content": input_text}]
#         response = llm.invoke(messages)
#         response = response.content
#         return response
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return {"error": str(e)}

# def VectorEmbeddings(chunks , ChatbotID):
#     try:
#         valid_chunks = [chunk for chunk in chunks if chunk.page_content is not None]
#         if not valid_chunks:
#             return {"error": "No valid documents to process."}

#         vector_storage = Chroma(persist_directory=f"vectordb/{ChatbotID}", embedding_function=embeddings)
#         vector_storage.add_documents(valid_chunks)
#         return {"Vectordb": vector_storage}    
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return {"error": str(e)}
    
# def generate_response(vector_storage , query):
#     try:
#         docs = vector_storage.similarity_search(query, k=3)
#         print(docs)
#         content = "\n".join([x.page_content for x in docs])

#         qa_prompt = "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer.\n----------------"
#         input_text = qa_prompt + "\nContext:" + content + "\nUser question:\n" + query

#         llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)
#         messages = [{"role": "system", "content": input_text}]
#         response = llm.invoke(messages)
#         response = response.content
#         return response
    
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return {"error": str(e)}
    
def generate_wo_Design(query):
    try:
        qa_prompt = "Answer the User's Question Direct from AI Assistant."
        input_text = qa_prompt  + "\nUser question:\n" + query

        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)
        messages = [{"role": "system", "content": input_text}]
        response = llm.invoke(messages)
        response = response.content
        print(response)
        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}


# def generate_HumanAsistant_response(vector_storage , query):
#     try:
#         docs = vector_storage.similarity_search(query, k=3)
#         content = "\n".join([x.page_content for x in docs])
#         print(content)
#         # qa_prompt = "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that currently I don’t have the information on that question gives the Response, don't try to make up an answer.\n----------------"
#         # input_text = qa_prompt + "\nContext:" + content + "\nUser question:\n" + query
#         qa_prompt = "Use the following pieces of context to answer the user's question. If the context does not provide sufficient information to answer the question accurately, respond with 'Currently, I don't have the information on that question.' Do not attempt to make up an answer.\n----------------"
#         input_text = qa_prompt + "\nContext:" + content + "\nUser question:\n" + query


#         llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=openai_api_key)
#         messages = [{"role": "system", "content": input_text}]
#         response = llm.invoke(messages)
#         print(response)
#         response = response.content
#         return response
    
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return {"error": str(e)}

# def generate_HumanAsistant_response(vector_storage, query):
#     try:

#         print(vector_storage)
#         # Fetch relevant documents from the vector storage
#         docs = vector_storage.similarity_search(query, k=3)
#         print(docs)
#         content = "\n".join([x.page_content for x in docs])
  
#         print(content)
#         qa_prompt = (
#         "Use the following pieces of context to answer the user's question. "
#         "If you find the answer, provide a simple and direct response. "
#         "If the answer is not available in the content, say 'I don't have Knowledge about this Question.' "
#         "Advise the user to contact the Human Assistant for further information.\n"
#         "----------------"
#          )
#         input_text = qa_prompt + "\nContext:" + content + "\nUser question:\n" + query

#         # Initialize the language model
#         llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)
#         print(llm)
#         messages = [{"role": "system", "content": input_text}]
#         response = llm.invoke(messages)
#         print(response)

#         # Extract and return the response content
#         response = response.content
#         return response

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return {"error": str(e)}

