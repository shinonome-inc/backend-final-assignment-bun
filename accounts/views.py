from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from tweets.models import Tweet

from .forms import SignUpForm

User = get_user_model()


class SignUpView(CreateView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return response
        else:
            return redirect("welcome:top")


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    pass


class UserProfileView(LoginRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):
        requested_user = get_object_or_404(User, username=kwargs.get("username"))
        requested_username = requested_user.get_username()
        user_tweets = Tweet.objects.filter(user=requested_user)
        context = {
            "user_tweets": user_tweets,
            "requested_username": requested_username,
        }
        return render(request, "accounts/profile.html", context)
