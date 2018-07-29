from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('tasks', views.tasks, name='tasks'),
    path('tasks/<int:id>', views.tasks_by_id, name='tasks_by_id'),
]