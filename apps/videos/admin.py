from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Video


# Register your models here.
@admin.register(Video)
class VideoAdmin(ModelAdmin):
    pass