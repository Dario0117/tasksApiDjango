from django.db import models

class User(models.Model):
    email = models.CharField(max_length = 200, unique = True)
    name = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    
class Task(models.Model):
    title = models.CharField(max_length = 200)
    content = models.CharField(max_length = 500)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)