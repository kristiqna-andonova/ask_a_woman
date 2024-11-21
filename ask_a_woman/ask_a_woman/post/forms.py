from django import forms

from ask_a_woman.common.mixins import ReadOnlyMixin
from ask_a_woman.post.models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'created_at')

    widgets = {
        'description': forms.TextInput(attrs={'placeholder':"Add description"}),
        'type': forms.Select(attrs={'class': 'styled-select'})
    }

class EditPostForm(CreatePostForm):
    pass

class DeletePost(ReadOnlyMixin, CreatePostForm):
    read_only_fields = ['title', 'description', 'type']