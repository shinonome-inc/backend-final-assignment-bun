from django.test import TestCase

from django.contrib.auth import get_user_model, SESSION_KEY
from django.urls import reverse


User = get_user_model()


class TestSignUpView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        """
        クラスの中で定義される関数はメソッド
        サーバーから情報を取得できるかtest

        ほんとはClientのimportが必要っぽい。今回はtest.pyの中なので大丈夫
        status_codeは404みたいなやつ。200はリクエスト成功
        reverseでURL取得、client.getを実行。client,getはTestCaseで定義されてる
        assert*はunittest等も多い
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        # サーバーへ情報が登録できるかtest

        # 辞書データをclient.postに投げるとそれらのフィールドに値を入れてくれて便利

        user = {
            "email": "test@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        response = self.client.post(self.url, user)
        self.assertTrue(
            # filterはモデルとobjectにくっつける
            User.objects.filter(username="test", email="test@example.com").exists()
        )
        # SimpleTestCase.assertRedirects(response, expected_url, status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        self.assertRedirects(
            response,
            reverse("accounts:home"),
            status_code=302,  # はじめに返ってくるHTTPレスポンスコード
            target_status_code=200,  # 最終的に返ってくるHTTPのレスポンスコード
            msg_prefix="",  # テスト結果のメッセージのプレフィックス
            fetch_redirect_response=True,  # 最終ページをロードするか否か
        )

        self.assertIn(
            SESSION_KEY, self.client.session
            )  # sessionを使うならsetting.pyを書き換え,AinBの確認。

    # 以降ちゃんとエラーでてくれるかtest
    def test_failure_post_with_empty_form(self):
        invalid_data = {
            "email": "",
            "username": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context['form']
        print(form.errors)


    def test_failure_post_with_empty_username(self):
        pass

    def test_failure_post_with_empty_email(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass

    def test_failure_post_with_duplicated_user(self):
        pass

    def test_failure_post_with_invalid_email(self):
        pass

    def test_failure_post_with_too_short_password(self):
        pass

    def test_failure_post_with_password_similar_to_username(self):
        pass

    def test_failure_post_with_only_numbers_password(self):
        pass

    def test_failure_post_with_mismatch_password(self):
        pass


class TestHomeView(TestCase):
    def test_success_get(self):
        pass


class TestLoginView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass


class TestLogoutView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileEditView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
