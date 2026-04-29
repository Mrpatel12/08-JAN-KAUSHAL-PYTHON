from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title


class Studinfo(models.Model):   
    name = models.CharField(max_length=20)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name
    