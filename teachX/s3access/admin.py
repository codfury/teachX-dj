from django.contrib import admin
from .models import classes,subjects,chapters,devices

admin.site.register(classes)
admin.site.register(subjects)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id','name')
admin.site.register(devices, DeviceAdmin)

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('Class','subject','chapter_number','chapter_name','s3object_value')
    search_fields = ['Class__Class','subject__subject','chapter_name','s3object_value']
admin.site.register(chapters, ChapterAdmin)

# Register your models here.
