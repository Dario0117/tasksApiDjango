from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import Task
from .serializers import TasksSerializer

class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TasksSerializer