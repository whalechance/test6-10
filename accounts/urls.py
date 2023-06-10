from django.urls import path
# viewsモジュールをインポート
from . import views

# viewsをインポートしてauth_viewという名前で利用する
from django.contrib.auth import views as auth_views

# urlパターンが逆引きできるように名前をつける

app_name = 'accounts'

# urlパターンを登録するための変数
urlpatterns = [
    # サインアップページのビューの呼び出し
    # 「http(s)://<ホスト名>/signup/」へのアクセスに対して
    # viewsモジュールのSignUpViewをインスタンス化する
    path('signup/',
         views.SignUpView.as_view(),
         name='signup'),

    # サインアップ完了ページのビューの呼び出し
    # 「http(s)://<ホスト名>/signup/」へのアクセスに対して
    # viewsモジュールのSignUpViewをインスタンス化する
    path('signup_success/',
         views.SignUpSuccessView.as_view(),
         name='signup_success'),

    # ログインページの表示
    # https://<ホスト名>/signup/へのアクセスに対して
    # django.contrib.auth.views.LoginViewをインスタンス化して
    # ログインページを表示する
    path('login/',
         # ログイン用のテンプレートフォームをレンダリング
         auth_views.LoginView.as_view(template_name='login.html'),
         name='login'),

    # ログアウトを実行
    # https://<ホスト名>/logout/へのアクセスに対して
    # django.contrib.auth.views.LogoutViewをインスタンス化して
    # ログアウトさせる
    path('logout/',
         auth_views.LogoutView.as_view(template_name='logout.html'),
         name='logout'),


    path('bio_update/',
         views.bio_update, name='bio_update')
            ]
