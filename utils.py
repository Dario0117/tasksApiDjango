import json
import jwt
import os

SECRET_KEY = os.getenv('API_SECRET_KEY', 'SECRET_KEY')

def getDict(byte_str):
    # Parse bytes to string
    raw_str = byte_str.decode('utf-8')
    if raw_str == '':
        return {}
    # Parse string to dict
    return json.loads(raw_str.replace('\'', '\"'))

def hasRequiredParams(param_list, requiredParams):
    params_on_body = param_list.keys()
    for param in requiredParams:
        if not param in params_on_body:
            return False
    return True

def getUserData(headers):
    try:
        token = headers['HTTP_AUTHORIZATION'].replace('\'', '')
        userData = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return userData
    except:
        return False

def genToken(user_data):
    token = jwt.encode(user_data, SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')