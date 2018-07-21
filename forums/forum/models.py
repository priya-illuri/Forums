from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
# Create your models here.


class Questions(models.Model):
    tag = models.CharField(max_length=50) #attributes
    question_title = models.CharField(max_length=100)
    question = models.CharField(max_length=500)
    created = models.DateTimeField(default=datetime.now())
    last_modified = models.DateTimeField(auto_now=True)#.strftime('%Y-%m-%d %H:%M:%S'))
    no_of_comments=models.IntegerField(default=0)
    username=models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.question_title

class Comments(models.Model):
    comment= models.CharField(max_length=500)
    username=models.CharField(max_length=100)
    commented_on=models.DateTimeField(default=datetime.now())#.strftime('%Y-%m-%d %H:%M:%S'))
    comm_question=models.ForeignKey(Questions, on_delete=models.CASCADE)

    def __str__(self):
        return self.username