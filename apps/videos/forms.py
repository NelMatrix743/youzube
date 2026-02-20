from django import forms


class VideoUploadForm(forms.Form):
    
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class" : "form-input",
                "placeholder" : "enter video title"
            }
        )
    )
    description = forms.CharField(
        required=False, 
        widget=forms.Textarea(
            attrs={
                "class" : "form-input",
                "placeholder" : "enter video description",
                "rows" : 4
            }
        )
    )
    video_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class" : "form-input",
                "accept" : "video/*"
            }
        )
    )

    def clean_video_file(self):
        uploaded_video: any | None = self.cleaned_data.get("video_file")
        allowed_video_types: list[str] = [
            "video/mp4",
            "video/quicktime",
            "video/webm",
            "video/x-msvideo"
        ]

        if not uploaded_video:
            return uploaded_video # None
        
        if uploaded_video.size > 500 * 1024 * 1024:
            raise forms.ValidationError("video size must be less than 500MB")
        
        if uploaded_video.content_type not in allowed_video_types:
            raise forms.ValidationError("video format not supported")
        
        return uploaded_video # video content
