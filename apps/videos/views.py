from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from .models import Video, VideoLike
from .forms import VideoUploadForm
from .imagekit_client import (
    upload_video, 
    upload_thumbnail,
    delete_video_from_imagekit
)


# Create your views here.
@login_required
@require_POST
def video_upload_view(request) -> JsonResponse:
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
            user=request.user,
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
def video_submission_view(request) -> HttpResponse:
    return render(
        request,
        "videos/upload.html",
        {
            "form" : VideoUploadForm()
        }
    )


@login_required
@require_POST
def video_delete_view(request, video_id) -> JsonResponse:
    video = get_object_or_404(Video, id=video_id, user=request.user)

    try:
        delete_video_from_imagekit(video.file_id)
    except Exception as e:
        print(e)
        pass

    video.delete()

    return JsonResponse({
        "success" : True,
        "message" : "video deleted successfullly"
    })


def video_list_view(request) -> HttpResponse:
    videos: any = Video.objects.all()
    context: dict[str, any] = {
        "videos" : videos
    }
    return render(request, "videos/list.html", context)


def video_detail_view(request, video_id) -> HttpResponse:
    video: Video = get_object_or_404(Video.objects, id=video_id)

    video.num_of_views += 1
    video.save(update_fields=["views"])

    context: dict[str, Video] = {
        "video" : video
    }
    return render(request, "videos/detail.html", context)


@login_required
@require_POST
def video_vote_view(request, video_id):
    video: Video = get_object_or_404(Video, id=video_id)
    vote_type: str = request.POST.get("vote")

    user_vote: int = 0

    if vote_type not in ["like", "dislike"]:
        return JsonResponse({
            "success" : False,
            "error" : "invalid vote",
        }, status=400)

    value = (
        VideoLike.LIKE if vote_type == "like" else VideoLike.DISLIKE
    )

    existing_vote = (
        VideoLike.objects.filter(user=request.user, video=video).first()
    )

    if existing_vote:
        if existing_vote.value == value:
            if value == VideoLike.LIKE:
                video.likes -= 1
            else:
                video.dislikes -= 1
            existing_vote.delete()
            user_vote = None
        else:
            if value == VideoLike.LIKE:
                video.likes += 1
                video.dislikes -= 1
            else:
                video.likes -= 1
                video.dislikes += 1
            existing_vote.value = value
            existing_vote.save()
            user_vote = value
    else:
        VideoLike.objects.create(user=request.user, video=video, value=value)
        if value == VideoLike.LIKE:
            video.likes += 1
        else:
            video.dislikes += 1
        user_vote = value

    video.save(update_fields=["likes", "dislikes"])

    return JsonResponse({
        "likes" : video.likes, 
        "dislikes" : video.dislikes,
        "user_vote" : user_vote
    })


def channel_view(request, username) -> HttpResponse:
    videos = Video.objects.filter(user__username=username)
    return render(request, "videos/channel.html", {
        "videos" : videos,
        "channel_name" : username
    })
