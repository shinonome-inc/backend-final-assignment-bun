import os
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View

from .forms import LoginForm, SignUpForm

User = get_user_model()


class SignUpView(CreateView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("tweets:home")

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


class LoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = "welcome/index.html"


class UserProfileView(TemplateView):
    def get_username(self, **kwargs):
        username = super().get_username(**kwargs)
        return username

    template_name = "accounts/profile.html"
