from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import validate_email
from rest_framework import viewsets
import json
from .models import Task
from .serializers import TasksSerializer
from utils import (
    getDict,
    hasRequiredParams,
)

class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TasksSerializer

def _validate(request, requiredParams, email=True):
    """
        this method return 200 if:
        - method is POST and
        - contentType is application/json and
        - has all required params and
        - email is well formated
    """
    if request.method == 'POST':
        try:
            body = getDict(request.body)
        except:
            return 400
        if (
            request.content_type == 'application/json' 
            and hasRequiredParams(body, requiredParams)
        ):
            if email:
                try:
                    validate_email(body['email'])
                except:
                    return 400
            return 200
        else:
            return 400
    else:
        return 404

@csrf_exempt 
def register(request):
    requiredParams = [
        'email',
        'username',
        'password',
    ]
    code = _validate(request, requiredParams)
    if code != 200:
        return HttpResponse(status=code)
    else:
        params = getDict(request.body)
        try:
            u = User.objects.create_user(
                username = params['username'].lower(),
                email = params['email'],
                password = params['password'],
            )
            u.save()
            token = 'PROVISOINAL_TOKEN'
            return HttpResponse(
                status = 201,
                content_type = 'application/json',
                content = json.dumps({
                    'token': token,
                })
            )
        except Exception as e:
            return HttpResponse(
                status = 400,
                content_type = 'application/json',
                content = json.dumps({
                    'detail' : 'invalid parameters',
                })
            )
            
@csrf_exempt 
def login(request):
    requiredParams = [
        'username',
        'password',
    ]
    code = _validate(request, requiredParams, False)
    if code != 200:
        return HttpResponse(status=code)
    else:
        params = getDict(request.body)
        try:
            user = authenticate(
                username = params['username'].lower(),
                password = params['password']
            )
            print(user)
            if user is None:
                raise ValueError('invalid credentials')
            token = 'PROVISOINAL_TOKEN'
            return HttpResponse(
                status = code,
                content_type = 'application/json',
                content = json.dumps({
                    'token': token,
                })
            )
        except:
            return HttpResponse(
                status = 400,
                content_type = 'application/json',
                content = json.dumps({
                    'detail' : 'wrong username or password',
                })
            )