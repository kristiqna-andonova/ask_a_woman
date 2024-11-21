from django import forms
from ask_a_woman.common.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add comment...'}),
        }