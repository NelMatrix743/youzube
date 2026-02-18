from django.shortcuts import redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import SystemUserCreationForm


# Create your views here.
class SystemRegistrationView(CreateView):
    
    form_class = SystemUserCreationForm
    success_url = reverse_lazy("account:login")
    template_name = "accounts/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return redirect('/')
    