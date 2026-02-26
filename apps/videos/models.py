from datetime import date, datetime
from typing import Literal

from django.db import models
from django.contrib.auth.models import User
from .imagekit_client import (
    get_optimized_video_url,
    get_streaming_url,
    get_thumbnail_url,
    add_image_watermark
)


# Create your models here.

class Video(models.Model):
    
    user: models.ForeignKey = models.ForeignKey(
          User,
          on_delete=models.CASCADE,
          related_name="videos"
    )
     
    title: models.CharField = models.CharField(
        max_length=200
    )
    description: models.TextField = models.TextField(
        blank=True
    )

    file_id: models.CharField = models.CharField(
        max_length=200
    )
    video_url: models.URLField = models.URLField(
        max_length=500
    )
    thumbnail_url: models.URLField = models.URLField(
        max_length=500,
        blank=True
    )

    num_of_views: models.PositiveBigIntegerField = models.PositiveBigIntegerField(
        default=0
    )
    num_of_likes: models.PositiveBigIntegerField = models.PositiveBigIntegerField(
        default=0
    )

    num_of_dislikes: models.PositiveBigIntegerField = models.PositiveBigIntegerField(
        default=0
    )

    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering: list[str] = ["-created_at"]

    
    def __str__(self) -> str:
        return self.title
    

    @property
    def display_thumbnail_url(self) -> str:
        if self.thumbnail_url and ("/thumbnails/" in self.thumbnail_url):
            return add_image_watermark(self.thumbnail_url, self.user.username)
        return self.generated_thumbnail_url
    

    @property
    def generated_thumbnail_url(self) -> str:
        if not self.video_url:
            return ""
        return get_thumbnail_url(self.video_url)
    

    @property
    def streaming_url(self) -> str:
        if not self.video_url:
            return ""
        return get_streaming_url(self.video_url)
    

    @property
    def optmized_video_url(self) -> str:
        if not self.video_url:
            return ""
        return get_optimized_video_url(self.video_url)
    


class VideoLike(models.Model):

    LIKE: int = 1
    DISLIKE: int = -1
    LIKE_CHOICES: list[tuple[int, str]] = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike")
    ]

    user: models.ForeignKey= models.ForeignKey(User, on_delete=models.CASCADE)
    video: models.ForeignKey = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name="user_likes"
    )
    value: models.SmallIntegerField = models.SmallIntegerField(choices=LIKE_CHOICES)
    created_at: models.DateField = models.DateField(auto_now_add=True)


    class Meta:
        
        unique_together: list[str] = ["user", "video"]

    
    def __str__(self) -> str:
        action: Literal['liked'] | Literal['disliked'] = (
            "liked" if self.value == self.LIKE else "disliked"
        )
        return f"{self.user.username} {action} {self.video.title}"
