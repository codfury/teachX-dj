from django.contrib import admin
from .models import classes,subjects,chapters,devices
admin.site.site_header = "TeachX Admin"
admin.site.index_title = "Welcome to TeachX Admin page"
admin.site.site_title = "TeachX Admin"

admin.site.register(classes)
admin.site.register(subjects)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id','name','is_enable')
    search_fields = ['device_id','name']
admin.site.register(devices, DeviceAdmin)

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chapter_name','Class','subject','chapter_number','s3object_value')
    search_fields = ['Class__Class','subject__subject','chapter_name','s3object_value']
admin.site.register(chapters, ChapterAdmin)

# Register your models here.
