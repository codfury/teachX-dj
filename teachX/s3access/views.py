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

def generate_presigned_url(bucket_name='teachx-bucket', object_key="Acid Base and Salt (Published)/index.html", expiry=3600):
    

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


# class ListClassesAPIView(generics.ListAPIView):
#     queryset = classes.objects.all()
#     serializer_class = classesSeralizer

#     def get_queryset(self):
#         return self.queryset
    
# class ListSubjectsAPIView(generics.ListAPIView):
#     queryset = subjects.objects.all()
#     serializer_class = subjectsSeralizer

#     def get_queryset(self):
#         return self.queryset.filter(class=class)
    
# class ListChaptersAPIView(generics.ListAPIView):
#     queryset = chapters.objects.all()
#     serializer_class = chaptersSeralizer

#     def get_queryset(self):
#         return self.queryset.filter(class=class,subject=subject)
    
# class ListCAPIView(generics.ListAPIView):
#     queryset = classes.objects.all()
#     serializer_class = classesSeralizer

#     def get_queryset(self):
#         return self.queryset


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

# class AddChapter(generics.CreateAPIView):
#     queryset = chapters.objects.all()
#     serializer_class = chaptersSerializer

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
    print(generate_presigned_url())
    
    resp={"course_url":"https://s3.ap-south-1.amazonaws.com/neweducationplatform.com/synthetic+fibres+and+plastic/index.html"}
    return Response(resp)

    #return generate_presigned_url()

    # resp={"url":"https://s3.ap-south-1.amazonaws.com/neweducationplatform.com/synthetic+fibres+and+plastic/index.html"}
    # return Response(resp)

    device_id,s3object_val = request.data.get('device_id') , request.data.get('s3object_value')
    print(device_id,s3object_val,"lolo")
    device = get_object_or_404(devices,device_id=device_id)
    #resp={"url":"acid_bases_salt_tx/Acid Base and Salt (Published)/index.html"}
    print(device_id,s3object_val)
    if(device.is_enable and s3object_val):
        return generate_presigned_url(object_key=s3object_val)
    print("404")
    return Response({"error":404})
    



# Create your views here.
