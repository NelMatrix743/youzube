from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class SystemUserCreationForm(UserCreationForm):
    phone_number: forms.CharField = forms.CharField(max_length=20)

    class Meta:
        model: User = User
        fields: tuple[str] = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)

        # phone number
        user.profile.phone_number = self.cleaned_data["phone_number"]
        
        if commit:
            user.save()
        return user
