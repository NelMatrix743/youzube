from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Video
from .forms import VideoUploadForm
from .imagekit_client import (
    upload_video, 
    upload_thumbnail
)


# Create your views here.
@login_required
@require_POST
def video_upload_view(request):
    form = VideoUploadForm(request.POST, request.FILES)

    if not form.is_valid():
        errors = []
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(
                    f"{field} : {error}" if field != "__all__" else error
                )
        return JsonResponse({
            "success" : False,
            "errors" : ';'.join(errors)
        })

    video_file = form.cleaned_data["video_file"]
    thumbnail_data: str = request.POST.get("thumbnail_data", '')
    thumbnail_url: str = ''

    try:
        video_result = upload_video(
            file_data=video_file.read(),
            file_name=video_file.name
        )

        if thumbnail_data and thumbnail_data.startswith("data:image"):
            base_name = video_file.name.resplit('.', 1)[0]
            try:
                thumbnail_result = upload_thumbnail(
                    file_data=thumbnail_data,
                    file_name=base_name + "_thumb.jpg"
                )
                thumbnail_url = thumbnail_result["url"]
            except Exception as e:
                pass
         
        video_entry = Video.objects.create(
            User=request.user,
            title=form.cleaned_data["title"],
            description=form.cleaned_data["description"],
            file_id=video_result["file_id"],
            video_url=video_result["url"],
            thumbnail_url=thumbnail_url
        )

        return JsonResponse({
            "success" : True,
            "video_id" : video_entry.id,
            "message" : "Video Successfully Uploaded!"
        })
            
    except Exception as error:
        return JsonResponse({
            "success" : False,
            "error" : str(error)
        })
    

@login_required
def video_submission_view(request):
    return render(
        request,
        "videos/upload.html",
        {
            "form" : VideoUploadForm()
        }
    )

