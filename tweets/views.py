from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, ListView
from django.db.models import Count, Exists, OuterRef

from tweets.forms import TweetCreateForm
from tweets.models import Tweet


class HomeView(LoginRequiredMixin, ListView):
    template_name = "tweets/home.html"
    model = Tweet

    def get_queryset(self, **kwargs):
        return (
            Tweet.objects.select_related("user")
            .prefetch_related("liked_by")
            .order_by("-created_at")
            .annotate(
                like_counts=Count("liked_by"),
                is_liked=Exists(
                    Tweet.objects.filter(
                        pk=OuterRef("pk"),
                        liked_by=self.request.user,
                    ),
                ),
            )
        )

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


class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=self.kwargs["pk"])
        tweet.liked_by.add(request.user)
        previous_url = request.META.get('HTTP_REFERER')
        return redirect(previous_url)


class UnlikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=self.kwargs["pk"])
        tweet.liked_by.remove(request.user)
        previous_url = request.META.get('HTTP_REFERER')
        return redirect(previous_url)
