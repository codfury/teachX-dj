from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import base64
from rest_framework import status
from django.conf import settings
from rest_framework import response, decorators, permissions, status
import urllib.request
import urllib.parse
import json
from .models import classes,subjects,chapters,devices
#import pytz
from django.conf import settings
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import generics
# from rest_framework_api_key.permissions import HasAPIKey
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
import requests
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth.models import User

@decorators.api_view(["GET","POST"])
def login(request):

    username,password,device_id = request.data.get('username'),request.data.get('password'),request.data.get('device_id')
    device = get_object_or_404(devices,device_id=device_id,username=username)
    if(username and password and device):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@decorators.api_view(["GET","POST"])
def forgot_password(request):

    username,password,confirm_password,device_id = request.data.get('username'),request.data.get('password'),request.data.get('confirm_password'),request.data.get('device_id')
    user = get_object_or_404(User, username=username)
    device = get_object_or_404(devices,device_id=device_id,username=username)
    if(device and user and password==confirm_password):
        user.set_password(password)
        user.save()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

def generate_presigned_url(object_key,bucket_name='teachx-bucket',expiry=3600):
    
    client = boto3.client("s3",region_name='ap-south-1',
                          aws_access_key_id='AKIA3AOM6DCCQSHKING7',
                          aws_secret_access_key="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")
    try:
        response = client.generate_presigned_url('get_object',
                                                  Params={'Bucket': bucket_name,'Key': object_key},
                                                  HttpMethod="GET",ExpiresIn=expiry)
        print(response)
        return Response({"course_url":response})
    except ClientError as e:
        return {"Error":1}



@decorators.api_view(["GET","POST"])
def get_classes(request):
    classes_avl = classes.objects.all()
    serializer = classesSerializer(classes_avl, many=True)    
    return Response(serializer.data)

@decorators.api_view(["GET","POST"])
def get_subjects(request):
    class_data=int(request.data.get('class'))
    class_object = get_object_or_404(classes,Class=class_data)
    subjects_avl = chapters.objects.filter(Class=class_object)
    serializer = chaptersSerializer(subjects_avl, many=True)
    subjects_list={}
    for chapter in serializer.data:
        subject_name=chapter.get('subject')
        if(subject_name in subjects_list ):
            subjects_list[subject_name]['count']+=1
        else:
            subjects_list[subject_name]={'count':1}
    response_list=[]
    for key,value in subjects_list.items():
        response_list.append({
            "subject":key,
            "chapters_count":value['count'],
            "image_url":subjects.objects.get(subject=key).image_url      
             })
    return Response(response_list)

@decorators.api_view(["GET","POST"])
def get_chapters(request):
    class_data = request.data.get('class')
    class_data = get_object_or_404(classes,Class=class_data)
    chapters_avl = chapters.objects.filter(Class = class_data)
    serializer = chaptersSerializer(chapters_avl, many=True)
    resp={}
    for data in serializer.data:
        if(data['subject'] in resp):
            resp[data['subject']].append(data)
        else:
            resp[data['subject']]=[data]

    
    return Response(resp)


@api_view(['GET', 'POST'])
def AddChapter(request ):


    class_data,subject,chapter_number = request.data.get('class'),request.data.get('subject'),request.data.get('chapter_number')
    try:
        chapter_avl=chapters.objects.get(Class=class_data,subject=subject,chapter_number=chapter_number)
        serializer = chaptersSerializer(chapters_avl)
        return Response(serializer.data)
    except:
        serializer = chaptersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
Edit if 3 matches in ADD,
Secure ADD
"""
    # if request.method == 'GET' or :
    #     class_data,subject = request.data.get('class'),request.data.get('subject')
    #     class_data,subject = get_object_or_404(classes,Class=class_data), get_object_or_404(subjects,subject=subject)
    #     chapters_avl = chapters.objects.filter(Class = class_data,subject = subject)
    #     serializer = chaptersSerializer(chapters_avl, many=True)
    #     return Response(serializer.data)

    # elif request.method == 'POST':
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChapterListEdit(generics.ListCreateAPIView):
    queryset = chapters.objects.all()
    serializer_class = chaptersSerializer

class ChapterDetailEdit(generics.RetrieveUpdateDestroyAPIView):
    queryset = chapters.objects.all()
    serializer_class = chaptersSerializer


@decorators.api_view(['GET','POST'])    
def get_s3access(request):

    device_id,s3object_val = request.data.get('device_id') , request.data.get('s3object_value')
    device = get_object_or_404(devices,device_id=device_id)
    #resp={"url":"acid_bases_salt_tx/Acid Base and Salt (Published)/index.html"}
    print(device_id,s3object_val)
    if(device.is_enable and s3object_val):
        return generate_presigned_url(object_key=s3object_val)
    print("404")
    return Response({"error":404})
    



# Create your views here.
