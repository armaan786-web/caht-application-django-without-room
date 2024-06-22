from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class chat_Group(models.Model):
    members = models.ManyToManyField(User,related_name='member')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class ChatMessage(models.Model):
    message_by = models.ForeignKey(User,on_delete=models.CASCADE) 
    receive_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="receive_by")
    message = models.TextField()
    msg_time = models.DateTimeField(auto_now=True)

