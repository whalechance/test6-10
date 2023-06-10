# UserCreationFormクラスをインポート
from django import forms
from django.contrib.auth.forms import UserCreationForm
# models.pyで定義したカスタムUserモデルをインポート
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    UserCreationFormのサブクラス
    """
    bio = forms.CharField(label="自己紹介", widget=forms.Textarea)

    class Meta:
        """
        UserCreationFormのインナークラス
        Attributes:
              model:連携するUserモデル
              fields:フォームで使用するフィールド
        """
        # 連携するUserモデルを設定
        model = CustomUser
        # フォームで使用するフィールドを設定
        # ユーザー名、メールアドレス、パスワード、確認用パスワード
        fields = ('username', 'email', 'password1', 'password2', 'bio')
