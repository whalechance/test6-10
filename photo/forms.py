from django.forms import ModelForm
from .models import PhotoPost
from .models import Comment


class PhotoPostForm(ModelForm):
    """
    モデルフォームのサブクラス
    """

    class Meta:
        """
        Modelformのインナークラス
        Attributes:
            model : モデルのクラス
            fields : フォームで使用するモデルのフィールドを指定
        """
        model = PhotoPost
        fields = ['category', 'title', 'comment', 'image1', 'image2', 'video']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
