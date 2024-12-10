from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from ask_a_woman.account.managers import AppUserManager
from ask_a_woman.account.validators import validate_and_crop_image, check_valid_size


class AppUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        unique=True,
        max_length=50
    )

    email = models.EmailField(
        unique=True
    )


    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = AppUserManager()

    USERNAME_FIELD = 'username'  # USERNAME_FIELD means the first credential in our auth

    def __str__(self):
        return self.username



class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )

    date_modified = models.DateTimeField(auto_now=True)

    profile_img = CloudinaryField(
        "image",
        validators=[
            validate_and_crop_image,
            check_valid_size
        ],
        null=True,
        blank=True,
        default='download_i2dvem',

    )

    profile_bio = models.CharField(
        null=True,
        blank=True,
        max_length=160
    )

    facebook_link = models.CharField(
        null=True,
        blank=True,
        max_length=100
    )

    instagram_link = models.CharField(
        null=True,
        blank=True,
        max_length=100
    )

    linkedin_link = models.CharField(
        null=True,
        blank=True,
        max_length=100
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=AppUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
