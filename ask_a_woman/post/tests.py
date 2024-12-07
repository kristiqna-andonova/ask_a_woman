from django.core.exceptions import ValidationError
from django.test import TestCase

from ask_a_woman.account.models import AppUser
from ask_a_woman.post.models import Post


# Create your tests here.
class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_post_creation_valid__should_create(self):
        post = Post.objects.create(
            author=self.user,
            title='Valid Post Title',
            description='This is a valid post description',
            type='question'
        )

        self.assertEqual(post.title, "Valid Post Title")
        self.assertEqual(post.description, "This is a valid post description")
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.type, "question")

    def test_post_creation_missing_title__should_raise(self):
        with self.assertRaises(ValidationError):
            post = Post.objects.create(
                author=self.user,
                title='',
                description='This is a valid post description',
                type='question'
            )
            post.full_clean()

    def test_post_title_maxing_the_limit(self):
        with self.assertRaises(ValidationError):
            post = Post.objects.create(
                author=self.user,
                title=('q' * 50),
                description='This is a valid post description',
                type='question'
            )
            post.full_clean()

    def test_post_creation_missing_description__should_raise(self):
        with self.assertRaises(ValidationError):
            post = Post.objects.create(
                author=self.user,
                title='Valid Post Title',
                description='',
                type='question'
            )
            post.full_clean()

    def test_post_description_maxing_the_limit(self):
        with self.assertRaises(ValidationError):
            post = Post.objects.create(
                author=self.user,
                title='Title',
                description=('q' * 261),
                type='question'
            )
            post.full_clean()


