from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('tasks', views.TaskView)

urlpatterns = [
    path('', include(router.urls)),
    path('register', views.register),
    path('login', views.login),
]