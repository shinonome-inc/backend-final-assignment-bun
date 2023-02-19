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

