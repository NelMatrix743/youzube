from django.urls import path
from .views import (
    video_upload_view,
    video_submission_view, 
    video_list_view,
    video_detail_view,
    channel_view
)


app_name = "apps.videos"

urlpatterns = [
    path('', video_list_view, name="list"),
    path("upload/", video_submission_view, name="upload"),
    path("upload/submit/", video_upload_view, name="upload_submit"),
    path("videos/<int:video_id>", video_detail_view, name="detail"),
    path("channel/<str:username>/", channel_view, name="channel")
]