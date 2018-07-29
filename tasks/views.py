from django.http import HttpResponse
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from .models import (
    User,
    Task,
)
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

def handle_tasks_post(body, user_data):
    requiredParams = [
        'title',
        'content',
    ]
    if hasRequiredParams(body, requiredParams):
        user = User.objects.get(
            id = user_data['id'],
            email = user_data['email'],
        )
        t = user.task_set.create(
            title = body['title'],
            content = body['content'],
        )
        return HttpResponse(
            status = 201,
            content_type = 'application/json',
            content = json.dumps({
                'error': '',
                'id_task': t.id
            })
        )
    else:
        return HttpResponse(status=400)

def handle_tasks_get(user_data):
    user = User.objects.get(
        id = user_data['id'],
        email = user_data['email'],
    )
    tasks = user.task_set.all().values(
        'id',
        'title',
        'content',
    )
    return HttpResponse(
        status = 200,
        content_type = 'application/json',
        content = json.dumps({
            'error': '',
            'tasks': list(tasks)
        })
    )

def handle_tasks_get_by_id(user_data, task_id):
    try:
        task = Task.objects.get(
            id = task_id,
            owner_id = user_data['id'],
        )
        return HttpResponse(
            status = 200,
            content_type = 'application/json',
            content = json.dumps({
                'error': '',
                'task': task.toDict()
            })
        )
    except:
        return HttpResponse(
            status = 404,
            content_type = 'application/json',
            content = json.dumps({
                'error' : 'task does not exists',
                'task': '',
            })
        )

@csrf_exempt
def tasks(request):
    userData = getUserData(request.META)
    if userData:
        if request.method == 'POST' and request.content_type == 'application/json':
            body = getDict(request.body)
            return handle_tasks_post(body, userData)
        elif request.method == 'GET':
            return handle_tasks_get(userData)
        elif request.method == 'PUT' and request.content_type == 'application/json':
            pass
        elif request.method == 'PATCH' and request.content_type == 'application/json':
            pass
        elif request.method == 'DELETE':
            pass
        else:
            return HttpResponse(status=404)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)

@csrf_exempt
def tasks_by_id(request, id):
    userData = getUserData(request.META)
    if userData:
        if request.method == 'GET':
            return handle_tasks_get_by_id(userData, id)
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=403)