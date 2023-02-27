# backend-final-assignment
Template repository for final assignment of basic backend.

memo
テスト作りたい。
UserProfileView
    viewのcontextに含まれるフォローフォロワーの数がDBと一致すればいい
FollowView
test_success_post
    リクエストを送信セット。DBにデータが格納されたことを確認する
test_failure_post_with_not_exist_user
    存在しないユーザーにリクエストを送信して、DBにデータが追加されないことを確認
test_failure_post_with_self
    自分自身にたいしてリクエストを送信して、DBにデータが追加されないことを確認
UnfollowView
test_succcess_post
    リクエストを送信。DBのデータが削除される。


    resolve_url
class TestUnlikeView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="@0dg8gwO7_0Gw",
        )
        self.tweet = Tweet.objects.create(
            user=self.user,
            content="Hello, world!",
        )
        self.client.force_login(self.user)
        self.tweet.liked_by.add(self.user)

    def test_success_post(self):
        print(reverse("tweets:unlike", kwargs={"pk": self.tweet.pk}))
        response = self.client.post(
            reverse(
                "tweets:unlike",
                kwargs={"pk": self.tweet.pk},
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tweet.liked_by.count(), 0)
