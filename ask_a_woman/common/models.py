from django.conf import settings
from django.db import models

from ask_a_woman.account.models import AppUser
from ask_a_woman.post.models import Post


# Create your models here.
class Like(models.Model):
    to_post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        to=AppUser,
        on_delete=models.CASCADE,
    )


class Comment(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['date_time_of_publication']),
        ]
        ordering = ['-date_time_of_publication']

    text = models.TextField(
        max_length=300,
    )

    date_time_of_publication = models.DateTimeField(
        auto_now_add=True,
    )

    to_post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        to=AppUser,
        on_delete=models.CASCADE,
    )


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # when the post is bookmarked

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title}"

    class Meta:
        unique_together = ['user', 'post']
    