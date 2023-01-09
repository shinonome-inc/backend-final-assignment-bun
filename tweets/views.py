from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from tweets.models import Tweet
# Create your views here.


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tweets = Tweet.objects.select_related("user").all()
        context = {"tweet": tweets}
        return render(request, "tweets/home.html", context)
