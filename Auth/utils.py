import jwt 
from django.conf import settings
from rest_framework.permissions import BasePermission




def generate_jwt_token(userid , useremail):
    # payload = {
    #     'Email': useremail,
    # }
    # token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    # return token


    payload = {
        'user_id': userid,
        'username': useremail,
        # Add other relevant data to the payload if needed
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}
    except jwt.DecodeError:
        return {'error': 'Invalid token'}



# # import jwt
# # import datetime
# # from django.conf import settings

# # def generate_jwt_token(useremail):
# #     payload = {
# #         'Email': useremail,
# #         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)  # Token expires in 5 minutes
# #     }
# #     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
# #     return token


# # import jwt
# # import datetime
# # from django.conf import settings

# # def generate_jwt_token(useremail):
# #     payload = {
# #         # 'user_id': user_id,  # This should match the USER_ID_FIELD setting
# #         'email': useremail,
# #         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)  # Token expires in 5 minutes
# #     }
# #     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
# #     return token

# import jwt
# import datetime
# import uuid
# from django.conf import settings

# # def generate_jwt_token(useremail, userid):
# #     payload = {
# #         'email': useremail,
# #         'id': userid,  # Adding the user ID to the payload
# #         'token_type': 'access',  # Adding the token type
# #         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),  # Token expires in 5 minutes
# #         'iat': datetime.datetime.utcnow(),  # Issued at time
# #         'jti': str(uuid.uuid4()),  # Unique identifier for the token
# #         'sub': userid  # Using 'sub' for user identification
# #     }
# #     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
# #     return token


# def generate_jwt_token(useremail, userid):
#     payload = {
#         'email': useremail,
#         'id': userid,
#         'token_type': 'access',
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
#         'iat': datetime.datetime.utcnow(),
#         'jti': str(uuid.uuid4()),
#         'sub': userid
#     }
#     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
#     return token



