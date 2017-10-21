from django.db import models
from django.contrib.auth.models import User,Group
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# Create your models here.
class TPUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_identity = models.CharField(max_length=20, default="TPUser")

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.user.username
    
class Student(TPUser):
    
    def viewcourse(self):
        return