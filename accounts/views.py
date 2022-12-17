from django.shortcuts import render

from django.contrib.auth import get_user_model, login, authenticate  # なぜか順番変えたらエラーになった
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy

from .forms import SignUpForm

# Create your views here.

User = get_user_model()


class SignUpView(CreateView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("accounts:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return response
        else:
            return render("accounts:welcome")


class HomeView(TemplateView):
    template_name = "accounts/home.html"


class WelcomeView(TemplateView):
    template_name = "welcome/index.html"
