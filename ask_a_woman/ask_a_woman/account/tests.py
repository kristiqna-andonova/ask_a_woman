from django.core.exceptions import ValidationError
from django.test import TestCase

from ask_a_woman.account.models import Profile, AppUser

class ProfileModelTestCase(TestCase):
    def setUp(self):

        self.user = AppUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )


        self.profile = self.user.profile

    def test_profile_create_profile_bio__should_create(self):
        # Update the profile_bio for the test
        self.profile.profile_bio = 'This is a test bio'
        self.profile.save()

        self.assertEqual(self.profile.profile_bio, 'This is a test bio')

    def test_profile_create_invalid_profile_bio__should_raise(self):
        self.profile.profile_bio = "a" * 161 # This is my char field max
        with self.assertRaises(ValidationError):
            self.profile.full_clean()

    def test_profile_create_facebook_link__should_create(self):
        self.profile.facebook_link = 'https://softuni.bg/'
        self.profile.save()

    def test_profile_create_invalid_facebook_link__should_raise(self):
        self.profile.facebook_link = 'https://' * 101 # The max limit of the field

        with self.assertRaises(ValidationError):
            self.profile.full_clean()

    def test_profile_create_instagram_link__should_create(self):
        self.profile.instagram_link = 'https://'
        self.profile.save()

    def test_profile_create_invalid_instagram_link__should_raise(self):
        self.profile.instagram_link = 'https://' * 101 # The max limit of the field

        with self.assertRaises(ValidationError):
            self.profile.full_clean()

    def test_profile_create_linkedin_link__should_create(self):
        self.profile.linkedin_link = 'https://'
        self.profile.save()

    def test_profile_create_invalid_linkedin_link__should_raise(self):
        self.profile.linkedin_link = 'https://' * 101  # The max limit of the field

        with self.assertRaises(ValidationError):
            self.profile.full_clean()