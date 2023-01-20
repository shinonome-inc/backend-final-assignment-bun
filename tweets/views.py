from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, View

from tweets.forms import TweetCreateForm
from tweets.models import Tweet

# Create your views here.


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tweets = Tweet.objects.select_related("user").all()
        context = {
            "tweet": tweets,
        }
        return render(request, "tweets/home.html", context)


class TweetCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TweetCreateForm()
        return render(request, "tweets/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TweetCreateForm(data=request.POST)
        if form.is_valid():
            content = form.cleaned_data.get("content")
            Tweet.objects.create(user=request.user, content=content)
            return redirect("tweets:home")
        return render(request, "tweets/create.html", {"form": form})


class TweetDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tweet = get_object_or_404(
            Tweet,
            pk=kwargs.get("pk"),
        )
        is_tweet_user = tweet.user == request.user
        context = {
            "tweet": tweet,
            "is_tweet_user": is_tweet_user,
        }
        return render(
            request,
            "tweets/detail.html",
            context,
        )


class TweetDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(
            Tweet,
            pk=kwargs.get("pk"),
        )
        if tweet.user != request.user:
            return HttpResponseForbidden()
        tweet.delete()
        return redirect("tweets:home")
