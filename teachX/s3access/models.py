from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
# Create your models here.

class devices(models.Model):
    device_id = models.TextField(blank=False,unique=True)
    username = models.ForeignKey(User, to_field="username",unique=True,default=None,null=True,on_delete=models.SET_NULL)
    name = models.TextField(null=True,default=None,blank=True)
    address = models.TextField(null=True,default=None,blank=True)
    is_enable = models.BooleanField(default=True)
    updated_at =models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return str(self.device_id)
    class Meta:
        verbose_name_plural = "devices"


class classes(models.Model):
    Class = models.IntegerField(blank=False,unique=True)
    image_url=models.URLField(null=True)
    path = models.TextField(null=True)

    def __str__(self):
        return str(self.Class)

    class Meta:
        verbose_name_plural = "classes"
        ordering = ['Class']
        unique_together = [['Class']]

class subjects(models.Model):
    subject = models.TextField(blank=False)
    image_url=models.URLField(null=True)

    def __str__(self):
        return str(self.subject)
    class Meta:
        verbose_name_plural = "subjects"
        ordering = ['subject']
        unique_together = [['subject']]


class chapters(models.Model):
    chapter_number=models.IntegerField(default=1)
    chapter_name = models.CharField(blank=False,max_length=200)
    description = models.TextField(null=True,default=None,blank=True)
    Class= models.ForeignKey(classes, on_delete=models.CASCADE)
    subject = models.ForeignKey(subjects, on_delete=models.CASCADE)
    s3object_value = models.TextField()
    image_url=models.URLField(null=True,default=None)
    updated_at =models.DateTimeField(default=datetime.utcnow)
    

    def __str__(self):
        return str(self.s3object_value)
    
    class Meta:
        verbose_name_plural = "chapters"
        unique_together = [['chapter_number', 'Class','subject']]
        ordering = ['chapter_number']


