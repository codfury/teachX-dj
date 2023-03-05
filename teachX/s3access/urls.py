from django.urls import path
from .views import *

urlpatterns = [
    path('get_classes/',get_classes, name='get_classes'),
    path('get_subjects/',get_subjects, name='get_subjects'),
    path('get_chapters/',get_chapters, name='get_chapters'),
    path('edit_chapters/', ChapterListEdit.as_view(), name='get_chapters'),
    path('edit_chapter/<int:pk>/', ChapterDetailEdit.as_view(), name='get_chapter'),
    path('add_chapter/', AddChapter, name='add_chapter'),
    path('get_s3access/',get_s3access, name='get_s3access'),
    # path('add_device/', verify_otp, name='add'),
    # path('edit_device/', verify_otp, name='verify_otp'),
    # path('edit_course/', verify_otp, name='verify_otp'),
    
]