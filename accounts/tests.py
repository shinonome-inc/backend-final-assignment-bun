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

        user = {
            "email": "test@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        response = self.client.post(self.url, user)
        self.assertTrue(
            User.objects.filter(username="test", email="test@example.com").exists()
        )
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

        form = response.context["form"]
        print("failure_post_with_empty_form:", form.errors, "\n")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["username"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["password1"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["password2"], ["このフィールドは必須です。"])

    def test_failure_post_with_empty_username(self):
        invalid_data = {
            "email": "test@example.com",
            "username": "",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        response = self.client.post(self.url, invalid_data)

        form = response.context["form"]
        print("test_failure_post_with_empty_username:", form.errors, "\n")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username=invalid_data["username"]).exists()
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["username"], ["このフィールドは必須です。"])

    def test_failure_post_with_empty_email(self):
        invalid_data = {
            "email": "",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        response = self.client.post(self.url, invalid_data)

        form = response.context["form"]
        print("test_failure_post_with_empty_email:", form.errors, "\n")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email=invalid_data["email"]).exists())
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["このフィールドは必須です。"])

    def test_failure_pmst_with_empty_password(self):
        invalid_data = {
            "email": "test@example.com",
            "username": "test",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, invalid_data)

        form = response.context["form"]
        print("test_failure_post_with_empty_password:", form.errors, "\n")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(password=invalid_data["password1"]).exists()
        )
        self.assertFalse(
            User.objects.filter(password=invalid_data["password2"]).exists()
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password1"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["password2"], ["このフィールドは必須です。"])

    def test_failure_post_with_duplicated_user(self):
        user1 = {
            "email": "test1@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        user2 = {
            "email": "test2@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        self.client.post(reverse("accounts:signup"), user1)
        response = self.client.post(reverse("accounts:signup"), user2)

        form = response.context["form"]
        print("test_failure_post_with_empty_password:", form.errors, "\n")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="test", email="test2@example.com").exists()
        )
        self.assertFormError(response, "form", "username", "同じユーザー名が既に登録済みです。")

    def test_failure_post_with_invalid_email(self):
        user = {
            "email": "test.boo",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        response = self.client.post(reverse("accounts:signup"), user)

        form = response.context["form"]
        print("test_failure_post_with_empty_password:", form.errors, "\n")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="test", email="test.boo").exists()
        )
        self.assertFormError(response, "form", "email", "有効なメールアドレスを入力してください。")

    def test_failure_post_with_too_short_password(self):
        user = {
            "email": "test@example.com",
            "username": "test",
            "password1": "pase",
            "password2": "pase",
        }
        response = self.client.post(reverse("accounts:signup"), user)

        form = response.context["form"]
        print("test_failure_post_with_empty_password:", form.errors, "\n")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="test", email="test@example.com").exists()
        )
        self.assertFormError(
            response, "form", "password2", "このパスワードは短すぎます。最低 8 文字以上必要です。"
        )

    def test_failure_post_with_password_similar_to_username(self):
        user = {
            "email": "test@example.com",
            "username": "goodpass",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        response = self.client.post(reverse("accounts:signup"), user)

        form = response.context["form"]
        print("test_failure_post_with_empty_password:", form.errors, "\n")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="test", email="test@example.com").exists()
        )
        self.assertFormError(response, "form", "password2", "このパスワードは ユーザー名 と似すぎています。")

    def test_failure_post_with_only_numbers_password(self):
        user = {
            "email": "test@example.com",
            "username": "test",
            "password1": "20011111",
            "password2": "20011111",
        }
        response = self.client.post(reverse("accounts:signup"), user)

        form = response.context["form"]
        print("test_failure_post_with_empty_password:", form.errors, "\n")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="test", email="test@example.com").exists()
        )
        self.assertFormError(response, "form", "password2", "このパスワードは数字しか使われていません。")

    def test_failure_post_with_mismatch_password(self):
        user = {
            "email": "test@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpath",
        }
        response = self.client.post(reverse("accounts:signup"), user)

        form = response.context["form"]
        print("test_failure_post_with_empty_password:", form.errors, "\n")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="test", email="test@example.com").exists()
        )
        self.assertFormError(response, "form", "password2", "確認用パスワードが一致しません。")


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
