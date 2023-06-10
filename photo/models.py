from django.db import models
# from imagekit.models import ImageSpecField
# from imagekit.processors import ResizeToFit

# Create your models here.

# accountsアプリのmodelsモジュールからCustomUserをインポート
from accounts.models import CustomUser


class Category(models.Model):
    """
    投稿する写真のカテゴリを管理するモデル
    """
    # カテゴリ名のフィールド
    title = models.CharField(
        verbose_name="カテゴリ",
        max_length=20)


def __str__(self):
    """
    オブジェクトを文字列に変換して返す
    :return(str):カテゴリ名
    """
    return self.title


class PhotoPost(models.Model):
    """
    投稿されたデータを管理するモデル
    """
    # CustomUserモデル(のuser_id)とPhotoPostモデルを
    # 1対多の関係で結びつける
    # CustomUserが親でPhotoPostが子の関係となる
    user = models.ForeignKey(
        CustomUser,
        # フィールドのタイトル
        verbose_name="ユーザー",
        # ユーザーを削除する場合はそのユーザーの登録データもすべて削除する
        on_delete=models.CASCADE
    )

    # Categoryモデル(のtitle)とPhotoPostモデルを
    # 1対多の関係で結びつける
    # Categoryが親でPhotoPostが子の関係となる
    category = models.ForeignKey(
        Category,
        # フィールドのタイトル
        verbose_name="カテゴリ",
        # カテゴリに関連付けられた投稿データが存在する場合は
        # そのカテゴリを削除できないようにする
        on_delete=models.PROTECT
    )

    # タイトル用のフィールド
    title = models.CharField(
        verbose_name="タイトル",
        max_length=200
    )

    # コメント用のフィールド
    comment = models.TextField(
        verbose_name="コメント",
    )

    # イメージのフィールド
    image1 = models.ImageField(
        verbose_name="イメージ1",
        upload_to="photos",  # photosにファイルを保存
        blank=True,
        null=True
    )

    # イメージのフィールド
    image2 = models.ImageField(
        verbose_name="イメージ2",
        upload_to="photos",  # photosにファイルを保存
        blank=True,  # フィールド値の設定は必須ではない
        null=True  # データベースにnullが保存されることを許容
    )

    # 動画ファイルのフィールド
    video = models.FileField(
        verbose_name="動画",
        upload_to="videos",
        blank=True,
        null=True
    )

    # サムネイル作成
    # video_thumbnail = ImageSpecField(
    # source="video",
    # processors=[ResizeToFit(width=200, height=200)],
    # format="JPEG",
    # options={"quality": 90}
    #  )

    # 投稿日時のフィールド
    posted_at = models.DateTimeField(
        verbose_name="投稿日時",
        auto_now_add=True  # 日時を自動追加
    )

    likes = models.ManyToManyField(
        CustomUser,
        through='Like',
        related_name="liked_posts",
        verbose_name="いいね",
    )

    def __str__(self):
        """
        オブジェクトを文字列に変換して返す
        :return(str):投稿記事のタイトル
        """
        return self.title


class Like(models.Model):
    """
    いいねを管理するモデル
    """
    user = models.ForeignKey(
        CustomUser,
        verbose_name="ユーザー",
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        PhotoPost,
        verbose_name="投稿",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        verbose_name="作成日時",
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"


class Comment(models.Model):
    photo_post = models.ForeignKey(
        PhotoPost,
        verbose_name="投稿",
        related_name="comments",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name="ユーザー",
        on_delete=models.CASCADE
    )
    content = models.TextField(verbose_name="コメント")
    created_at = models.DateTimeField(verbose_name="投稿日時", auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.photo_post.title}"
