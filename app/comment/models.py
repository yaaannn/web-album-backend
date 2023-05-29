from django.db import models

from app.photo.models import Photo
from app.user.models import User
from extension.base.model import BaseModel


class Comment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name="照片")
    content = models.CharField(max_length=255, verbose_name="评论内容")
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="父评论",
        related_name="reply",
    )

    class Meta:
        db_table = "a_comment"
        verbose_name = "评论表"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]


class Reply(BaseModel):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies"
    )

    class Meta:
        db_table = "a_reply"
        verbose_name = "回复表"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]
