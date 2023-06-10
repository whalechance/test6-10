from django.urls import path
from . import views

# urlパターンが逆引きできるように名前をつける

app_name = 'photo'
urlpatterns = [
    # photoアプリへのアクセスはviewモジュールのIndexViewを実行
    path('', views.IndexView.as_view(), name='index'),
    # 写真投稿ページヘのアクセスはviewsモジュールのCreatePhotoViewを実行
    path('post/', views.CreatePhotoView.as_view(), name='post'),
    # 投稿完了ページヘのアクセスはviewsモジュールのPostSuccessViewを実行
    path('post_done/', views.PostSuccessView.as_view(), name='post_done'),
    # カテゴリー一覧ページ
    # photos/<Categorysテーブルのid値>にマッチング
    # <int:Category>は辞書{Category:id(int)}としてCategoryViewに渡される
    path('photos/<int:category>', views.CategoryView.as_view(), name='photos_cat'),
    # ユーザーの投稿一覧ページ
    # photos/<ユーザーテーブルのid値>にマッチング
    # <int:user>は辞書{user:id(int)}としてCategoryViewに渡される
    path('user-list/<int:user>', views.UserView.as_view(), name='user_list'),
    # 詳細ページ
    # photo-detail/<Photo postsのid値>にマッチング
    # <int:pk>は辞書{pk:id(int)}としてDetailViewに渡される
    path('photo-detail/<int:pk>', views.DetailView.as_view(), name='photo_detail'),
    # マイページ
    # my pageへのアクセスはMypageViewを実行
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    # 投稿写真の削除
    # photo/<Photo postsテーブルのid値>/delete/②マッチング
    # <int:pk>は辞書{pk:id値(int)}としてDetailViewに渡される
    path('photo/<int:pk>/delete', views.PhotoDeleteView.as_view(), name='photo_delete'),

    path('board/<int:pk>', views.BoardView.as_view(), name='board'),
]
