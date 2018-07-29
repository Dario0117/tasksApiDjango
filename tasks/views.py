from django.http import HttpResponse
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from .models import User
from utils import (
    getDict,
    hasRequiredParams,
    genToken,
    getUserData,
)

import json

def _validate(request, requiredParams):
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
        'name',
        'password',
    ]
    code = _validate(request, requiredParams)
    if code != 200:
        return HttpResponse(status=code)
    else:
        params = getDict(request.body)
        u = User(
            email = params['email'],
            name = params['name'],
            password = params['password'],
        )
        try:
            u.save()
            token = genToken({
                'email': params['email'],
                'id': u.id
            })
            return HttpResponse(
                status = code,
                content_type = 'application/json',
                content = json.dumps({
                    'error': '',
                    'token': token
                })
            )
        except:
            return HttpResponse(
                status = 400,
                content_type = 'application/json',
                content = json.dumps({
                    'error' : 'email already exists'
                })
            )
            
@csrf_exempt 
def login(request):
    requiredParams = [
        'email',
        'password',
    ]
    code = _validate(request, requiredParams)
    if code != 200:
        return HttpResponse(status=code)
    else:
        params = getDict(request.body)
        try:
            u = User.objects.get(
                email = params['email'],
                password = params['password']
            )
            token = genToken({
                'email': params['email'],
                'id': u.id
            })
            return HttpResponse(
                status = code,
                content_type = 'application/json',
                content = json.dumps({
                    'error': '',
                    'token': token
                })
            )
        except:
            return HttpResponse(
                status = 400,
                content_type = 'application/json',
                content = json.dumps({
                    'error' : 'wrong email or password'
                })
            )

@csrf_exempt
def tasks(request):
    userData = getUserData(request.META)
    if userData:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)

@csrf_exempt
def tasks_by_id(request, id):
    userData = getUserData(request.META)
    if userData:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)