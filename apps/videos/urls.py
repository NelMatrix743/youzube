from django.urls import path
from .views import (
    video_upload_view,
    video_submission_view
)


app_name = "apps.videos"

urlpatterns = [
    path("upload/", video_submission_view, name="upload"),
    path("upload/submit/", video_upload_view, name="upload_submit")
]