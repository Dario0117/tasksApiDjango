from django.db import models

class User(models.Model):
    email = models.CharField(max_length = 200, unique = True)
    name = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    