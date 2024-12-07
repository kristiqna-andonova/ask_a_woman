from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from ask_a_woman.post.choices import TypeChoices


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        to=get_user_model(),
        related_name='posts',
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(5)
        ]
    )

    description = models.TextField(
        max_length=260,
        validators=[
            MinLengthValidator(5)
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    type = models.CharField(
        max_length=20,
        choices=TypeChoices,
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.author} "
            f"{self.created_at:%Y-%m-%d %H:%M}: "
            f"{self.description} "
            f"({self.type}) "
        )