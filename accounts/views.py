from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, UpdateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model


# Create your views here.

class SignUpView(CreateView):
    """
    サインアップページのビュー
    """
    # form.pyで定義したフォームのクラス
    form_class = CustomUserCreationForm
    # レンダリングするテンプレート
    template_name = "signup.html"

    # サインアップ完了後のリダイレクト先のurlパターン
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        """  CreateViewクラスのform_valid()をオーバーライド
        フォームのバリデーションを通過したときに呼ばれる
        フォームデータの登録を行う
        parameters:
              form(django.forms.Form):
                  form_classに格納されているCustomUserCreationFormオブジェクト
        return:
        　　HttpResponseRedirectオブジェクト:
                 スーパークラスのform_valid()の戻り値を返すことで、
                 success_urlで設定されているurlにリダイレクトさせる
        """
        # formオブジェクトのフィールドの値をデータベースに保存
        user = form.save(commit=False)
        user.bio = form.cleaned_data['bio']
        user.save()
        # 戻り値はスーパクラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)


class SignUpSuccessView(TemplateView):
    """
    サインアップ完了ページビュー
    """
    # レンダリングするテンプレート
    template_name = "signup_success.html"


def bio_update(request):
    return render(request, 'bio_update.html')
