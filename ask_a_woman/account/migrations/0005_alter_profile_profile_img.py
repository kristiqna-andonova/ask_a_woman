# Generated by Django 5.1.2 on 2024-11-14 19:52

import ask_a_woman.account.validators
import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_profile_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, validators=[ask_a_woman.account.validators.validate_and_crop_image, ask_a_woman.account.validators.check_valid_size], verbose_name='image'),
        ),
    ]