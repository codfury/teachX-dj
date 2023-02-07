from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

from .models import *

class classesSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('__all__')
        model = classes
        ordering = ['Class']
        

class subjectsSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('__all__')
        model = subjects
        ordering = ['subject']

class chaptersSerializer(serializers.ModelSerializer):
    Class=serializers.CharField(source='Class.Class')
    subject=serializers.CharField(source='subject.subject')
    def create(self, validated_data):
        Class,created = classes.objects.get_or_create(Class=validated_data.get('Class').get('Class'))
        subject,created = subjects.objects.get_or_create(subject=validated_data.get('subject').get('subject'))

        chapter = chapters.objects.get_or_create(
            
                chapter_number = validated_data.get('chapter_number'),
                chapter_name = validated_data.get('chapter_name'),
                description = validated_data.get('description'),
                Class=Class,
                subject=subject,
                s3object_value =validated_data.get('s3object_value'),
                image_url=validated_data.get('image_url')
        )
        chapter.save()
        return chapter
    class Meta:
        fields = ('chapter_number','chapter_name','description','Class','subject','image_url','s3object_value')
        ordering = ['chapter_number']
        model = chapters
    

class deviceSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('device_id,name,address','is_enable','updated_at')
        model = devices
        read_only_fields = ['updated_at']
        

