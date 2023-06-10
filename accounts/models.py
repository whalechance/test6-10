from django.db import models

# Create your models here.
# AbstractUserクラスをインポート
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
     Userモデルを継承したカスタムユーザーモデル
     """
    bio = models.TextField(
        blank=True,
        verbose_name='自己紹介'
    )

    def __str__(self):
        return self.username
    pass
