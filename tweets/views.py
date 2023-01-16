from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, View

from tweets.forms import TweetCreateForm
from tweets.models import Like, Tweet

# Create your views here.


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tweets = Tweet.objects.select_related("user").all()
        liked_tweets = [
            like_record.tweet for like_record in Like.objects.filter(user=request.user)
        ]
        context = {
            "tweet": tweets,
            "liked_tweets": liked_tweets,
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
        like_count = Like.objects.filter(tweet=tweet).count()
        context = {
            "tweet": tweet,
            "like_count": like_count,
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
        return redirect("welcome:home")


class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(
            Tweet,
            pk=kwargs.get("pk"),
        )
        if Like.objects.filter(user=request.user, tweet=tweet).exists():
            return HttpResponse("UNIQUE constraint failed", status=200)
        Like.objects.create(user=request.user, tweet=tweet)
        params = {"tweet": tweet.id}
        return JsonResponse(params, status=200)


class UnlikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(
            Tweet,
            pk=kwargs.get("pk"),
        )
        if not (like_record := Like.objects.filter(user=request.user, tweet=tweet)):
            return HttpResponse("Like Record Unexist", status=200)
        like_record.delete()
        params = {"data": tweet.id}
        return JsonResponse(params, status=200)
