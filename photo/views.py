from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView

# django.views.genericからCreateViewをインポート
from django.views.generic import CreateView
# django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy
# formsモジュールからPhotoPostFormをインポート
from .forms import PhotoPostForm
# method_decoratorをインポート
from django.utils.decorators import method_decorator
# login_requiredをインポート
from django.contrib.auth.decorators import login_required
# modelsモジュールからモデルPhotoPostをインポート
from .models import PhotoPost, Like, Comment
# django.views.genericからDetailViewをインポート
from django.views.generic import DetailView
# django.views.genericからDeleteViewをインポート
from django.views.generic import DeleteView
from .forms import CommentForm


class IndexView(ListView):
    template_name = 'index.html'
    # 投稿日時の降順で並び替える
    queryset = PhotoPost.objects.order_by('-posted_at')
    # 1ページ内に表示するレコードの件数
    paginate_by = 9


# デコレーターによりCreatePhotoViewへのアクセスはログインユーザーにのみ限定
# 非ログイン状態はsettings.py→LOGIN_URLにリダイレクト
@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    """
    写真投稿ページのビュー
    PhotoPostFormで定義されているモデルとフィールドを連携
    投稿データをデータベースに登録

    Attributes :
         form_class : モデルとフィールドが登録されたフォームクラス
         template_name : レンダリングするテンプレート
         success_url : データベースへの登録完了後のリダイレクト先
    """
    # forms.pyのPhotoPostFormをクラスとして登録
    form_class = PhotoPostForm
    # レンダリングするテンプレート
    template_name = "post_photo.html"
    # フォームデータ登録完了後のリダイレクト先
    success_url = reverse_lazy('photo:post_done')

    def form_valid(self, form):
        """
        CreateViewクラスのform_valid()をオーバーライド

        フォームのバリデーションを通過したときに呼ばれる
        フォームクラスの登録
        :param form:
            form(django.forms.Form):
                form_classに格納されているPhotoPostFormオブジェクト
        :return:
            HttpResponseRedirectオブジェクト:
                スーパークラスのform_valid()の戻り地を返すことで
                success_urlで設定されているURLにリダイレクトさせる
        """
        # commit = FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        # 戻り値はスーパークラスのform_valid()の戻値(HttpResponseRedirect)
        return super().form_valid(form)


class PostSuccessView(TemplateView):
    """
    投稿完了ページのview
    Attributes:
          template_name : レンダリングするテンプレート
    """
    # index.htmlをレンダリングする
    template_name = 'post_success.html'


class CategoryView(ListView):
    """
    カテゴリページのView
    Attributes:
          template_name:レンダリングするテンプレート
          paginate_by:1ページに表示するっレコードの設定
    """
    # index.htmlをレンダリングする
    template_name = 'index.html'

    paginate_by = 9

    def get_queryset(self):
        """
        クエリを実行する
        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライドによりクエリを実行する
        :return: クエリによって取得されたレコード
        """
        # self.kwargsでキーワードの辞書を取得し
        # categoryキーの値(Categoryテーブルのid)を取得
        category_id = self.kwargs['category']
        # filter(フィールド名=id)で絞り込む
        categories = PhotoPost.objects.filter(category=category_id).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return categories


class UserView(ListView):
    """
    ユーザーの投稿一覧ページ
    Attributes:
          template_name:レンダリングするテンプレート
          paginate_by:1ページに表示されるレコードの件数
    """
    # index.htmlをレンダリング
    template_name = "index.html"
    paginate_by = 9

    def get_queryset(self):
        """
        クエリの実行
        上記 categoryviewと同様
        :return:クエリによって取得されたレコード
        """
        user_id = self.kwargs['user']
        user_list = PhotoPost.objects.filter(user=user_id).order_by('-posted_at')

        return user_list


class DetailView(DetailView):
    """
     詳細ページのビュー
     """
    template_name = 'detail.html'
    model = PhotoPost


class MypageView(ListView):
    """
    マイページのビュー
    """
    template_name = 'mypage.html'
    paginate_by = 9

    def get_queryset(self):
        """
        クエリを実行する
        :return: クエリによって取得されたコード
        """
        # 現在ログインしているユーザー名はHttpRequest.userに格納されている
        # filter(userフィールド=userオブジェクト)で絞り込む
        queryset = PhotoPost.objects.filter(user=self.request.user).order_by('-posted_at')

        return queryset


class PhotoDeleteView(DeleteView):
    # 操作対象はPhotoPostモデル
    model = PhotoPost
    template_name = 'photo_delete.html'
    success_url = reverse_lazy('photo:mypage')

    def delete(self, request, *args, **kwargs):
        """
        レコードの削除を行う
        :param request:WSGIRequest(HttpRequest)オブジェクト
        :param args:引数として渡される辞書(dict)
        :param kwargs:キーワード付きの辞書(dict)
        {'pk';21}の値にレコードのidが渡される
        :return:
            HttpResponseRedirect(success_url)をかえして
            success_urlにリダイレクト
        """
        # スーパークラスのdelete()を実行
        return super().delete(request, *args, **kwargs)


class BoardView(ListView):
    model = Comment
    template_name = 'board.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            post_id = request.POST.get('post_id')
            content = comment_form.cleaned_data['content']
            user = request.user
            post = PhotoPost.objects.get(pk=post_id)
            Comment.objects.create(photo_post=post, user=user, content=content)
            return redirect('board')
        else:
            return self.get(request, *args, **kwargs)
