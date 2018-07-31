from django.http import HttpResponse
from django.shortcuts import (
    render,
    get_object_or_404
)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import viewsets
from rest_framework.response import Response
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

    def list(self, request):
        user = User.objects.get(username=request.user)
        queryset = user.task_set.all()
        serializer = TasksSerializer(
            queryset, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = User.objects.get(username=request.user)
        queryset = user.task_set.all()
        task = get_object_or_404(queryset, pk=pk)
        serializer = TasksSerializer(
            task, 
            context={'request': request}
        )
        return Response(serializer.data)

    def create(self, request):
        user = User.objects.get(username=request.user)
        try:
            user.task_set.create(
                title=request.data['title'],
                content=request.data['content']
            )
        except:
            return Response(None, status=400)
        return Response(None, status=201)


    def partial_update(self, request, pk=None):
        updated = False
        bodyKeys = request.data.keys()
        user = User.objects.get(username=request.user)
        queryset = user.task_set.all()
        task = get_object_or_404(queryset, pk=pk)
        if 'title' in bodyKeys:
            updated = True
            task.title = request.data['title']

        if 'content' in bodyKeys:
            updated = True
            task.content = request.data['content']

        if updated:
            task.save()

        serializer = TasksSerializer(
            task, 
            context={'request': request}
        )
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user = User.objects.get(username=request.user)
        queryset = user.task_set.all()
        task = get_object_or_404(queryset, pk=pk)
        task.delete()
        return Response(None, status=200)
        

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
            return HttpResponse(status = 201)
        except Exception as e:
            return HttpResponse(
                status = 400,
                content_type = 'application/json',
                content = json.dumps({
                    'detail' : 'invalid parameters',
                })
            )
    